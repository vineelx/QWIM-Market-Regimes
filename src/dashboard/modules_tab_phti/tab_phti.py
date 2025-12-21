from shiny import ui, module, render, reactive
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

@module.ui
def tab_phti_ui(data_utils=None, data_inputs=None):
    return ui.layout_sidebar(
        ui.sidebar(
            ui.h4("PHTI Controls"),
            ui.hr(),
            ui.input_date_range(
                "dates", 
                "Select Date Range", 
                start="2000-01-01", 
                end="2025-05-01"
            ),
            ui.input_checkbox_group(
                "strategies", 
                "Compare Strategies", 
                choices=[
                    "SPY (Benchmark)", 
                    "PHTI (WCP)", 
                    "PHTI (FE)", 
                    "PHTI (FEL)"
                ],
                selected=["SPY (Benchmark)", "PHTI (WCP)"]
            ),
            ui.hr(),
            ui.p("Regime Switching Model using Persistent Homology.", style="font-size: 0.8em; color: gray;")
        ),
        
        # fillable=False here ensures the main area grows with content (Page Scroll)
        ui.navset_card_underline(
            
            # --- TAB 1: Analysis ---
            ui.nav_panel(
                "Analysis",
                ui.card_header("Performance & Signals"),
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Cumulative Growth ($1)"),
                        ui.output_ui("plot_cumulative"),
                        fill=False  # Don't shrink to fit, grow with content
                    ),
                    ui.card(
                        ui.card_header("Turbulence Indicators (Dual Axis)"),
                        ui.output_ui("plot_signals"),
                        fill=False
                    ),
                    col_widths=[12, 12]
                )
            ),
            
            # --- TAB 2: Risk & Regimes ---
            ui.nav_panel(
                "Risk & Regimes",
                ui.card_header("Drawdowns & Market States"),
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Drawdown from Peak (%)"),
                        ui.output_ui("plot_drawdown"),
                        fill=False
                    ),
                    ui.card(
                        ui.card_header("Market Regime Quintiles (1=Calm, 5=Turbulent)"),
                        ui.output_ui("plot_quintiles"),
                        fill=False
                    ),
                    col_widths=[12, 12]
                )
            ),

            # --- TAB 3: Allocations ---
            ui.nav_panel(
                "Allocations",
                ui.card_header("Dynamic Portfolio Weights"),
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Exposure to Risky Asset (SPY)"),
                        ui.output_ui("plot_weights"),
                        fill=False
                    ),
                    ui.card(
                        ui.card_header("Strategy Reaction Functions"),
                        ui.output_ui("plot_reaction"),
                        fill=False
                    ),
                    col_widths=[12, 12]
                )
            ),
        ),
        fillable=False  # <--- CRITICAL: Enables full page scrolling
    )

