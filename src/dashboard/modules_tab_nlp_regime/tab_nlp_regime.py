"""
Esen-NLP Regime Model Tab - Portfolio Comparison with Stock Selection
"""

from pathlib import Path
from shiny import ui, render, reactive
import pandas as pd
import numpy as np

# For standalone Viz-QWIM: data is in Viz-QWIM/data/
# For integrated setup: data is in parent Project_2_fe800/
viz_root = Path(__file__).parent.parent.parent.parent
if (viz_root / 'data').exists():
    # Standalone mode
    project_root = viz_root
else:
    # Integrated mode
    project_root = viz_root.parent

# Available stocks by sector
STOCK_UNIVERSE = {
    'Technology': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'NFLX', 'ADBE', 'CRM'],
    'Finance': ['JPM', 'BAC', 'WFC', 'GS', 'C', 'MS', 'BLK', 'SCHW', 'AXP', 'USB'],
    'Healthcare': ['JNJ', 'PFE', 'UNH', 'ABT', 'TMO', 'ABBV', 'LLY', 'MRK', 'BMY', 'AMGN'],
    'Consumer': ['WMT', 'HD', 'MCD', 'NKE', 'SBUX', 'TGT', 'LOW', 'COST', 'PG', 'KO'],
    'Industrial': ['BA', 'CAT', 'GE', 'HON', 'UPS', 'LMT', 'MMM', 'DE', 'RTX', 'UNP'],
    'Energy': ['XOM', 'CVX', 'SLB', 'COP', 'EOG', 'MPC', 'PSX', 'VLO', 'OXY', 'HAL']
}

# Flatten to single list
ALL_STOCKS = []
for stocks in STOCK_UNIVERSE.values():
    ALL_STOCKS.extend(stocks)


def tab_nlp_regime_ui():
    """UI with stock selection."""
    return ui.nav_panel(
        "Esen-NLP Regime Model",
        ui.page_fluid(
            ui.row(
                ui.column(
                    12,
                    ui.h2("📊 Custom Portfolio Builder"),
                    ui.hr()
                )
            ),
            
            # Stock Selector
            ui.row(
                ui.column(
                    12,
                    ui.card(
                        ui.card_header("🎯 Select Stocks for Portfolio", class_="bg-primary text-white"),
                        ui.row(
                            ui.column(
                                8,
                                ui.input_selectize(
                                    "selected_stocks",
                                    "Choose Stocks (default: 30 diverse stocks)",
                                    choices=ALL_STOCKS,
                                    selected=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'NFLX',
                                             'JPM', 'BAC', 'WFC', 'GS', 'C', 'MS',
                                             'JNJ', 'PFE', 'UNH', 'ABT', 'TMO', 'ABBV',
                                             'WMT', 'HD', 'MCD', 'NKE', 'SBUX', 'TGT',
                                             'BA', 'CAT', 'GE', 'HON'],
                                    multiple=True,
                                    options={'plugins': ['remove_button']}
                                )
                            ),
                            ui.column(
                                4,
                                ui.br(),
                                ui.input_action_button("run_backtest", "Run Backtest", class_="btn-success btn-lg")
                            )
                        )
                    )
                )
            ),
            
            ui.br(),
            
            # Results Display
            ui.row(
                ui.column(
                    12,
                    ui.output_ui("results_display")
                )
            ),
            
            ui.br(),
            
            # Plots
            ui.row(
                ui.column(
                    6,
                    ui.card(
                        ui.card_header("Regime Detection", class_="bg-success text-white"),
                        ui.output_ui("plot1")
                    )
                ),
                ui.column(
                    6,
                    ui.card(
                        ui.card_header("Portfolio Analysis", class_="bg-info text-white"),
                        ui.output_ui("plot2")
                    )
                )
            )
        )
    )


