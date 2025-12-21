# Contributing Guide

Welcome to the QWIM Dashboard project! This guide will help you contribute effectively while following our coding standards and best practices.

## Getting Started

### Prerequisites

!!! info "Development Requirements"
    - **Python 3.11+**: Core programming language
    - **Git**: Version control system
    - **Virtual Environment**: Recommended for isolation
    - **Code Editor**: VS Code recommended with Python extensions

### Development Setup

#### Clone the QWIM Dashboard repository
git clone <repository-url>
cd dashboard-QWIM

#### Install/upgrade pip and uv
python -m pip install --upgrade pip
python -m pip install --upgrade uv

#### Create virtual environment using uv
uv init

#### Activate virtual environment
##### Windows
.venv\Scripts\activate

###### macOS/Linux
source .venv/bin/activate

#### Since pyproject.toml contains all needed Python packages, just use "uv add" for one package
uv add polars

##### Install pre-commit hooks (if available)
pre-commit install
```

## Project Coding Standards

### Naming Conventions

Following our established naming standards:

#### Variable and Function Names

```python
# Use snake_case for variables and functions
portfolio_weight_data = get_portfolio_weights()
selected_component_count = len(selected_components)

def calculate_weight_statistics():
    """Calculate statistical metrics for portfolio weights."""
    pass

def get_filtered_weights_dataframe():
    """Get filtered weights DataFrame with selected components."""
    pass
```

#### Class Names

```python
# Use CamelCase for class names
class PortfolioAnalyzer:
    """Main portfolio analysis class."""
    pass

class DataProcessor:
    """Handles data processing operations."""
    pass
```

#### Constants

```python
# Use UPPERCASE for constants
MAX_POINTS_FOR_PLOTTING = 200
DEFAULT_TIME_PERIOD = "5y"
ENABLE_PNG_SAVING_SUBTAB_WEIGHTS_DISTRIBUTION = True
```

#### Shiny Component Identifiers

```python
# Input components
input_ID_tab_portfolios_subtab_weights_distribution_time_period
input_ID_tab_portfolios_subtab_weights_distribution_component_selection

# Output components  
output_ID_tab_portfolios_subtab_weights_distribution_plot_main
output_ID_tab_portfolios_subtab_weights_distribution_statistics_table
```

#### Data Structure Names

```python
# Use snake_case with uppercase first letters for elements
weights_dataframe_filtered = {
    "Component_One": [0.083, 0.085, 0.082],
    "Component_Two": [0.075, 0.073, 0.078],
    "Date_Values": ["2024-01-01", "2024-01-02", "2024-01-03"]
}

# Reactive dictionaries
reactives_shiny = {
    "Table_One_Summary_Data": reactive_value,
    "Plot_Two_Summary_Data": reactive_value,
    "Input_Tab_Portfolios_Selected_Components": reactive_value
}
```

#### Function coding standards

Two empty rows before each function definition
When a function has at least 2 input arguments, the function signature needs to have only one input argument per row, starting with second row after function name. 
Comprehensive docstring documentation and commenting, consistent with Python package mkdocs-material content, formats and style.
Type hints for all parameters and return values
Use input validation (with early returns), configuration validation, business logic validation and defensive programming as the primary approach, with try-except reserved for truly unpredictable operations.

```python
def first_function():
    """First function with proper spacing."""
    pass


def second_function():
    """Second function with two empty rows before definition."""
    pass


class ExampleClass:
    """Example class following standards."""
    
    def __init__(self):
        pass


    def method_one(self):
        """Method with proper spacing."""
        pass


    def method_two(self):
        """Another method with proper spacing."""
        pass
```

### Python Coding Standards

#### Input Validation and Defensive Programming

```python
def process_portfolio_data(weights_dataframe, selected_components, time_period):
    """
    Process portfolio data with comprehensive validation.
    
    Args:
        weights_dataframe: Portfolio weights data
        selected_components: List of selected ETF components  
        time_period: Analysis time period
        
    Returns:
        dict: Processed portfolio data
        
    Raises:
        ValueError: If input validation fails
    """
    # Input validation with early returns
    if weights_dataframe is None or weights_dataframe.empty:
        return {}
    
    if not selected_components or len(selected_components) == 0:
        return {}
        
    if not time_period or time_period not in ["1y", "3y", "5y", "10y", "ytd", "custom"]:
        time_period = "5y"  # Default fallback
    
    # Configuration validation
    required_columns = ["Date"] + selected_components
    missing_columns = [col for col in required_columns if col not in weights_dataframe.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Business logic validation
    date_column = weights_dataframe["Date"]
    if date_column.isnull().any():
        weights_dataframe = weights_dataframe.dropna(subset=["Date"])
    
    # Defensive programming - handle edge cases
    if len(weights_dataframe) == 0:
        return {}
    
    # Process data safely
    try:
        # Only use try-except for truly unpredictable operations
        processed_data = weights_dataframe[required_columns].copy()
        return {"data": processed_data, "status": "success"}
    except Exception as exc:
        # Last resort error handling
        raise RuntimeError(f"Unexpected error in data processing: {exc}")
```

#### Error Handling Philosophy

```python
# Preferred: Input validation and defensive programming
def calculate_statistics(data_values):
    """Calculate statistics with defensive programming."""
    # Input validation
    if not data_values or len(data_values) == 0:
        return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}
    
    # Convert to numeric, handle non-numeric values
    numeric_values = []
    for value_item in data_values:
        try:
            numeric_value = float(value_item)
            if not np.isnan(numeric_value) and not np.isinf(numeric_value):
                numeric_values.append(numeric_value)
        except (ValueError, TypeError):
            continue  # Skip non-numeric values
    
    # Defensive programming
    if len(numeric_values) == 0:
        return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}
    
    # Safe calculations
    mean_value = np.mean(numeric_values)
    std_value = np.std(numeric_values) if len(numeric_values) > 1 else 0.0
    min_value = np.min(numeric_values)
    max_value = np.max(numeric_values)
    
    return {
        "mean": float(mean_value),
        "std": float(std_value), 
        "min": float(min_value),
        "max": float(max_value)
    }

