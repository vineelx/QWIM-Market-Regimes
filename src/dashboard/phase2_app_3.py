from shiny import module, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# --- 1. DATA LOADING LOGIC (Internal to Module) ---
# We calculate the path relative to this file to ensure it works anywhere
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def load_data_internal():
    data = {}
    for model in ["tft", "lstm"]:
        path = DATA_DIR / f"{model}_clean.csv"
        if path.exists():
            df = pd.read_csv(path)
            df['time'] = pd.to_datetime(df['time'])
            data[model.upper()] = df
            
    # Calculate Regimes if LSTM exists
    if "LSTM" in data:
        benchmark = data["LSTM"].copy()
        benchmark['Rolling_Vol'] = benchmark['captured_returns'].rolling(window=21).std() * (252**0.5)
        
        low = benchmark['Rolling_Vol'].quantile(0.33)
        high = benchmark['Rolling_Vol'].quantile(0.66)
        
        def get_regime(vol):
            if pd.isna(vol): return "Unknown"
            if vol < low: return "Low Volatility (Calm)"
            if vol > high: return "High Volatility (Crisis)"
            return "Normal Conditions"

        regime_map = benchmark.set_index('time')['Rolling_Vol'].apply(get_regime).to_dict()
        for model in data:
            data[model]['Regime'] = data[model]['time'].map(regime_map)
            
    return data

# Load data once when module is imported
dfs = load_data_internal()

# --- 2. MODULE UI ---
@module.ui
def tab_momentum_ui():
    """UI for the Momentum Strategies Tab."""
    return ui.layout_sidebar(
        ui.sidebar(
            ui.h4("Settings"),
            ui.input_slider("cost", "Transaction Cost (bps)", 0, 3.0, 0, step=0.5),
            ui.input_date_range("dates", "Date Range", 
                              start="2016-01-01", end="2020-12-31"),
            ui.hr(),
            ui.input_checkbox_group("models", "Select Models:", 
                                  {"TFT": "Transformer (TFT)", "LSTM": "LSTM Benchmark"},
                                  selected=["TFT", "LSTM"]),
            ui.br(),
            ui.h6("Regime Definition:"),
            ui.p("Regimes are defined by benchmark volatility. 'High Volatility' indicates crash periods.", 
               style="font-size: 0.8em; color: #666;")
        ),
        
        # Main Content
        ui.navset_card_tab(
            ui.nav_panel("Performance & Ratios",
                ui.row(
                    ui.column(8, ui.card(ui.card_header("Cumulative Returns"), output_widget("main_plot"))),
                    ui.column(4, ui.card(ui.card_header("Risk-Adjusted Ratios"), output_widget("ratios_plot")))
                ),
                ui.card(ui.card_header("Detailed Statistics"), ui.output_data_frame("stats_table"))
            ),
            ui.nav_panel("Market Regime Analysis",
                 ui.row(
                     ui.column(6, ui.card(ui.card_header("Annualized Return by Regime"), output_widget("regime_plot"))),
                     ui.column(6, ui.card(ui.card_header("Drawdown Severity"), output_widget("drawdown_plot")))
                 ),
                 ui.p("Insight: TFT (Orange) typically outperforms during 'High Volatility' periods due to the attention mechanism.")
            )
        )
    )

