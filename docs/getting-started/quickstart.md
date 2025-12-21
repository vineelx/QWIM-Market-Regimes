# Quick Start Guide

This guide will get you up and running with the QWIM Dashboard in minutes.

## 1. Start the Dashboard

### Development Mode (Default)

```bash
# Navigate to project directory
cd dashboard-QWIM

# Start development server
python src/dashboard/main_App.py
```

### Production Mode

```bash
# Set environment variable
export QWIM_ENVIRONMENT=production  # Linux/macOS
set QWIM_ENVIRONMENT=production     # Windows

# Start production server
python src/dashboard/main_App.py
```

## 2. Access the Dashboard

!!! success "Dashboard URLs"
    - **Development**: [http://127.0.0.1:8080](http://127.0.0.1:8080)
    - **Production**: [http://0.0.0.0:8000](http://0.0.0.0:8000)

## 3. First Steps

### Portfolio Analysis

1. **Navigate to QWIM Portfolios tab**
2. **Select time period** (1Y, 3Y, 5Y, 10Y, YTD, or Custom)
3. **Choose components** to analyze (default: first 3 ETFs)
4. **Select visualization type** (Area, Line, Bar, or Heatmap)

### Component Selection

=== "Default Selection"
    - First 3 ETF components are selected by default
    - Provides immediate analysis capability

=== "Custom Selection"
    - Check/uncheck individual ETF components
    - Use "Select All ETFs" for complete portfolio analysis
    - Real-time updates across all visualizations

=== "Statistical Analysis"
    - View weight statistics table
    - Latest, average, min, max, and standard deviation
    - Synchronized with selected components

## 4. Key Features Overview

### Interactive Visualizations

| Chart Type | Best For | Features |
|------------|----------|----------|
| **Stacked Area** | Portfolio composition over time | Cumulative view, easy proportion analysis |
| **Line Chart** | Individual component trends | Clear trend analysis, multiple series |
| **Stacked Bar** | Period comparisons | Discrete time points, easy comparison |
| **Heatmap** | Pattern identification | Color-coded intensity, correlation patterns |

### Time Period Selection

!!! tip "Time Period Options"
    - **1Y**: Last 12 months of data
    - **3Y**: Last 3 years for medium-term analysis
    - **5Y**: Default 5-year view for comprehensive analysis
    - **10Y**: Long-term historical perspective
    - **YTD**: Year-to-date analysis
    - **Custom**: Flexible date range selection

### Export Features

- **PNG Export**: Save plots as high-quality images
- **Table Export**: Export statistical summaries
- **Real-time Updates**: All exports reflect current selections

## 5. Example Workflow

### Analyze Portfolio Composition

1. **Start with default settings**
   ```
   - Time Period: Last 5 Years
   - Components: First 3 ETFs selected
   - Visualization: Stacked Area Chart
   ```

2. **Explore component selection**
   - Add 2 more components → View 5-component analysis
   - Use "Select All" → Full 12-component portfolio view

3. **Change visualization types**
   - Switch to Line Chart → See individual trends
   - Try Heatmap → Identify patterns and correlations

4. **Analyze different periods**
   - YTD → Current year performance
   - 10Y → Long-term historical trends
   - Custom → Focus on specific events

### Statistical Analysis

1. **Review Weight Statistics table**
   - Latest weights for current composition
   - Historical averages and volatility (StdDev)
   - Min/Max ranges for risk assessment

2. **Component comparison**
   - Select different component combinations
   - Compare statistical metrics
   - Identify high/low volatility components

## 6. Troubleshooting

??? question "Dashboard won't start"
    - Check Python version: `python --version` (need 3.11+)
    - Verify installation: `pip list | grep shiny`
    - Check project directory structure

??? question "No data visible"
    - Ensure data files are in correct locations
    - Check selected time period has data
    - Verify component selection (at least 1 selected)

??? question "Visualizations not updating"
    - Refresh browser page
    - Check browser console for errors
    - Verify component checkboxes are responsive

## Next Steps

Now that you have the dashboard running:

- [Learn about configuration options](configuration.md)
- [Explore "Portfolios" tab in QWIM dasHboard](../user-guide/tab-portfolios.md)
- [Explore "Investors" tab in QWIM dasHboard](../user-guide/tab-portfolios.md)
- [Understand data filtering](../user-guide/data-filtering.md)
- [Use export features](../user-guide/export.md)

!!! success "You're Ready!"
    The QWIM Dashboard is now running and ready for portfolio analysis. Explore the features and customize your analysis workflow!