# Avoid: Excessive try-except blocks
def calculate_statistics_avoid(data_values):
    """Avoid this pattern - too much try-except."""
    try:
        try:
            mean_value = np.mean(data_values)
        except:
            mean_value = 0.0
        try:
            std_value = np.std(data_values)
        except:
            std_value = 0.0
        return {"mean": mean_value, "std": std_value}
    except:
        return {}
```

### Shiny-Specific Standards

#### Reactive Value Access

```python
# Correct: Access reactive values with proper syntax
@reactive.calc
def get_selected_components():
    """Get selected components from Shiny inputs."""
    # Access reactive input values
    select_all = input.input_ID_tab_portfolios_subtab_weights_distribution_select_all_components()
    time_period = input.input_ID_tab_portfolios_subtab_weights_distribution_time_period()
    
    # Process reactive values
    if select_all:
        return get_all_available_components()
    
    selected_components = []
    for component_name in get_available_components():
        checkbox_name = f"input_ID_tab_portfolios_subtab_weights_distribution_component_{component_name}"
        checkbox_value = getattr(input, checkbox_name, lambda: False)()
        if checkbox_value:
            selected_components.append(component_name)
    
    return selected_components


# Correct: Output assignment
@output
@render.plot
def output_ID_tab_portfolios_subtab_weights_distribution_plot_main():
    """Render main portfolio weights plot."""
    return generate_portfolio_plot()
```

## Contributing Workflow

### Development Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow Coding Standards**
   - Use established naming conventions
   - Implement input validation and defensive programming
   - Add comprehensive documentation
   - Include type hints

3. **Write Tests**
   ```python
   # test_portfolio_analysis.py
   def test_calculate_weight_statistics():
       """Test weight statistics calculation."""
       # Test data
       test_data = [0.083, 0.085, 0.082, 0.088, 0.079]
       
       # Calculate statistics
       result = calculate_weight_statistics(test_data)
       
       # Assertions
       assert "mean" in result
       assert "std" in result
       assert isinstance(result["mean"], float)
       assert result["mean"] > 0
   ```

4. **Documentation Requirements**
   - Comprehensive docstring documentation and commenting, consistent with Python package mkdocs-material content, formats and style.
   - Type hints for all parameters
   - Usage examples where helpful
   - Update API documentation if needed

5. **Code Review Checklist**
   - [ ] Follows naming conventions
   - [ ] Uses input validation over try-except
   - [ ] Includes comprehensive documentation
   - [ ] Has appropriate tests
   - [ ] Maintains performance standards

### Pull Request Guidelines

#### PR Title Format

```
[Category] Brief description

Categories:
- feat: New feature
- fix: Bug fix  
- docs: Documentation changes
- refactor: Code refactoring
- test: Test additions/changes
- perf: Performance improvements
```

#### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Performance testing (if applicable)

## Documentation
- [ ] Code comments updated
- [ ] API documentation updated
- [ ] User guide updated (if applicable)

## Checklist
- [ ] Code follows project standards
- [ ] Input validation implemented
- [ ] Defensive programming used
- [ ] Type hints included
- [ ] Documentation complete
```

## Code Quality Standards

### Documentation Requirements