# --- 3. MODULE SERVER ---
@module.server
def tab_momentum_server(input, output, session, data_utils, data_inputs, reactives_shiny):
    """
    Server logic for Momentum Strategies.
    Args:
        data_utils, data_inputs, reactives_shiny: Passed from main_App for consistency,
        even if we rely on internal CSVs for this specific tab.
    """

    @reactive.Calc
    def filtered_data():
        start = pd.to_datetime(input.dates()[0])
        end = pd.to_datetime(input.dates()[1])
        cost_val = float(input.cost())
        
        # Robust Mapping
        COLUMN_MAP = {
            0.0: "captured_returns",
            0.5: "captured_returns_0_5_bps",
            1.0: "captured_returns_1_0_bps",
            1.5: "captured_returns_1_5_bps",
            2.0: "captured_returns_2_0_bps",
            2.5: "captured_returns_2_5_bps",
            3.0: "captured_returns_3_0_bps"
        }
        col = COLUMN_MAP.get(cost_val)
        if not col: return pd.DataFrame()

        combined = []
        for model_name in input.models():
            if model_name in dfs:
                df = dfs[model_name].copy()
                mask = (df['time'] >= start) & (df['time'] <= end)
                df_filt = df.loc[mask].copy()
                
                if col in df_filt.columns:
                    df_filt['Model'] = model_name
                    df_filt['Daily Return'] = df_filt[col]
                    df_filt['Cumulative'] = (1 + df_filt[col]).cumprod() - 1
                    roll_max = df_filt['Cumulative'].cummax()
                    df_filt['Drawdown'] = (df_filt['Cumulative'] - roll_max) / (1 + roll_max)
                    combined.append(df_filt)
        
        if combined: return pd.concat(combined)
        return pd.DataFrame()

    @render_widget
    def main_plot():
        df = filtered_data()
        if df.empty: return go.Figure()
        fig = px.line(df, x="time", y="Cumulative", color="Model",
                      title="Cumulative Returns Over Time",
                      color_discrete_map={"TFT": "orange", "LSTM": "blue"})
        fig.update_layout(template="plotly_white", hovermode="x unified")
        fig.update_yaxes(tickformat=".1%")
        return fig

    @render_widget
    def ratios_plot():
        df = filtered_data()
        if df.empty: return go.Figure()
        metrics = []
        for model in df['Model'].unique():
            sub = df[df['Model'] == model]['Daily Return']
            sharpe = (sub.mean() / sub.std() * (252**0.5)) if sub.std() > 0 else 0
            downside = sub[sub < 0].std() * (252**0.5)
            sortino = (((1 + sub.mean())**252 - 1) / downside) if downside > 0 else 0
            cum = (1 + sub).cumprod()
            mdd = ((cum - cum.cummax()) / cum.cummax()).min()
            calmar = (((1 + sub.mean())**252 - 1) / abs(mdd)) if mdd != 0 else 0
            
            metrics.append({"Model": model, "Metric": "Sharpe", "Value": sharpe})
            metrics.append({"Model": model, "Metric": "Sortino", "Value": sortino})
            metrics.append({"Model": model, "Metric": "Calmar", "Value": calmar})
            
        fig = px.bar(pd.DataFrame(metrics), x="Metric", y="Value", color="Model", barmode="group",
                     color_discrete_map={"TFT": "orange", "LSTM": "blue"})
        fig.update_layout(template="plotly_white")
        return fig

    @render_widget
    def regime_plot():
        df = filtered_data()
        if df.empty: return go.Figure()
        stats = df.groupby(['Model', 'Regime'])['Daily Return'].mean().reset_index()
        stats['Annualized Return'] = stats['Daily Return'] * 252
        order = ["Low Volatility (Calm)", "Normal Conditions", "High Volatility (Crisis)"]
        
        fig = px.bar(stats, x="Regime", y="Annualized Return", color="Model", barmode="group",
                     category_orders={"Regime": order},
                     color_discrete_map={"TFT": "orange", "LSTM": "blue"})
        fig.update_layout(template="plotly_white")
        fig.update_yaxes(tickformat=".1%")
        return fig

    @render_widget
    def drawdown_plot():
        df = filtered_data()
        if df.empty: return go.Figure()
        fig = px.area(df, x="time", y="Drawdown", color="Model",
                      title="Underwater Plot",
                      color_discrete_map={"TFT": "orange", "LSTM": "blue"})
        fig.update_layout(template="plotly_white", hovermode="x unified")
        fig.update_yaxes(tickformat=".1%")
        return fig

    @render.data_frame
    def stats_table():
        df = filtered_data()
        if df.empty: return pd.DataFrame()
        
        def get_stats(series):
            ann_ret = (1 + series.mean())**252 - 1
            ann_vol = series.std() * (252**0.5)
            sharpe = (series.mean() / series.std() * (252**0.5)) if series.std() > 0 else 0
            neg_ret = series[series < 0]
            downside = neg_ret.std() * (252**0.5)
            sortino = (ann_ret / downside) if downside > 0 else 0
            cum = (1 + series).cumprod()
            mdd = ((cum - cum.cummax()) / cum.cummax()).min()
            calmar = (ann_ret / abs(mdd)) if mdd != 0 else 0
            
            return pd.Series({
                "Total Ret": (1 + series).prod() - 1,
                "Ann. Vol": ann_vol,
                "Sharpe": sharpe,
                "Sortino": sortino,
                "Calmar": calmar,
                "Max DD": mdd
            })

        stats = df.groupby("Model")['Daily Return'].apply(get_stats).unstack()
        for col in ["Total Ret", "Ann. Vol", "Max DD"]:
            stats[col] = stats[col].apply(lambda x: f"{x:.2%}")
        for col in ["Sharpe", "Sortino", "Calmar"]:
            stats[col] = stats[col].apply(lambda x: f"{x:.2f}")
            
        return render.DataGrid(stats.reset_index())