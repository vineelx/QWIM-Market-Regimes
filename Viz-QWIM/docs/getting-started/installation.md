# Installation

## System Requirements

!!! info "Prerequisites"
    - **Python 3.11+**: Core programming language
    - **Git**: Version control system
    - **uv**: Python package manager

## Installation Steps

### 1. Clone Repository

```bash
# Clone the QWIM Dashboard repository
git clone <repository-url>
cd dashboard-QWIM
```

### 2. Create Virtual Environment (Recommended)

```bash
# Install/upgrade pip and uv
python -m pip install --upgrade pip
python -m pip install --upgrade uv

# Create virtual environment using uv
uv init

# Activate virtual environment
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Since pyproject.toml contains all needed Python packages, just use "uv add" for one package
uv add polars

```

## Required Packages

The main dependencies include:

| Package | Version | Purpose |
|---------|---------|---------|
| `shiny` | Latest | Web framework for Python |
| `plotly` | Latest | Interactive visualizations |
| `polars` | Latest | High-performance time series and data processing |
| `pandas` | Latest | Data manipulation |
| `numpy` | Latest | Numerical computations |
| `shinyswatch` | Latest | Bootstrap themes |
| `great-tables` | Latest | Great looking static tables |
| `plotnine` | Latest | Great looking static plots (based on grammar of graphics, same as ggplot2 in R) |

## Verification

### Test Installation

```bash
# Verify Python version
python --version  # Should be 3.11+

# Test dashboard startup
shiny run --launch-browser src/dashboard/main_App.py
```

### Expected Output

```
🚀 Starting QWIM Dashboard...
📊 Environment: development
🐍 Python version: 3.11.x
💻 Platform: Windows 10
📁 Project directory: C:\path\to\dashboard-QWIM
🔧 Development mode: http://127.0.0.1:8080
```

## Troubleshooting

??? question "Python version error"
    Ensure you have Python 3.11 or higher installed:
    ```bash
    python --version
    ```

??? question "Package installation fails"
    Try upgrading pip first:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

??? question "Permission errors"
    Use virtual environment or install with user flag:
    ```bash
    pip install --user -r requirements.txt
    ```

## Next Steps

After successful installation:

1. [Configure your environment](configuration.md)
2. [Run the quick start guide](quickstart.md)
3. [Explore the user guide](../user-guide/overview.md)