```python
def analyze_portfolio_performance(
    weights_dataframe: pd.DataFrame,
    selected_components: list[str], 
    time_period: str,
    analysis_type: str = "standard"
) -> dict[str, typing.Any]:
    """
    Analyze portfolio performance for selected components and time period.
    
    Performs comprehensive analysis including statistical calculations,
    trend analysis, and risk assessment for the specified portfolio
    components over the given time period.
    
    Args:
        weights_dataframe: Portfolio weights data with Date column and component columns
        selected_components: List of ETF component names to analyze  
        time_period: Analysis period ("1y", "3y", "5y", "10y", "ytd", "custom")
        analysis_type: Type of analysis ("standard", "detailed", "risk_focused")
        
    Returns:
        Dictionary containing:
            - "statistics": Statistical metrics for each component
            - "trends": Trend analysis results
            - "risk_metrics": Risk assessment data
            - "status": Analysis completion status
            
    Raises:
        ValueError: If weights_dataframe is empty or invalid
        KeyError: If required columns are missing from dataframe
        
    Example:
        ```python
        weights_df = load_portfolio_data()
        components = ["Component_One", "Component_Two"]
        results = analyze_portfolio_performance(
            weights_dataframe=weights_df,
            selected_components=components,
            time_period="5y"
        )
        ```
        
    Notes:
        - Uses defensive programming for robust error handling
        - Automatically handles missing data and edge cases
        - Performance optimized for large datasets through downsampling
    """
    # Implementation follows...
```

### Testing Standards

```python
# test_portfolio_module.py
import pytest
import pandas as pd
import numpy as np
from src.dashboard.modules_tab_portfolios.subtab_weights_distribution import (
    calculate_weight_statistics,
    get_filtered_weights_dataframe,
    analyze_portfolio_performance
)


class TestPortfolioAnalysis:
    """Test suite for portfolio analysis functionality."""
    
    
    def setup_method(self):
        """Set up test data for each test method."""
        self.test_weights_data = pd.DataFrame({
            "Date": pd.date_range("2020-01-01", periods=100, freq="D"),
            "Component_One": np.random.uniform(0.05, 0.15, 100),
            "Component_Two": np.random.uniform(0.04, 0.12, 100),
            "Component_Three": np.random.uniform(0.06, 0.14, 100)
        })
        self.test_components = ["Component_One", "Component_Two"]
    
    
    def test_calculate_weight_statistics_valid_data(self):
        """Test weight statistics calculation with valid data."""
        test_values = [0.083, 0.085, 0.082, 0.088, 0.079]
        
        result = calculate_weight_statistics(test_values)
        
        assert isinstance(result, dict)
        assert "mean" in result
        assert "std" in result
        assert "min" in result
        assert "max" in result
        assert result["mean"] > 0
        assert result["std"] >= 0
    
    
    def test_calculate_weight_statistics_empty_data(self):
        """Test weight statistics calculation with empty data."""
        result = calculate_weight_statistics([])
        
        assert result["mean"] == 0.0
        assert result["std"] == 0.0
    
    
    def test_get_filtered_weights_dataframe_valid_input(self):
        """Test dataframe filtering with valid input."""
        result = get_filtered_weights_dataframe(
            self.test_weights_data,
            self.test_components,
            "custom",
            "2020-01-01",
            "2020-01-31"
        )
        
        assert not result.empty
        assert "Date" in result.columns
        assert all(comp in result.columns for comp in self.test_components)
    
    
    @pytest.mark.parametrize("time_period", ["1y", "3y", "5y", "10y", "ytd"])
    def test_analyze_portfolio_performance_different_periods(self, time_period):
        """Test portfolio analysis with different time periods."""
        result = analyze_portfolio_performance(
            self.test_weights_data,
            self.test_components,
            time_period
        )
        
        assert isinstance(result, dict)
        assert "statistics" in result
        assert "status" in result
```

## Performance Guidelines

### Optimization Best Practices

```python
# Efficient data processing
def process_large_dataset(weights_dataframe, max_points=200):
    """Process large datasets with automatic optimization."""
    # Input validation
    if weights_dataframe.empty:
        return pd.DataFrame()
    
    # Performance optimization
    if len(weights_dataframe) > max_points:
        # Downsample for performance
        step_size = len(weights_dataframe) // max_points
        weights_dataframe = weights_dataframe.iloc[::step_size]
    
    return weights_dataframe


# Memory-efficient operations
def calculate_rolling_statistics(data_series, window_size=30):
    """Calculate rolling statistics with memory efficiency."""
    # Input validation
    if len(data_series) < window_size:
        return data_series.copy()
    
    # Use Polars for better performance on large data
    if len(data_series) > 1000:
        import polars as pl
        polars_series = pl.Series(data_series)
        return polars_series.rolling_mean(window_size).to_pandas()
    
    # Standard pandas for smaller data
    return data_series.rolling(window=window_size).mean()
```

## Issue Reporting

### Bug Reports

Use this template for bug reports:

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two  
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- Python version:
- Operating system:
- Browser (if applicable):

**Additional Context**
Any other relevant information
```

### Feature Requests

Use this template for feature requests:

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why this feature would be valuable

**Proposed Implementation**
Technical approach (if applicable)

**Alternatives Considered**
Other solutions considered
```

## Getting Help

!!! info "Support Channels"
    - **Documentation**: Check this documentation first
    - **Issues**: Create GitHub issues for bugs and features
    - **Discussions**: Use GitHub discussions for questions
    - **Code Review**: Request reviews on pull requests

## Recognition

Contributors are recognized through:
- GitHub contributor credits
- Documentation acknowledgments  
- Release notes mentions
- Community recognition

Thank you for contributing to the QWIM Dashboard project!