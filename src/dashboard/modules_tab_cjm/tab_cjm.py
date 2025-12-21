from shiny import ui, module, render, reactive
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from src.dashboard.utils_dashboard.utils_data_cjm import (
    load_backtest,
    load_spy_ts,
    load_cjm_regimes,
)

# ==========================
# module ui
# ==========================
@module.ui
def tab_cjm_ui():

    return ui.page_sidebar(
        ui.sidebar(
            ui.h4("Time Period Selection"),
            ui.input_select(
                "cjm_period",
                "Select Time Period",
                {
                    "last1": "Last 1 Year",
                    "last2": "Last 2 Years",
                    "last3": "Last 3 Years",
                },
                selected="last3",
            ),

            ui.hr(),
            # Portfolio Analysis tab
            ui.panel_conditional(
                "input.cjm_tab == 'Portfolio Analysis'",
                ui.h4("Analysis Options"),
                ui.input_select(
                    "cjm_analysis_type",
                    "Analysis Type",
                    {
                        "pvb": "Portfolio vs Benchmark",
                        "ret_dist": "Returns Distribution",
                        "drawdown": "Drawdown Analysis",
                    },
                    selected="pvb",
                ),
            ),

            # Portfolio Comparison tab
            ui.panel_conditional(
                "input.cjm_tab == 'Portfolio Comparison'",
                ui.h4("Visualization Type"),
                ui.input_select(
                    "cjm_comp_vis",
                    "Comparison View",
                    {
                        "abs": "Absolute Value",
                        "pct": "Percent Change (Daily Return)",
                        "cum": "Cumulative Return",
                    },
                    selected="cum",
                ),
            ),

            ui.hr(),
            ui.p("Compare CJM regime-based strategy vs SPY buy & hold."),
        ),

        ui.navset_tab(
            # ---------- 1) Portfolio Analysis ----------
            ui.nav_panel(
                "Portfolio Analysis",
                ui.card(
                    ui.card_header(ui.output_text("cjm_plot_title")),
                    ui.p(ui.output_text("cjm_plot_subtitle")),
                    ui.output_plot("cjm_plot", height="450px"),
                ),

                ui.layout_columns(
                    ui.card(
                        ui.card_header("Basic Statistics"),
                        ui.output_ui("cjm_table_basic"),   # table -> ui
                    ),
                    ui.card(
                        ui.card_header("Performance Metrics"),
                        ui.output_ui("cjm_table_perf"),    # table -> ui
                    ),
                    col_widths=(6, 6),
                ),
            ),

            # ---------- 2) Portfolio Comparison ----------
            ui.nav_panel(
                "Portfolio Comparison",
                ui.card(
                    ui.card_header(ui.output_text("cjm_comp_title")),
                    ui.output_plot("cjm_comp_plot", height="450px"),
                ),
                ui.card(
                    ui.card_header("Performance Statistics (Portfolio vs Benchmark)"),
                    ui.output_ui("cjm_comp_table"),       # table -> ui
                ),
            ),

            id="cjm_tab",
        ),
    )