@module.server
def tab_phti_server(input, output, session, data_utils, data_inputs, reactives_shiny):
    
    # --- 1. Load Data ---
    df_raw = data_inputs.get("phti_data")
    
    if df_raw is None:
        df_raw = pd.DataFrame()
    else:
        if not np.issubdtype(df_raw["Date"].dtype, np.datetime64):
            df_raw["Date"] = pd.to_datetime(df_raw["Date"])

    # --- 2. Reactive Data ---
    @reactive.Calc
    def filtered_df():
        if df_raw.empty: return df_raw
        start, end = input.dates()
        mask = (df_raw["Date"] >= pd.Timestamp(start)) & (df_raw["Date"] <= pd.Timestamp(end))
        return df_raw.loc[mask].copy()

    # --- Helper: Drawdown ---
    def calc_drawdown(series):
        s = series.fillna(0)
        wealth = (1 + s).cumprod()
        peaks = wealth.cummax()
        peaks[peaks == 0] = 1 
        return (wealth - peaks) / peaks

    # --- PLOT 1: Cumulative ---
    @output
    @render.ui
    def plot_cumulative():
        d = filtered_df()
        if d.empty: return "No data."
        fig = go.Figure()
        
        def get_cum(col): return (1 + d[col].fillna(0)).cumprod()
        
        sel = input.strategies()
        if "SPY (Benchmark)" in sel and "SPY" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=get_cum("SPY"), name="SPY", line=dict(color='black')))
        if "PHTI (WCP)" in sel and "Ret_PHTI_WCP" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=get_cum("Ret_PHTI_WCP"), name="PHTI (WCP)", line=dict(color='#ef553b')))
        if "PHTI (FE)" in sel and "Ret_PHTI_FE" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=get_cum("Ret_PHTI_FE"), name="PHTI (FE)", line=dict(color='#00cc96')))
        if "PHTI (FEL)" in sel and "Ret_PHTI_FEL" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=get_cum("Ret_PHTI_FEL"), name="PHTI (FEL)", line=dict(color='#ab63fa')))

        fig.update_layout(template="plotly_white", margin=dict(l=0,r=0,t=10,b=0), height=350, hovermode="x unified", yaxis_title="Growth of $1")
        return ui.HTML(fig.to_html(full_html=False))

    # --- PLOT 2: Signals ---
    @output
    @render.ui
    def plot_signals():
        d = filtered_df()
        if d.empty: return ui.div()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        if "Signal_PHTI" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=d["Signal_PHTI"], fill='tozeroy', name='PHTI', line=dict(color='#ef553b', width=1.5)), secondary_y=False)
        if "Signal_OTI" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=d["Signal_OTI"], name='OTI', line=dict(color='gray', dash='dot', width=1)), secondary_y=True)
            
        fig.update_layout(template="plotly_white", margin=dict(l=0,r=0,t=30,b=0), height=300, title="Turbulence Indicators", hovermode="x unified")
        fig.update_yaxes(title_text="PHTI", secondary_y=False)
        fig.update_yaxes(title_text="OTI", showgrid=False, secondary_y=True)
        return ui.HTML(fig.to_html(full_html=False))

    # --- PLOT 3: Drawdown ---
    @output
    @render.ui
    def plot_drawdown():
        d = filtered_df()
        if d.empty: return ui.div()
        fig = go.Figure()
        sel = input.strategies()

        if "SPY (Benchmark)" in sel and "SPY" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=calc_drawdown(d["SPY"]), name="SPY DD", fill='tozeroy', line=dict(color='black', width=1)))
        
        if "PHTI (WCP)" in sel and "Ret_PHTI_WCP" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=calc_drawdown(d["Ret_PHTI_WCP"]), name="PHTI (WCP) DD", line=dict(color='#ef553b', width=1)))

        if "PHTI (FE)" in sel and "Ret_PHTI_FE" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=calc_drawdown(d["Ret_PHTI_FE"]), name="PHTI (FE) DD", line=dict(color='#00cc96', width=1)))

        if "PHTI (FEL)" in sel and "Ret_PHTI_FEL" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=calc_drawdown(d["Ret_PHTI_FEL"]), name="PHTI (FEL) DD", line=dict(color='#ab63fa', width=1)))

        fig.update_layout(template="plotly_white", margin=dict(l=0,r=0,t=20,b=0), height=300, hovermode="x unified", yaxis_title="Drawdown", yaxis_tickformat=".1%")
        return ui.HTML(fig.to_html(full_html=False))

    # --- PLOT 4: Quintiles ---
    @output
    @render.ui
    def plot_quintiles():
        d = filtered_df()
        if d.empty or "Signal_PHTI" not in d.columns: return ui.div()
        
        full_series = df_raw["Signal_PHTI"].dropna()
        if full_series.empty: return "No signal data"
        try:
            _, bins = pd.qcut(full_series, 5, retbins=True, duplicates='drop')
            d["Quintile"] = pd.cut(d["Signal_PHTI"], bins=bins, labels=False, include_lowest=True) + 1
        except: return "Error in quintiles"

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d["Date"], y=d["Quintile"], mode='lines+markers', name="Regime", line=dict(shape='hv', color='#636efa'), marker=dict(size=4)))
        fig.update_layout(template="plotly_white", margin=dict(l=0,r=0,t=30,b=0), height=300, title="Regime (1=Calm, 5=Turbulent)", hovermode="x unified")
        return ui.HTML(fig.to_html(full_html=False))

    # --- PLOT 5: Allocations ---
    @output
    @render.ui
    def plot_weights():
        d = filtered_df()
        if d.empty: return "No data."
        
        sel = input.strategies()
        fig = go.Figure()
        has_data = False

        if "PHTI (WCP)" in sel and "Wgt_PHTI_WCP" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=d["Wgt_PHTI_WCP"], mode='lines', name='WCP Weight (SPY)', line=dict(color='#ef553b', width=2)))
            has_data = True

        if "PHTI (FE)" in sel and "Wgt_PHTI_FE" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=d["Wgt_PHTI_FE"], mode='lines', name='FE Weight (SPY)', line=dict(color='#00cc96', width=2)))
            has_data = True
            
        if "PHTI (FEL)" in sel and "Wgt_PHTI_FEL" in d.columns:
            fig.add_trace(go.Scatter(x=d["Date"], y=d["Wgt_PHTI_FEL"], mode='lines', name='FEL Weight (SPY)', line=dict(color='#ab63fa', width=2)))
            has_data = True
        
        if not has_data: return "Select a PHTI strategy to see weights."

        fig.update_layout(template="plotly_white", margin=dict(l=0,r=0,t=20,b=0), height=300, title="Allocation to Risky Asset (SPY)", hovermode="x unified", yaxis=dict(range=[-0.05, 1.05], title="Weight %"))
        return ui.HTML(fig.to_html(full_html=False))

    # --- PLOT 6: Reaction Function ---
    @output
    @render.ui
    def plot_reaction():
        d = filtered_df()
        if d.empty or "Signal_PHTI" not in d.columns: return ui.div()
        
        sel = input.strategies()
        fig = go.Figure()
        has_data = False

        def add_reaction(w_col, name, color):
            sub = d[["Signal_PHTI", w_col]].dropna()
            if sub.empty: return
            fig.add_trace(go.Scatter(x=sub["Signal_PHTI"], y=sub[w_col], mode='markers', name=name, marker=dict(color=color, size=5, opacity=0.4)))
            sub_sorted = sub.sort_values("Signal_PHTI")
            sub_sorted["Smooth"] = sub_sorted[w_col].rolling(window=20, center=True, min_periods=1).mean()
            fig.add_trace(go.Scatter(x=sub_sorted["Signal_PHTI"], y=sub_sorted["Smooth"], mode='lines', name=f"{name} Trend", line=dict(color=color, width=2)))

        if "PHTI (WCP)" in sel and "Wgt_PHTI_WCP" in d.columns:
            add_reaction("Wgt_PHTI_WCP", "WCP", "#ef553b")
            has_data = True

        if "PHTI (FE)" in sel and "Wgt_PHTI_FE" in d.columns:
            add_reaction("Wgt_PHTI_FE", "FE", "#00cc96")
            has_data = True

        if "PHTI (FEL)" in sel and "Wgt_PHTI_FEL" in d.columns:
            add_reaction("Wgt_PHTI_FEL", "FEL", "#ab63fa")
            has_data = True
            
        if not has_data: return "Select a PHTI strategy to see reaction."

        fig.update_layout(template="plotly_white", height=300, margin=dict(l=0,r=0,t=40,b=0), title="Strategy Reaction Function", xaxis_title="Turbulence Signal (High = Bad)", yaxis_title="Weight in SPY")
        return ui.HTML(fig.to_html(full_html=False))