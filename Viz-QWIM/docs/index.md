# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

-   `mkdocs new [dir-name]` - Create a new project.
-   `mkdocs serve` - Start the live-reloading docs server.
-   `mkdocs build` - Build the documentation site.
-   `mkdocs -h` - Print help message and exit.

## Project layout

```         
mkdocs.yml    # The configuration file.
docs/
    index.md  # The documentation homepage.
    ...       # Other markdown pages, images and other files.
```

# QWIM Dashboard Documentation

Welcome to the QWIM Dashboard documentation. This dashboard provides comprehensive portfolio analysis and management capabilities.

## Overview

The QWIM Dashboard is a web-based application built with Python and Shiny that offers:

-   **Portfolio Analysis**: Detailed performance metrics and analytics
-   **Portfolio Comparison**: Side-by-side comparison with benchmarks
-   **Weights Distribution**: Interactive visualization of portfolio components
-   **Export Capabilities**: PNG export functionality for charts and reports

## Quick Start

To get started with the QWIM Dashboard:

1.  Install the required dependencies
2.  Configure your portfolio data
3.  Launch the dashboard application
4.  Navigate through the portfolio analysis tabs

## Architecture

The dashboard follows a modular architecture with specialized components:

-   `tab_portfolios.py`: Portfolios tab
    -   `subtab_portfolios_analysis.py`: Individual portfolio analysis
    -   `subtab_portfolios_comparison.py`: Portfolio comparison functionality
    -   `subtab_weights_distribution.py`: Weights visualization
-   `tab_investors.py`: Investor(s) tab
    -   `subtab_investors_personal_infos.py`: Personal information for investor(s)
    -   `subtab_investors_assets.py`: Assets of investor(s)
    -   `subtab_investors_goals.py`: Goals of investor(s)
    -   `subtab_investors_income.py`: Income of investor(s)

## Reference

For detailed documentation on functions and modules, see the [Reference](reference/main.md) section.

## Key Features

### Portfolio Management

-   Comprehensive portfolio analysis tools
-   Real-time performance tracking
-   Risk assessment capabilities

### Data Visualization

-   Interactive charts and graphs
-   Customizable dashboards
-   Export functionality for presentations

### Comparison Tools

-   Benchmark comparisons
-   Historical performance analysis
-   Relative performance metrics

### Investors information

-   Personal information
-   Assets
-   Goals
-   Income

## Getting Help

-   **User Guide**: Step-by-step instructions for using the dashboard
-   **Reference**: Complete documentation of all functions and modules
-   **Development**: Guidelines for contributing to the project

## Navigation

Use the navigation menu to explore:

-   [Getting Started](getting-started/installation.md) - Installation and initial setup
-   [User Guide](user-guide/overview.md) - How to use the dashboard features
-   [Reference](reference/main.md) - Documentation on functions and modules
-   [Development](development/contributing.md) - Contributing guidelines
