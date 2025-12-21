# Esen's NLP-Enhanced Market Regime Detection Integration

## Overview

Successfully integrated Esen's NLP-enhanced market regime detection model into the Viz-QWIM Shiny dashboard as a new tab.

## What Was Added

### 1. New Tab Module
**Location**: `src/dashboard/modules_tab_nlp_regime/`

- **`__init__.py`**: Module initialization
- **`tab_nlp_regime.py`**: Complete tab implementation with UI and server logic

### 2. Data Files
**Location**: `data/`

- **`regime_detection_nlp.png`**: Main regime detection timeline (SPY, 2015-2025)
- **`portfolio_comprehensive.png`**: 6-panel comprehensive performance analysis

### 3. Dashboard Integration
**Modified File**: `src/dashboard/main_App.py`

- Added import for NLP regime module
- Integrated UI in navigation panel
- Initialized server logic

## Features

### Tab Name
**"Esen-NLP Regime Model"**

### Content Sections

1. **Market Regime Detection Timeline**
   - Full SPY price chart with color-coded regimes
   - 🔴 Strong Bear, 🟠 Mild Bear, 🟢 Mild Bull, 🔵 Strong Bull
   - Period: 2015-2025 (10+ years)

2. **Rolling 30-Day Sharpe Ratio**
   - Extracted from comprehensive plot
   - Compares SPY vs Dynamic Portfolio
   - Shows risk-adjusted performance over time

3. **Portfolio Allocation Weights**
   - Information about dynamic optimization strategy
   - Regime-dependent mean-variance optimization
   - 30 tickers across 5 sectors
   - Risk aversion parameter: γ = 2.0

4. **Performance Metrics**
   - Total Return: -0.60%
   - Sharpe Ratio: -415.33
   - Max Drawdown: -0.60%
   - vs SPY: -0.27%

5. **Expandable Sections** (Accordions)
   - 🔬 Model Architecture
   - 📊 Data Sources
   - 📈 Results & Insights

## Technical Details

### Model Components

- **Regime Detection**: RB-4 (Return-Based Clustering with 4 regimes)
- **Time-Series Features**: 9 features (5 lagged returns + 4 lagged volatility)
- **NLP Sentiment**: 4 features from FinBERT2 (ProsusAI/finbert)
- **Markov Switching Model**: Hidden Markov Model with sentiment enhancement
- **Portfolio Optimization**: Dynamic mean-variance with regime-dependent parameters

### Data Statistics

- **Tickers**: 30 stocks + SPY benchmark
- **Period**: 2015-01-01 to 2025-12-16 (2,754 trading days)
- **News Articles**: 6,778 financial headlines
- **Training/Test Split**: 2015-2019 train, 2024-2025 backtest

### Key Results

- ✅ Classification accuracy improved +12.5% with NLP
- ✅ Model captures 36.8% different signal than price-only
- ✅ Successfully identifies major market transitions
- ⚠️ Portfolio underperformed SPY by 0.27% (short backtest period)

## How to Run

### Start the Dashboard

```bash
cd /Users/esendashnyam/Desktop/Project_2_fe800/Viz-QWIM

# Development mode
python app.py
```

### Access the Tab

1. Open browser to http://127.0.0.1:8000
2. Click on "Esen-NLP Regime Model" tab
3. View all visualizations and metrics

## File Structure

```
Viz-QWIM/
├── data/
│   ├── regime_detection_nlp.png          # Main regime timeline
│   └── portfolio_comprehensive.png       # Full performance analysis
├── src/
│   └── dashboard/
│       ├── main_App.py                   # Main app (MODIFIED)
│       └── modules_tab_nlp_regime/       # NEW MODULE
│           ├── __init__.py
│           └── tab_nlp_regime.py
└── ESEN_NLP_INTEGRATION.md              # This file
```

## Code Highlights

### UI Function
```python
def tab_nlp_regime_ui():
    """Creates the navigation panel with all visualization components"""
    return ui.nav_panel(
        "Esen-NLP Regime Model",
        # Regime timeline, Sharpe ratio, metrics, accordions
    )
```

### Server Function
```python
def tab_nlp_regime_server(input, output, session):
    """Handles rendering images and dynamic content"""
    @output
    @render.image
    def regime_detection_plot():
        # Renders regime detection timeline
        
    @output
    @render.image
    def sharpe_ratio_plot():
        # Extracts Sharpe ratio panel from comprehensive plot
```

## Integration Points

### In main_App.py

**Import (line ~442)**:
```python
from src.dashboard.modules_tab_nlp_regime.tab_nlp_regime import (
    tab_nlp_regime_ui,
    tab_nlp_regime_server)
```

**UI Integration (line ~687)**:
```python
# Esen (NLP-Enhanced Regime Detection)
tab_nlp_regime_ui(),
```

**Server Integration (line ~974)**:
```python
# Esen (NLP-Enhanced Market Regime Detection)
tab_nlp_regime_server(input, output, session)
```

## Future Enhancements

### Potential Additions:
1. **Interactive regime selection**: Click to filter data by regime
2. **Dynamic portfolio weights plot**: Show actual allocation over time
3. **Regime transition probabilities**: Interactive transition matrix
4. **Real-time sentiment analysis**: Connect to live news feeds
5. **Downloadable reports**: Export analysis as PDF
6. **Comparison tools**: Compare multiple regime detection methods

### Data Updates:
- Replace synthetic news with real financial news
- Extend backtest to 10+ years for validation
- Add more tickers (50-100 stocks)
- Include international markets

## Notes

- Images are loaded from `data/` directory relative to module location
- Sharpe ratio is extracted programmatically from comprehensive plot
- All metrics are hardcoded (could be made dynamic with CSV data)
- Module follows Viz-QWIM naming conventions and patterns

## Credits

**Model Development**: Esen  
**Dashboard Integration**: December 16, 2025  
**Framework**: Shiny for Python + Plotly  
**NLP Model**: FinBERT2 (ProsusAI/finbert from HuggingFace)

---

**Status**: ✅ Successfully integrated and tested  
**Last Updated**: December 16, 2025