# ==========================
# module server
# ==========================
@module.server
def tab_cjm_server(input, output, session, data_utils=None, data_inputs=None, reactives_shiny=None):

    @reactive.calc
    def df_bt():
        df = load_backtest().sort_values("date").reset_index(drop=True)

        # log returns -> normal returns
        df["ret_port_pct"] = np.exp(df["r_port"]) - 1
        df["ret_bench_pct"] = np.exp(df["r_bench"]) - 1
        return df

    @reactive.calc
    def df_period():
        df = df_bt()
        period = input.cjm_period()

        end_date = df["date"].max()
        if period == "last1":
            start = end_date - pd.DateOffset(years=1)
        elif period == "last2":
            start = end_date - pd.DateOffset(years=2)
        else:
            start = end_date - pd.DateOffset(years=3)

        return df[df["date"] >= start].copy()
    
    @reactive.calc
    def stats():
        df = df_period()
        if df.empty:
            return None

        daily_port = df["ret_port_pct"]
        daily_bench = df["ret_bench_pct"]

        first_idx_port = df["idx_port"].iloc[0]
        first_idx_bench = df["idx_bench"].iloc[0]
        final_idx_port = df["idx_port"].iloc[-1]
        final_idx_bench = df["idx_bench"].iloc[-1]

        # total return
        total_ret_port = final_idx_port / first_idx_port - 1
        total_ret_bench = final_idx_bench / first_idx_bench - 1

        # annual return, volatility, sharpe ratio
        ann_ret_port = daily_port.mean() * 252
        ann_ret_bench = daily_bench.mean() * 252

        vol_port = daily_port.std() * np.sqrt(252)
        vol_bench = daily_bench.std() * np.sqrt(252)

        sharpe_port = ann_ret_port / vol_port if vol_port > 0 else np.nan
        sharpe_bench = ann_ret_bench / vol_bench if vol_bench > 0 else np.nan

        # Drawdown
        dd_port = df["idx_port"] / df["idx_port"].cummax() - 1.0
        dd_bench = df["idx_bench"] / df["idx_bench"].cummax() - 1.0
        mdd_port = dd_port.min()
        mdd_bench = dd_bench.min()

        # Returns Distribution mean, std
        mean_port = daily_port.mean()
        std_port = daily_port.std()

        win_rate = (daily_port > 0).mean()
        best_day = daily_port.max()
        worst_day = daily_port.min()
        skew = daily_port.skew()

        fisher_kurt = daily_port.kurt()
        kurt = fisher_kurt + 3

        return {
            "final_idx_port": final_idx_port,
            "final_idx_bench": final_idx_bench,
            "total_ret_port": total_ret_port,
            "total_ret_bench": total_ret_bench,
            "ann_ret_port": ann_ret_port,
            "ann_ret_bench": ann_ret_bench,
            "vol_port": vol_port,
            "vol_bench": vol_bench,
            "sharpe_port": sharpe_port,
            "sharpe_bench": sharpe_bench,
            "mean_port": mean_port,
            "std_port": std_port,
            "mdd_port": mdd_port,
            "mdd_bench": mdd_bench,
            "win_rate": win_rate,
            "best_day": best_day,
            "worst_day": worst_day,
            "skew": skew,
            "kurt": kurt,
        }

    # ------------------ Plot title / subtitle ------------------
    @output
    @render.text
    def cjm_plot_title():
        atype = input.cjm_analysis_type()
        if atype == "ret_dist":
            return "Returns Distribution (mean variance portfolio vs SPY)"
        elif atype == "drawdown":
            return "Drawdown Analysis (mean variance portfolio vs SPY)"
        else:
            return "Portfolio vs Benchmark (mean variance portfolio vs SPY)"

    @output
    @render.text
    def cjm_plot_subtitle():
        s = stats()
        if s is None:
            return ""

        atype = input.cjm_analysis_type()

        if atype == "ret_dist":
            mean_pct = s["mean_port"] * 100
            std_pct = s["std_port"] * 100
            return f"Portfolio Mean: {mean_pct:.4f}%, Std Dev: {std_pct:.4f}%"

        elif atype == "drawdown":
            mdd_p = s["mdd_port"] * 100
            mdd_b = s["mdd_bench"] * 100
            return f"Max Drawdown – Strategy: {mdd_p:.2f}%, SPY: {mdd_b:.2f}%"

        else:
            tr_p = s["total_ret_port"] * 100
            tr_b = s["total_ret_bench"] * 100
            return f"Strategy Total Return: {tr_p:.2f}%, SPY: {tr_b:.2f}%"

    # ------------------ Main plot ------------------
    @output
    @render.plot
    def cjm_plot():
        df = df_period()
        atype = input.cjm_analysis_type()

        if df.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(0.5, 0.5, "No data for selected period",
                    ha="center", va="center", transform=ax.transAxes)
            ax.axis("off")
            return fig

        if atype == "ret_dist":
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(df["ret_port_pct"] * 100, bins=40, alpha=0.6, label="Strategy")
            ax.hist(df["ret_bench_pct"] * 100, bins=40, alpha=0.6, label="SPY")
            ax.set_xlabel("Daily Return (%)")
            ax.set_ylabel("Frequency")
            ax.legend()
            return fig

        elif atype == "drawdown":
            dd_port = df["idx_port"] / df["idx_port"].cummax() - 1.0
            dd_bench = df["idx_bench"] / df["idx_bench"].cummax() - 1.0

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df["date"], dd_port * 100, label="Strategy")
            ax.plot(df["date"], dd_bench * 100, label="SPY", linestyle="--")
            ax.axhline(0, color="black", linewidth=0.8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Drawdown (%)")
            ax.legend()
            fig.autofmt_xdate()
            return fig

        else:
            fig, ax = plt.subplots(figsize=(10, 5))

            base_port = df["idx_port"].iloc[0]
            base_bench = df["idx_bench"].iloc[0]

            cum_port = df["idx_port"] / base_port - 1
            cum_bench = df["idx_bench"] / base_bench - 1

            ax.plot(df["date"], cum_port * 100, label="CJM Strategy")
            ax.plot(df["date"], cum_bench * 100, label="SPY Buy & Hold",
                    linestyle="--")

            ax.set_xlabel("Date")
            ax.set_ylabel("Cumulative Return (%)")
            ax.legend()
            fig.autofmt_xdate()
            return fig

    # ------------------ Tables: Portfolio Analysis ------------------
    @output
    @render.ui
    def cjm_table_basic():
        s = stats()
        if s is None:
            return ui.HTML("<p>No data for selected period.</p>")

        df = pd.DataFrame(
            {
                "Metric": [
                    "Ann. Return (Strategy, %)",
                    "Ann. Return (SPY, %)",
                    "Ann. Vol (Strategy, %)",
                    "Ann. Vol (SPY, %)",
                    "Sharpe (Strategy)",
                    "Sharpe (SPY)",
                ],
                "Value": [
                    s["ann_ret_port"] * 100,
                    s["ann_ret_bench"] * 100,
                    s["vol_port"] * 100,
                    s["vol_bench"] * 100,
                    s["sharpe_port"],
                    s["sharpe_bench"],
                ],
            }
        )

        html = df.to_html(index=False, classes="table table-sm")
        return ui.HTML(html)

    @output
    @render.ui
    def cjm_table_perf():
        s = stats()
        if s is None:
            return ui.HTML("<p>No data for selected period.</p>")

        df = pd.DataFrame(
            {
                "Metric": [
                    "Total Return (%)",
                    "Max Drawdown (%)",
                    "Win Rate (%)",
                    "Best Day (%)",
                    "Worst Day (%)",
                    "Skewness",
                    "Kurtosis",
                ],
                "Value": [
                    s["total_ret_port"] * 100,
                    s["mdd_port"] * 100,
                    s["win_rate"] * 100,
                    s["best_day"] * 100,
                    s["worst_day"] * 100,
                    s["skew"],
                    s["kurt"],
                ],
            }
        )

        html = df.to_html(index=False, classes="table table-sm")
        return ui.HTML(html)

    # ------------------ Portfolio Comparison ------------------
    @output
    @render.text
    def cjm_comp_title():
        vis = input.cjm_comp_vis()
        if vis == "abs":
            return "Portfolio vs Benchmark – Absolute Index Level"
        elif vis == "pct":
            return "Portfolio vs Benchmark – Daily Returns (%)"
        else:
            return "Portfolio vs Benchmark – Cumulative Return (%)"

    @output
    @render.plot
    def cjm_comp_plot():
        df = df_period()
        vis = input.cjm_comp_vis()

        if df.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(0.5, 0.5, "No data for selected period",
                    ha="center", va="center", transform=ax.transAxes)
            ax.axis("off")
            return fig

        fig, ax = plt.subplots(figsize=(10, 5))

        # ----- 1) Absolute index level (but rebased at period start) -----
        if vis == "abs":
            # rebase so that it starts from 1
            base_port = df["idx_port"].iloc[0]
            base_bench = df["idx_bench"].iloc[0]

            idx_port_rebased = df["idx_port"] / base_port
            idx_bench_rebased = df["idx_bench"] / base_bench

            ax.plot(df["date"], idx_port_rebased, label="Portfolio")
            ax.plot(df["date"], idx_bench_rebased, label="Benchmark", linestyle="--")
            ax.set_ylabel("Index Level (rebased, start = 1)")

        # ----- 2) Daily % return -----
        elif vis == "pct":
            ax.plot(df["date"], df["ret_port_pct"] * 100, label="Portfolio")
            ax.plot(df["date"], df["ret_bench_pct"] * 100, label="Benchmark", linestyle="--")
            ax.set_ylabel("Daily Return (%)")

        # ----- 3) Cumulative return -----
        else:  # "cum"
            cum_port = (1 + df["ret_port_pct"]).cumprod() - 1
            cum_bench = (1 + df["ret_bench_pct"]).cumprod() - 1
            ax.plot(df["date"], cum_port * 100, label="Portfolio")
            ax.plot(df["date"], cum_bench * 100, label="Benchmark", linestyle="--")
            ax.set_ylabel("Cumulative Return (%)")

        ax.set_xlabel("Date")
        ax.legend()
        fig.autofmt_xdate()
        return fig

    @output
    @render.ui
    def cjm_comp_table():
        s = stats()
        if s is None:
            return ui.HTML("<p>No data for selected period.</p>")

        df = pd.DataFrame(
            {
                "Metric": [
                    "Total Return (%)",
                    "Annualized Volatility (%)",
                    "Sharpe Ratio",
                    "Max Drawdown (%)",
                ],
                "Portfolio": [
                    s["total_ret_port"] * 100,
                    s["vol_port"] * 100,
                    s["sharpe_port"],
                    s["mdd_port"] * 100,
                ],
                "Benchmark": [
                    s["total_ret_bench"] * 100,
                    s["vol_bench"] * 100,
                    s["sharpe_bench"],
                    s["mdd_bench"] * 100,
                ],
                "Difference": [
                    (s["total_ret_port"] - s["total_ret_bench"]) * 100,
                    (s["vol_port"] - s["vol_bench"]) * 100,
                    s["sharpe_port"] - s["sharpe_bench"],
                    (s["mdd_port"] - s["mdd_bench"]) * 100,
                ],
            }
        )

        html = df.to_html(index=False, classes="table table-sm")
        return ui.HTML(html)