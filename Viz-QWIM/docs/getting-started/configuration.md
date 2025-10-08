# Configuration

## Environment Variables

The QWIM Dashboard uses environment variables for configuration management.

### Core Environment Variables

| Variable | Default | Options | Description |
|----------|---------|---------|-------------|
| `QWIM_ENVIRONMENT` | `development` | `development`, `production` | Application environment mode |

### Environment-Specific Settings

=== "Development"
    ```bash
    # Default development settings
    QWIM_ENVIRONMENT=development
    ```
    
    **Features:**
    - Host: `127.0.0.1` (localhost only)
    - Port: `8080`
    - Debug mode: `False` (if True then detailed error messages)
    - Auto-reload: `False` (if rue then restart on code changes)

=== "Production"
    ```bash
    # Production environment
    export QWIM_ENVIRONMENT=production  # Linux/macOS
    set QWIM_ENVIRONMENT=production     # Windows
    ```
    
    **Features:**
    - Host: `0.0.0.0` (external access)
    - Port: `8000`
    - Debug mode: `False` (minimal error exposure)
    - Auto-reload: `False` (stable operation)

## Configuration Files

### Project Structure

```
dashboard-QWIM/
├── src/dashboard/
│   ├── main_App.py                 # Main application entry point
│   ├── modules_tab_portfolios/     # Portfolio analysis modules
│   └── utils_dashboard/            # Utility modules
├── inputs/                         # Data files location
├── logs/                           # Application logs
├── pyproject.toml                  # Project dependencies
└── mkdocs.yml                      # Documentation configuration
```

### Data Configuration

The dashboard expects data files in specific locations:

| Data Type | Expected Location | Format |
|-----------|------------------|---------|
| Portfolio Weights | `data/Weights_My_Portfolio.*` | Polars-compatible format |
| Time Series Data | `data/` directory | CSV, Parquet, Excel |

### Logging Configuration

!!! info "Logging Setup"
    - Log directory: `logs/` (created automatically)
    - Log files: Application-specific naming
    - Log levels: Environment-dependent

## Application Settings

### Performance Configuration

```python
# Data processing settings
MAX_POINTS_FOR_PLOTTING = 200      # Automatic downsampling threshold
ENABLE_PNG_SAVING = True           # Export functionality
DEFAULT_TIME_PERIOD = "5y"         # Default analysis period
DEFAULT_COMPONENTS_SELECTED = 3    # Default ETF selection count
```

### UI Configuration

```python
# User interface settings
DEFAULT_THEME = "flatly"           # Bootstrap theme
DEFAULT_CHART_TYPE = "area"        # Default visualization
ENABLE_RESPONSIVE_LAYOUT = True    # Mobile-friendly design
```

## Data Source Configuration

### Portfolio Data Requirements

!!! warning "Data Format Requirements"
    Portfolio weights data must include:
    
    - **Date column**: Date information (string or datetime format)
    - **Component columns**: 12 ETF weight columns
    - **Consistent naming**: Column names used for component selection
    - **Clean data**: No missing critical values

### Example Data Structure

```python
# Expected portfolio weights data structure
Date         | ETF_Component_1 | ETF_Component_2 | ... | ETF_Component_12
2020-01-01   | 0.083          | 0.075          | ... | 0.092
2020-01-02   | 0.085          | 0.073          | ... | 0.089
...          | ...            | ...            | ... | ...
```

## Customization Options

### Theme Customization

```python
# Available shinyswatch themes
themes = [
    "bootstrap",    # Classic Bootstrap
    "cerulean",     # Light blue theme
    "cosmo",        # Clean and modern
    "cyborg",       # Dark theme
    "darkly",       # Dark professional
    "flatly",       # Default - clean and modern
    "journal",      # Newspaper style
    "litera",       # Typography focused
    "lumen",        # Light and airy
    "lux",          # Luxury feel
    "materia",      # Material design
    "minty",        # Fresh green
    "morph",        # Soft shadows
    "pulse",        # Purple accent
    "quartz",       # Modern glass
    "sandstone",    # Warm earth tones
    "simplex",      # Minimal design
    "sketchy",      # Hand-drawn style
    "slate",        # Professional dark
    "solar",        # High contrast
    "spacelab",     # Clean and spacious
    "superhero",    # Comic book style
    "united",       # Corporate style
    "vapor",        # Retro cyberpunk
    "yeti",         # Clean minimalist
    "zephyr"        # Light and breezy
]
```

### Chart Configuration

```python
# Plotly chart settings
chart_config = {
    "area": {
        "stackgroup": "one",
        "mode": "lines",
        "fill": "tonexty"
    },
    "line": {
        "mode": "lines+markers",
        "marker_size": 4
    },
    "bar": {
        "barmode": "stack"
    },
    "heatmap": {
        "colorscale": "Viridis"
    }
}
```

## Security Configuration

### Development Security

!!! warning "Development Mode Security"
    - Debug mode enabled (detailed error messages)
    - Local access only (`127.0.0.1`)
    - Auto-reload enabled
    - **Not suitable for production use**

### Production Security

!!! success "Production Mode Security"
    - Debug mode disabled
    - External access enabled (`0.0.0.0`)
    - Stable operation (no auto-reload)
    - Minimal error information exposure

## Advanced Configuration

### Custom Data Paths

```python
# Override default data paths
import os
os.environ["QWIM_DATA_PATH"] = "/custom/data/path"
os.environ["QWIM_LOG_PATH"] = "/custom/log/path"
```

### Performance Tuning

```python
# Memory optimization
POLARS_MAX_THREADS = 4              # CPU thread usage
PANDAS_MEMORY_USAGE = "deep"        # Memory profiling
PLOTLY_RENDERER = "browser"         # Rendering engine
```

## Validation and Testing

### Configuration Validation

```bash
# Test configuration
python -c "
from src.dashboard.utils_dashboard.utils_data import get_data_utils
data_utils = get_data_utils()
print('Configuration valid!')
"
```

### Environment Testing

```bash
# Test development environment
QWIM_ENVIRONMENT=development python src/dashboard/main_App.py

# Test production environment  
QWIM_ENVIRONMENT=production python src/dashboard/main_App.py
```

## Troubleshooting

??? question "Configuration not loading"
    - Check environment variable syntax
    - Verify file permissions
    - Check project directory structure

??? question "Data not found"
    - Verify data file locations
    - Check file naming conventions
    - Ensure proper file formats

??? question "Port conflicts"
    - Development port 8080 may be in use
    - Production port 8000 may be in use
    - Check running processes: `netstat -an | grep :8080`

## Next Steps

After configuration:

1. [Start the dashboard](quickstart.md)
2. [Learn about dashboard tab "Portfolios"](../user-guide/tab-portfolios.md)
3. [Learn about dashboard tab "Investors"](../user-guide/tab-investors.md)
4. [Explore deployment options](../deployment/local.md)