def tab_nlp_regime_server(input, output, session):
    """Server logic with dynamic backtesting."""
    
    # Reactive value to store backtest results
    backtest_results = reactive.Value(None)
    
    @reactive.Effect
    @reactive.event(input.run_backtest)
    def run_custom_backtest():
        """Run backtest with selected stocks."""
        selected = input.selected_stocks()
        
        if len(selected) < 2:
            backtest_results.set({'error': 'Please select at least 2 stocks'})
            return
        
        try:
            # Load price data
            data_path = project_root / 'data/cache/price_data_30tickers.parquet'
            prices = pd.read_parquet(data_path)
            
            # Filter to selected stocks
            prices = prices[prices.index.get_level_values('Ticker').isin(selected)]
            prices_pivot = prices[['Close']].reset_index().pivot(index='Date', columns='Ticker', values='Close')
            
            # Filter to 2024+
            prices_2024 = prices_pivot[prices_pivot.index >= '2024-01-01']
            
            # Calculate equal weight returns
            returns = prices_2024.pct_change().dropna()
            equal_returns = returns.mean(axis=1)
            port_cumulative = (1 + equal_returns).cumprod()
            
            # Calculate metrics
            port_return = (port_cumulative.iloc[-1] - 1) * 100
            port_sharpe = equal_returns.mean() / equal_returns.std() * np.sqrt(252)
            port_dd = ((port_cumulative / port_cumulative.expanding().max()) - 1).min() * 100
            port_vol = equal_returns.std() * np.sqrt(252) * 100
            
            # SPY comparison
            spy_path = project_root / 'data/cache/price_data_spy.parquet'
            spy_prices = pd.read_parquet(spy_path)
            spy_2024 = spy_prices[spy_prices.index.get_level_values('Date') >= '2024-01-01']
            spy_data = spy_2024.xs('SPY', level='Ticker')
            spy_return = (spy_data['Close'].iloc[-1] / spy_data['Close'].iloc[0] - 1) * 100
            spy_returns = spy_data['Close'].pct_change().dropna()
            spy_sharpe = spy_returns.mean() / spy_returns.std() * np.sqrt(252)
            
            backtest_results.set({
                'port_return': port_return,
                'port_sharpe': port_sharpe,
                'port_dd': port_dd,
                'port_vol': port_vol,
                'spy_return': spy_return,
                'spy_sharpe': spy_sharpe,
                'num_stocks': len(selected),
                'stocks': selected
            })
            
        except Exception as e:
            backtest_results.set({'error': str(e)})
    
    @output
    @render.ui
    def results_display():
        """Display backtest results."""
        results = backtest_results.get()
        
        if results is None:
            # Show default results
            try:
                df = pd.read_csv(project_root / 'data/portfolio_results/clean_comparison.csv')
                spy_ret = df[df['strategy'].str.contains('SPY')]['total_return'].iloc[0]
                port_ret = df[df['strategy'].str.contains('Equal')]['total_return'].iloc[0]
                spy_sharpe = df[df['strategy'].str.contains('SPY')]['sharpe_ratio'].iloc[0]
                port_sharpe = df[df['strategy'].str.contains('Equal')]['sharpe_ratio'].iloc[0]
                
                return ui.HTML(f"""
                <div class="alert alert-info">
                    <p><strong>Default Results (30 Stocks)</strong></p>
                    <p>Click "Run Backtest" to test your custom portfolio selection.</p>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card bg-success text-white mb-3">
                            <div class="card-body">
                                <h3>Default Portfolio (30)</h3>
                                <h1 class="display-4">+{port_ret:.2f}%</h1>
                                <p>Sharpe: {port_sharpe:.2f}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card bg-secondary text-white mb-3">
                            <div class="card-body">
                                <h3>SPY Benchmark</h3>
                                <h1 class="display-4">+{spy_ret:.2f}%</h1>
                                <p>Sharpe: {spy_sharpe:.2f}</p>
                            </div>
                        </div>
                    </div>
                </div>
                """)
            except:
                return ui.p("Click 'Run Backtest' to see results")
        
        if 'error' in results:
            return ui.HTML(f'<div class="alert alert-danger">Error: {results["error"]}</div>')
        
        # Display custom results
        port_ret = results['port_return']
        spy_ret = results['spy_return']
        port_sharpe = results['port_sharpe']
        spy_sharpe = results['spy_sharpe']
        num_stocks = results['num_stocks']
        
        outperformance = port_ret - spy_ret
        color = "success" if outperformance > 0 else "danger"
        symbol = "✅" if outperformance > 0 else "❌"
        
        return ui.HTML(f"""
        <div class="row">
            <div class="col-md-6">
                <div class="card bg-success text-white mb-3">
                    <div class="card-body">
                        <h3>Your Portfolio ({num_stocks} Stocks)</h3>
                        <h1 class="display-4">+{port_ret:.2f}%</h1>
                        <p>Sharpe: {port_sharpe:.2f}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card bg-secondary text-white mb-3">
                    <div class="card-body">
                        <h3>SPY Benchmark</h3>
                        <h1 class="display-4">+{spy_ret:.2f}%</h1>
                        <p>Sharpe: {spy_sharpe:.2f}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="alert alert-{color}">
            <h4>{symbol} Portfolio Outperformance: {outperformance:+.2f}%</h4>
            <p>Your {num_stocks}-stock equal-weight portfolio vs SPY.</p>
        </div>
        
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Strategy</th>
                    <th>Total Return</th>
                    <th>Sharpe Ratio</th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-success">
                    <td><strong>Your Portfolio ({num_stocks})</strong></td>
                    <td><strong>+{port_ret:.2f}%</strong></td>
                    <td>{port_sharpe:.2f}</td>
                </tr>
                <tr>
                    <td>SPY Benchmark</td>
                    <td>+{spy_ret:.2f}%</td>
                    <td>{spy_sharpe:.2f}</td>
                </tr>
            </tbody>
        </table>
        """)
    
    @output
    @render.ui
    def plot1():
        """Regime plot."""
        import base64
        try:
            plot_path = project_root / 'data/plots/1_regime_detection.png'
            with open(plot_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            return ui.HTML(f'<img src="data:image/png;base64,{img_data}" style="width: 100%;">')
        except:
            return ui.p("Plot not available")
    
    @output
    @render.ui
    def plot2():
        """Portfolio plot."""
        import base64
        try:
            plot_path = project_root / 'data/plots/2_portfolio_vs_spy_comprehensive.png'
            with open(plot_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            return ui.HTML(f'<img src="data:image/png;base64,{img_data}" style="width: 100%;">')
        except:
            return ui.p("Plot not available")
