# Local Deployment

This guide provides comprehensive instructions for deploying the QWIM Dashboard in a local development environment.

## Prerequisites

### System Requirements

!!! info "Development Environment Requirements"
    - **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18+)
    - **Python**: Version 3.11 or higher
    - **Memory**: Minimum 4GB RAM (8GB recommended for large datasets)
    - **Storage**: At least 1GB free space for installation and data
    - **Network**: Internet connection for package installation

### Required Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| **Python** | 3.11+ | Core runtime | [python.org](https://python.org) |
| **Git** | Latest | Version control | [git-scm.com](https://git-scm.com) |
| **pip** | Latest | Package manager | Included with Python |

### Development Tools (Recommended)

```bash
# Recommended development tools
pip install --upgrade pip setuptools wheel
pip install virtualenv  # For virtual environment management
```

## Installation Steps

### 1. Clone Repository

```bash
# Clone the QWIM Dashboard repository
git clone https://github.com/your-org/dashboard-QWIM.git
cd dashboard-QWIM

# Verify repository structure
ls -la
```

Expected directory structure:
```
dashboard-QWIM/
├── src/dashboard/          # Main application source
├── data/                   # Data files directory
├── docs/                   # Documentation
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
├── requirements-docs.txt   # Documentation dependencies
├── mkdocs.yml             # Documentation configuration
└── README.md              # Project overview
```

### 2. Create Virtual Environment

!!! tip "Virtual Environment Best Practice"
    Using a virtual environment isolates project dependencies and prevents conflicts.

=== "Windows"
    ```cmd
    # Create virtual environment
    python -m venv qwim_dashboard_env
    
    # Activate virtual environment
    qwim_dashboard_env\Scripts\activate
    
    # Verify activation (should show virtual environment name)
    echo %VIRTUAL_ENV%
    ```

=== "macOS/Linux"
    ```bash
    # Create virtual environment
    python3 -m venv qwim_dashboard_env
    
    # Activate virtual environment
    source qwim_dashboard_env/bin/activate
    
    # Verify activation (should show virtual environment name)
    echo $VIRTUAL_ENV
    ```

### 3. Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install core application dependencies
pip install -r requirements.txt

# Install documentation dependencies (optional)
pip install -r requirements-docs.txt

# Install development/testing dependencies (optional)
pip install pytest pytest-cov pytest-mock black flake8
```

### 4. Verify Installation

```bash
# Check Python version
python --version
# Expected: Python 3.11.x or higher

# Check installed packages
pip list | grep -E "(shiny|plotly|polars|pandas)"

# Verify core packages
python -c "
import shiny
import plotly
import polars as pl
import pandas as pd
print('All core packages imported successfully!')
"
```

## Configuration

### Environment Configuration

Create environment configuration file:

```bash
# Create .env file for local configuration (optional)
cat > .env << 'EOF'
QWIM_ENVIRONMENT=development
QWIM_DEBUG=true
QWIM_LOG_LEVEL=INFO
EOF
```

### Data Setup

!!! warning "Data Requirements"
    The dashboard requires portfolio weights data to function properly.

#### Option 1: Use Sample Data (Recommended for Testing)

```bash
# Create sample data directory
mkdir -p data

# Generate sample portfolio data (if available)
python -c "
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample portfolio weights data
np.random.seed(42)
dates = pd.date_range('2020-01-01', '2024-01-01', freq='D')
data = {'Date': dates}

# Create 12 sample ETF components
for i in range(1, 13):
    component_name = f'Component_{i:02d}'
    base_weight = 0.083 + (i - 6.5) * 0.001
    noise = np.random.normal(0, base_weight * 0.03, len(dates))
    weights = np.maximum(base_weight + noise, 0.001)
    data[component_name] = weights

portfolio_df = pd.DataFrame(data)
portfolio_df.to_csv('data/Weights_My_Portfolio.csv', index=False)
print('Sample portfolio data created successfully!')
"
```

#### Option 2: Use Real Data

```bash
# Place your portfolio data files in the data directory
# Supported formats: CSV, Excel, Parquet
cp your_portfolio_data.csv data/Weights_My_Portfolio.csv

# Verify data format
python -c "
import pandas as pd
data = pd.read_csv('data/Weights_My_Portfolio.csv')
print('Data shape:', data.shape)
print('Columns:', list(data.columns))
print('First few rows:')
print(data.head())
"
```

### Application Configuration

The dashboard uses default configuration suitable for local development:

```python
# Default local development settings
DEFAULT_SETTINGS = {
    "environment": "development",
    "host": "127.0.0.1",
    "port": 8080,
    "debug": True,
    "reload": True,
    "max_points_plotting": 200,
    "enable_png_saving": True,
    "default_time_period": "5y"
}
```

## Running the Application

### Standard Development Mode

```bash
# Ensure virtual environment is activated
# Windows: qwim_dashboard_env\Scripts\activate
# macOS/Linux: source qwim_dashboard_env/bin/activate

# Navigate to project directory
cd dashboard-QWIM

# Start the dashboard in development mode
python src/dashboard/main_App.py
```

Expected output:
```
🚀 Starting QWIM Dashboard...
📊 Environment: development
🐍 Python version: 3.11.x
💻 Platform: Windows 10 / macOS / Linux
📁 Project directory: /path/to/dashboard-QWIM
🔧 Development mode: http://127.0.0.1:8080
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

### Custom Port Configuration

```bash
# Run on different port (if 8080 is in use)
# Modify main_App.py or use environment variable
QWIM_PORT=8081 python src/dashboard/main_App.py

# Or edit the port in main_App.py:
# app.run(host="127.0.0.1", port=8081, debug=True, reload=True)
```

### Background Execution

```bash
# Run in background (Linux/macOS)
nohup python src/dashboard/main_App.py > dashboard.log 2>&1 &

# Run in background (Windows)
start /B python src/dashboard/main_App.py > dashboard.log 2>&1
```

## Accessing the Dashboard

### Web Interface

Once the application is running:

1. **Open web browser**
2. **Navigate to**: [http://127.0.0.1:8080](http://127.0.0.1:8080)
3. **Verify loading**: Should see QWIM Dashboard interface

### First-Time Setup

!!! success "Initial Dashboard Setup"
    1. **Navigate to QWIM Portfolios tab** (should be default)
    2. **Verify data loading**: Check for component selection checkboxes
    3. **Test functionality**: Try changing time period and components
    4. **Check visualizations**: Ensure charts render properly

### Feature Verification

=== "Component Selection"
    - [ ] Default 3 components selected
    - [ ] Individual checkboxes functional
    - [ ] "Select All ETFs" toggle works
    - [ ] Component count displays correctly

=== "Time Period Selection"
    - [ ] Dropdown shows all options (1Y, 3Y, 5Y, 10Y, YTD, Custom)
    - [ ] Default 5Y period selected
    - [ ] Custom date range picker functional
    - [ ] Charts update when period changes

=== "Visualizations"
    - [ ] Main chart displays (default: Stacked Area)
    - [ ] Chart type selector functional (Area, Line, Bar, Heatmap)
    - [ ] Composition pie chart shows
    - [ ] Statistics table populates

=== "Interactive Features"
    - [ ] Chart zoom and pan functional
    - [ ] Hover tooltips display
    - [ ] Percentage toggle works
    - [ ] Sort components option functional

## Development Workflow

### File Watching and Auto-Reload

The development server automatically reloads when files change:

```bash
# Start with auto-reload (default in development)
python src/dashboard/main_App.py

# Monitor file changes
# The server will automatically restart when you modify:
# - src/dashboard/*.py files
# - Template files
# - Configuration files
```

### Development Tools Integration

#### VS Code Integration

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "QWIM Dashboard",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/dashboard/main_App.py",
            "env": {
                "QWIM_ENVIRONMENT": "development"
            },
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

#### PyCharm Integration

```python
# Run configuration in PyCharm
# Script path: /path/to/dashboard-QWIM/src/dashboard/main_App.py
# Working directory: /path/to/dashboard-QWIM
# Environment variables: QWIM_ENVIRONMENT=development
```

### Debugging

#### Enable Debug Mode

```python
# In main_App.py, debug mode is enabled by default for development
if ENVIRONMENT == "development":
    app.run(host="127.0.0.1", port=8080, debug=True, reload=True)
```

#### Debug Configuration

```python
# Enhanced debugging with detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints in your code
def debug_component_selection():
    """Debug helper for component selection issues."""
    print("=== Component Selection Debug ===")
    available_components = get_available_etf_components()
    print(f"Available components: {available_components}")
    
    selected_components = get_selected_etf_components()
    print(f"Selected components: {selected_components}")
```

### Testing in Development

```bash
# Run test suite
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/unit/ -v                    # Unit tests
python -m pytest tests/integration/ -v             # Integration tests
python -m pytest tests/performance/ -v             # Performance tests

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Generate coverage report
open htmlcov/index.html  # View coverage report
```

## Troubles<!-- filepath: c:\Copilota\dashboard-QWIM\docs\deployment\local.md -->
# Local Deployment

This guide provides comprehensive instructions for deploying the QWIM Dashboard in a local development environment.

## Prerequisites

### System Requirements

!!! info "Development Environment Requirements"
    - **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18+)
    - **Python**: Version 3.11 or higher
    - **Memory**: Minimum 4GB RAM (8GB recommended for large datasets)
    - **Storage**: At least 1GB free space for installation and data
    - **Network**: Internet connection for package installation

### Required Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| **Python** | 3.11+ | Core runtime | [python.org](https://python.org) |
| **Git** | Latest | Version control | [git-scm.com](https://git-scm.com) |
| **pip** | Latest | Package manager | Included with Python |

### Development Tools (Recommended)

```bash
# Recommended development tools
pip install --upgrade pip setuptools wheel
pip install virtualenv  # For virtual environment management
```

## Installation Steps

### 1. Clone Repository

```bash
# Clone the QWIM Dashboard repository
git clone https://github.com/your-org/dashboard-QWIM.git
cd dashboard-QWIM

# Verify repository structure
ls -la
```

Expected directory structure:
```
dashboard-QWIM/
├── src/dashboard/          # Main application source
├── data/                   # Data files directory
├── docs/                   # Documentation
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
├── requirements-docs.txt   # Documentation dependencies
├── mkdocs.yml             # Documentation configuration
└── README.md              # Project overview
```

### 2. Create Virtual Environment

!!! tip "Virtual Environment Best Practice"
    Using a virtual environment isolates project dependencies and prevents conflicts.

=== "Windows"
    ```cmd
    # Create virtual environment
    python -m venv qwim_dashboard_env
    
    # Activate virtual environment
    qwim_dashboard_env\Scripts\activate
    
    # Verify activation (should show virtual environment name)
    echo %VIRTUAL_ENV%
    ```

=== "macOS/Linux"
    ```bash
    # Create virtual environment
    python3 -m venv qwim_dashboard_env
    
    # Activate virtual environment
    source qwim_dashboard_env/bin/activate
    
    # Verify activation (should show virtual environment name)
    echo $VIRTUAL_ENV
    ```

### 3. Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install core application dependencies
pip install -r requirements.txt

# Install documentation dependencies (optional)
pip install -r requirements-docs.txt

# Install development/testing dependencies (optional)
pip install pytest pytest-cov pytest-mock black flake8
```

### 4. Verify Installation

```bash
# Check Python version
python --version
# Expected: Python 3.11.x or higher

# Check installed packages
pip list | grep -E "(shiny|plotly|polars|pandas)"

# Verify core packages
python -c "
import shiny
import plotly
import polars as pl
import pandas as pd
print('All core packages imported successfully!')
"
```

## Configuration

### Environment Configuration

Create environment configuration file:

```bash
# Create .env file for local configuration (optional)
cat > .env << 'EOF'
QWIM_ENVIRONMENT=development
QWIM_DEBUG=true
QWIM_LOG_LEVEL=INFO
EOF
```

### Data Setup

!!! warning "Data Requirements"
    The dashboard requires portfolio weights data to function properly.

#### Option 1: Use Sample Data (Recommended for Testing)

```bash
# Create sample data directory
mkdir -p data

# Generate sample portfolio data (if available)
python -c "
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample portfolio weights data
np.random.seed(42)
dates = pd.date_range('2020-01-01', '2024-01-01', freq='D')
data = {'Date': dates}

# Create 12 sample ETF components
for i in range(1, 13):
    component_name = f'Component_{i:02d}'
    base_weight = 0.083 + (i - 6.5) * 0.001
    noise = np.random.normal(0, base_weight * 0.03, len(dates))
    weights = np.maximum(base_weight + noise, 0.001)
    data[component_name] = weights

portfolio_df = pd.DataFrame(data)
portfolio_df.to_csv('data/Weights_My_Portfolio.csv', index=False)
print('Sample portfolio data created successfully!')
"
```

#### Option 2: Use Real Data

```bash
# Place your portfolio data files in the data directory
# Supported formats: CSV, Excel, Parquet
cp your_portfolio_data.csv data/Weights_My_Portfolio.csv

# Verify data format
python -c "
import pandas as pd
data = pd.read_csv('data/Weights_My_Portfolio.csv')
print('Data shape:', data.shape)
print('Columns:', list(data.columns))
print('First few rows:')
print(data.head())
"
```

### Application Configuration

The dashboard uses default configuration suitable for local development:

```python
# Default local development settings
DEFAULT_SETTINGS = {
    "environment": "development",
    "host": "127.0.0.1",
    "port": 8080,
    "debug": True,
    "reload": True,
    "max_points_plotting": 200,
    "enable_png_saving": True,
    "default_time_period": "5y"
}
```

## Running the Application

### Standard Development Mode

```bash
# Ensure virtual environment is activated
# Windows: qwim_dashboard_env\Scripts\activate
# macOS/Linux: source qwim_dashboard_env/bin/activate

# Navigate to project directory
cd dashboard-QWIM

# Start the dashboard in development mode
python src/dashboard/main_App.py
```

Expected output:
```
🚀 Starting QWIM Dashboard...
📊 Environment: development
🐍 Python version: 3.11.x
💻 Platform: Windows 10 / macOS / Linux
📁 Project directory: /path/to/dashboard-QWIM
🔧 Development mode: http://127.0.0.1:8080
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

### Custom Port Configuration

```bash
# Run on different port (if 8080 is in use)
# Modify main_App.py or use environment variable
QWIM_PORT=8081 python src/dashboard/main_App.py

# Or edit the port in main_App.py:
# app.run(host="127.0.0.1", port=8081, debug=True, reload=True)
```

### Background Execution

```bash
# Run in background (Linux/macOS)
nohup python src/dashboard/main_App.py > dashboard.log 2>&1 &

# Run in background (Windows)
start /B python src/dashboard/main_App.py > dashboard.log 2>&1
```

## Accessing the Dashboard

### Web Interface

Once the application is running:

1. **Open web browser**
2. **Navigate to**: [http://127.0.0.1:8080](http://127.0.0.1:8080)
3. **Verify loading**: Should see QWIM Dashboard interface

### First-Time Setup

!!! success "Initial Dashboard Setup"
    1. **Navigate to QWIM Portfolios tab** (should be default)
    2. **Verify data loading**: Check for component selection checkboxes
    3. **Test functionality**: Try changing time period and components
    4. **Check visualizations**: Ensure charts render properly

### Feature Verification

=== "Component Selection"
    - [ ] Default 3 components selected
    - [ ] Individual checkboxes functional
    - [ ] "Select All ETFs" toggle works
    - [ ] Component count displays correctly

=== "Time Period Selection"
    - [ ] Dropdown shows all options (1Y, 3Y, 5Y, 10Y, YTD, Custom)
    - [ ] Default 5Y period selected
    - [ ] Custom date range picker functional
    - [ ] Charts update when period changes

=== "Visualizations"
    - [ ] Main chart displays (default: Stacked Area)
    - [ ] Chart type selector functional (Area, Line, Bar, Heatmap)
    - [ ] Composition pie chart shows
    - [ ] Statistics table populates

=== "Interactive Features"
    - [ ] Chart zoom and pan functional
    - [ ] Hover tooltips display
    - [ ] Percentage toggle works
    - [ ] Sort components option functional

## Development Workflow

### File Watching and Auto-Reload

The development server automatically reloads when files change:

```bash
# Start with auto-reload (default in development)
python src/dashboard/main_App.py

# Monitor file changes
# The server will automatically restart when you modify:
# - src/dashboard/*.py files
# - Template files
# - Configuration files
```

### Development Tools Integration

#### VS Code Integration

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "QWIM Dashboard",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/dashboard/main_App.py",
            "env": {
                "QWIM_ENVIRONMENT": "development"
            },
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

#### PyCharm Integration

```python
# Run configuration in PyCharm
# Script path: /path/to/dashboard-QWIM/src/dashboard/main_App.py
# Working directory: /path/to/dashboard-QWIM
# Environment variables: QWIM_ENVIRONMENT=development
```

### Debugging

#### Enable Debug Mode

```python
# In main_App.py, debug mode is enabled by default for development
if ENVIRONMENT == "development":
    app.run(host="127.0.0.1", port=8080, debug=True, reload=True)
```

#### Debug Configuration

```python
# Enhanced debugging with detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints in your code
def debug_component_selection():
    """Debug helper for component selection issues."""
    print("=== Component Selection Debug ===")
    available_components = get_available_etf_components()
    print(f"Available components: {available_components}")
    
    selected_components = get_selected_etf_components()
    print(f"Selected components: {selected_components}")
```

### Testing in Development

```bash
# Run test suite
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/unit/ -v                    # Unit tests
python -m pytest tests/integration/ -v             # Integration tests
python -m pytest tests/performance/ -v             # Performance tests

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Generate coverage report
open htmlcov/index.html  # View coverage report
```

## Troubles