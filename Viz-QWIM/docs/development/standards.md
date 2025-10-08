# Development Standards

This document outlines the comprehensive development standards for the QWIM Dashboard project, ensuring consistent, maintainable, and robust code across all components.

## Code Architecture Principles

### Defensive Programming

!!! success "Primary Approach"
    The project follows defensive programming as the primary approach:
    
    - **Input Validation**: Validate all inputs with early returns
    - **Configuration Validation**: Verify system configuration
    - **Business Logic Validation**: Ensure data integrity
    - **Try-Except Limited**: Reserved for truly unpredictable operations

#### Defensive Programming Example

```python
def calculate_portfolio_weights_statistics(weights_data, selected_components):
    """
    Calculate portfolio statistics with comprehensive validation.
    
    Args:
        weights_data: Portfolio weights DataFrame
        selected_components: List of selected component names
        
    Returns:
        Dictionary with calculated statistics or empty dict if invalid
    """
    # Input validation with early returns (preferred approach)
    if weights_data is None or weights_data.empty:
        return {}
        
    if not selected_components or not isinstance(selected_components, list):
        return {}
    
    # Configuration validation
    required_columns = ["Date"] + selected_components
    missing_columns = [col for col in required_columns if col not in weights_data.columns]
    if missing_columns:
        return {}
    
    # Business logic validation
    if len(weights_data) < 2:
        return {}
    
    # Data quality validation
    for component_name in selected_components:
        if not pd.api.types.is_numeric_dtype(weights_data[component_name]):
            # Try to convert, but use early return if it fails
            try:
                weights_data[component_name] = pd.to_numeric(weights_data[component_name], errors='coerce')
                if weights_data[component_name].isna().all():
                    return {}
            except Exception:
                return {}
    
    # Process only after all validations pass
    statistics_results = {}
    
    for component_name in selected_components:
        component_data = weights_data[component_name]
        
        # Defensive programming for each calculation
        try:
            latest_weight = float(component_data.iloc[-1]) if len(component_data) > 0 else 0.0
        except (ValueError, TypeError, IndexError):
            latest_weight = 0.0
            
        try:
            average_weight = float(component_data.mean()) if len(component_data) > 0 else 0.0
        except (ValueError, TypeError):
            average_weight = 0.0
        
        statistics_results[component_name] = {
            "Latest": latest_weight,
            "Average": average_weight
        }
    
    return statistics_results
```

### Error Handling Strategy

#### When to Use Try-Except

```python
def load_portfolio_data_from_file(file_path):
    """
    Load portfolio data from file with appropriate error handling.
    
    Try-except is appropriate here because file I/O is truly unpredictable.
    """
    # Input validation first
    if not file_path or not isinstance(file_path, (str, Path)):
        return pd.DataFrame()
    
    file_path = Path(file_path)
    if not file_path.exists():
        return pd.DataFrame()
    
    # Try-except for truly unpredictable file operations
    try:
        if file_path.suffix.lower() == '.csv':
            portfolio_data = pd.read_csv(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            portfolio_data = pd.read_excel(file_path)
        elif file_path.suffix.lower() == '.parquet':
            portfolio_data = pd.read_parquet(file_path)
        else:
            return pd.DataFrame()
            
        return portfolio_data
        
    except FileNotFoundError:
        return pd.DataFrame()
    except PermissionError:
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    except Exception as exc:
        # Log unexpected errors but still return safely
        print(f"Unexpected error loading {file_path}: {exc}")
        return pd.DataFrame()


def calculate_simple_average(values_list):
    """
    Calculate average with defensive programming (no try-except needed).
    
    This is predictable logic that should use input validation.
    """
    # Input validation with early returns
    if not values_list or not isinstance(values_list, (list, tuple, pd.Series, np.ndarray)):
        return 0.0
    
    # Convert to numeric if needed (defensive programming)
    try:
        numeric_values = pd.to_numeric(values_list, errors='coerce')
        clean_values = numeric_values.dropna()
    except Exception:
        return 0.0
    
    # Business logic validation
    if len(clean_values) == 0:
        return 0.0
    
    # Simple calculation (no try-except needed for basic arithmetic)
    return float(clean_values.mean())
```

## Naming Conventions

### Variable and Function Names

!!! info "Snake Case Standards"
    Use `snake_case` for all variables and functions with descriptive names.

```python
# Good: Descriptive variable names with snake_case
portfolio_weights_data = load_portfolio_data()
selected_etf_components = ["Component_One", "Component_Two", "Component_Three"]
time_period_selection = "5y"
enable_percentage_display = True
max_points_for_plotting = 200

# Function names should clearly describe purpose
def get_filtered_portfolio_weights_by_time_period():
    """Get portfolio weights filtered by selected time period."""
    pass

def calculate_component_volatility_statistics():
    """Calculate volatility statistics for selected components."""
    pass

def update_visualization_based_on_user_selection():
    """Update chart visualization when user changes selections."""
    pass

# Bad: Non-descriptive or inconsistent names
# data = load_data()  # Too generic
# df = get_weights()  # Abbreviation without context
# calc_stats()  # Incomplete description
```

### Class Names and Constants

```python
# Class names use CamelCase
class PortfolioDataProcessor:
    """Process and validate portfolio weight data."""
    
    def __init__(self, data_source_path: Path):
        self.data_source_path = data_source_path
    
    def process_raw_portfolio_data(self) -> pd.DataFrame:
        """Process raw portfolio data with validation."""
        pass


class ComponentStatisticsCalculator:
    """Calculate comprehensive statistics for portfolio components."""
    
    def calculate_all_statistics(self, component_data: pd.Series) -> dict:
        """Calculate all statistical metrics for a component."""
        pass


# Constants use UPPERCASE
MAX_COMPONENTS_FOR_ANALYSIS = 12
DEFAULT_TIME_PERIOD_YEARS = 5
ENABLE_PNG_EXPORT_BY_DEFAULT = True
PERFORMANCE_DOWNSAMPLING_THRESHOLD = 200
DEFAULT_CHART_HEIGHT_PIXELS = 600
```

### Data Structure Element Names

```python
# Use snake_case with uppercase first letters for dictionary elements
portfolio_statistics_data = {
    "Component_One_Latest_Weight": 0.083,
    "Component_One_Average_Weight": 0.081,
    "Component_Two_Latest_Weight": 0.075,
    "Time_Period_Start_Date": "2020-01-01",
    "Time_Period_End_Date": "2024-01-01",
    "Analysis_Generation_Timestamp": datetime.now()
}

# DataFrame column names
portfolio_weights_df = pd.DataFrame({
    "Date": pd.date_range("2020-01-01", "2024-01-01"),
    "Component_One": [0.083] * 1461,
    "Component_Two": [0.075] * 1461,
    "Component_Three": [0.092] * 1461
})

# Configuration dictionaries
chart_configuration_settings = {
    "Chart_Type_Area": "area",
    "Chart_Type_Line": "line", 
    "Chart_Type_Bar": "bar",
    "Default_Chart_Type": "area",
    "Enable_Interactive_Zoom": True,
    "Show_Percentage_By_Default": False
}
```

### Minimum Variable Name Length

!!! warning "Variable Name Length Requirement"
    Every variable name must have at least three characters, including loop variables.

```python
# Good: Descriptive names with minimum 3 characters
for component_idx in range(12):
    component_name = f"Component_{component_idx}"
    process_portfolio_component(component_name)

for time_idx in range(len(time_periods)):
    current_period = time_periods[time_idx]
    analyze_time_period(current_period)

for row_idx, portfolio_row in portfolio_data.iterrows():
    process_portfolio_row(portfolio_row)

# Acceptable for mathematical contexts with clear meaning
for x_coordinate in range(plot_width):
    for y_coordinate in range(plot_height):
        calculate_plot_pixel(x_coordinate, y_coordinate)

# Bad: Single or two-letter variables
# for i in range(10):  # Avoid
# for j in range(10):  # Avoid  
# df = data  # Avoid abbreviations without context
```

### Shiny Component Naming

#### Input Component Identifiers

```python
# Shiny input identifiers follow specific pattern
input_ID_tab_portfolios_subtab_weights_distribution_time_period
input_ID_tab_portfolios_subtab_weights_distribution_select_all_components
input_ID_tab_portfolios_subtab_weights_distribution_component_Component_One
input_ID_tab_portfolios_subtab_weights_distribution_viz_type
input_ID_tab_portfolios_subtab_weights_distribution_show_pct

# Accessing Shiny input values
selected_time_period = input.input_ID_tab_portfolios_subtab_weights_distribution_time_period()
show_as_percentage = input.input_ID_tab_portfolios_subtab_weights_distribution_show_pct()
```

#### Output Component Identifiers

```python
# Shiny output identifiers follow specific pattern  
output_ID_tab_portfolios_subtab_weights_distribution_plot_main
output_ID_tab_portfolios_subtab_weights_distribution_plot_secondary
output_ID_tab_portfolios_subtab_weights_distribution_statistics_table
output_ID_tab_portfolios_subtab_weights_distribution_data_info

# Defining Shiny outputs
@output
@render_widget
def output_ID_tab_portfolios_subtab_weights_distribution_plot_main():
    """Render main portfolio weights chart."""
    pass

@output
@render.table
def output_ID_tab_portfolios_subtab_weights_distribution_statistics_table():
    """Render portfolio statistics table."""
    pass
```

#### Reactive Value Dictionaries

```python
# Reactive value storage with proper naming
reactives_shiny_values = {
    "Input_Tab_Portfolios_Time_Period": reactive.value("5y"),
    "Input_Tab_Portfolios_Selected_Components": reactive.value([]),
    "Output_Tab_Portfolios_Statistics_Data": reactive.value({}),
    "Plot_Main_Chart_Figure_Object": reactive.value(None),
    "Table_Statistics_Summary_Data": reactive.value(pd.DataFrame())
}

# Accessing reactive values
current_time_period = reactives_shiny_values["Input_Tab_Portfolios_Time_Period"].get()
selected_components = reactives_shiny_values["Input_Tab_Portfolios_Selected_Components"].get()
```

## Function Coding Standards

### Function Definition and Structure

!!! success "Function Structure Requirements"
    - Use input validation (with early returns), configuration validation, business logic validation and defensive programming as the primary approach, with try-except reserved for truly unpredictable operations.
    - Two empty rows before each function definition
    - When a function has at least 2 input arguments, the function signature needs to have only one input argument per row, starting with second row after function name. 
    - Comprehensive docstring documentation and commenting, consistent with Python package mkdocs-material content, formats and style.
    - Type hints for all parameters and return values
    - Input validation at the beginning

```python
def process_portfolio_component_selection(
    available_components: list[str],
    user_selections: dict[str, bool],
    default_selection_count: int = 3
) -> list[str]:
    """
    Process user's portfolio component selections with validation.
    
    This function validates user component selections and applies
    default selection logic when needed.
    
    Args:
        available_components: List of available ETF component names
        user_selections: Dictionary mapping component names to selection status
        default_selection_count: Number of components to select by default
        
    Returns:
        List of selected component names. Returns first N components if
        no valid selections found.
        
    Raises:
        None: Uses defensive programming with early returns
        
    Example:
        >>> available = ["Component_One", "Component_Two", "Component_Three"]
        >>> selections = {"Component_One": True, "Component_Two": False}
        >>> result = process_portfolio_component_selection(available, selections)
        >>> result
        ["Component_One"]
    """
    # Input validation with early returns
    if not available_components or not isinstance(available_components, list):
        return []
        
    if not user_selections or not isinstance(user_selections, dict):
        return available_components[:default_selection_count]
        
    if default_selection_count < 1:
        default_selection_count = 1
    
    # Process user selections with defensive programming
    selected_components = []
    
    for component_name in available_components:
        # Defensive check for component in selections
        if component_name in user_selections:
            try:
                if user_selections[component_name] is True:
                    selected_components.append(component_name)
            except (TypeError, KeyError):
                # Skip invalid selection entries
                continue
    
    # Apply default selection if no valid selections
    if not selected_components:
        max_default = min(default_selection_count, len(available_components))
        selected_components = available_components[:max_default]
    
    return selected_components


def validate_time_period_selection(
    time_period: str,
    custom_start_date: str = None,
    custom_end_date: str = None
) -> tuple[bool, str]:
    """
    Validate time period selection with comprehensive checks.
    
    Args:
        time_period: Selected time period ("1y", "3y", "5y", "10y", "ytd", "custom")
        custom_start_date: Start date for custom period (ISO format)
        custom_end_date: End date for custom period (ISO format)
        
    Returns:
        Tuple of (is_valid, error_message). Error message is empty if valid.
    """
    # Input validation with early returns
    if not time_period or not isinstance(time_period, str):
        return False, "Time period must be a non-empty string"
    
    valid_periods = ["1y", "3y", "5y", "10y", "ytd", "custom"]
    if time_period not in valid_periods:
        return False, f"Time period must be one of: {valid_periods}"
    
    # Custom period validation
    if time_period == "custom":
        if not custom_start_date or not custom_end_date:
            return False, "Custom period requires both start and end dates"
        
        try:
            start_date = pd.to_datetime(custom_start_date)
            end_date = pd.to_datetime(custom_end_date)
            
            if start_date >= end_date:
                return False, "Start date must be before end date"
                
            # Business logic validation
            date_range = end_date - start_date
            if date_range.days < 1:
                return False, "Date range must be at least 1 day"
                
        except Exception as exc:
            return False, f"Invalid date format: {exc}"
    
    return True, ""
```

### Documentation Standards

#### Comprehensive Docstrings

```python
def calculate_portfolio_weight_statistics(
    weights_dataframe: pd.DataFrame,
    selected_components: list[str],
    calculate_percentages: bool = False
) -> dict[str, dict[str, float]]:
    """
    Calculate comprehensive statistical metrics for portfolio component weights.
    
    This function computes key statistical measures including latest values,
    historical averages, volatility metrics, and range information for
    selected portfolio components.
    
    The function implements defensive programming with comprehensive input
    validation and graceful error handling for robust operation.
    
    Args:
        weights_dataframe: DataFrame containing portfolio weights with Date column
            and component weight columns. Must contain at least 2 rows of data.
        selected_components: List of component names to analyze. Component names
            must correspond to column names in weights_dataframe.
        calculate_percentages: If True, normalize weights to percentages based on
            selected components. If False, use absolute weight values.
            
    Returns:
        Dictionary mapping component names to their statistical metrics.
        Each component maps to a dictionary containing:
            - "Latest": Most recent weight value
            - "Average": Historical mean weight
            - "Min": Minimum weight in period
            - "Max": Maximum weight in period  
            - "StdDev": Standard deviation (volatility measure)
        Returns empty dictionary if input validation fails.
        
    Raises:
        None: Function uses defensive programming with early returns instead
            of raising exceptions for predictable error conditions.
            
    Example:
        >>> weights_df = pd.DataFrame({
        ...     "Date": pd.date_range("2020-01-01", periods=100),
        ...     "Component_One": np.random.normal(0.083, 0.005, 100),
        ...     "Component_Two": np.random.normal(0.075, 0.003, 100)
        ... })
        >>> components = ["Component_One", "Component_Two"]
        >>> stats = calculate_portfolio_weight_statistics(weights_df, components)
        >>> "Component_One" in stats
        True
        >>> "Latest" in stats["Component_One"]
        True
        
    Note:
        This function follows project coding standards:
        - Input validation with early returns
        - Defensive programming for data quality
        - Descriptive variable names with snake_case
        - Comprehensive error handling without exceptions
    """
    # Implementation follows defensive programming patterns...
    pass
```

### Type Hints Standards

```python
from typing import Optional, Union, Dict, List, Tuple, Any
from pathlib import Path
import pandas as pd
import numpy as np

def load_and_process_portfolio_data(
    data_file_path: Union[str, Path],
    selected_components: List[str],
    time_period_config: Dict[str, Any],
    enable_caching: bool = True
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Load and process portfolio data with comprehensive type hints.
    
    Args:
        data_file_path: Path to portfolio data file (CSV, Excel, or Parquet)
        selected_components: List of component names to include in analysis
        time_period_config: Configuration dictionary with time period settings
        enable_caching: Whether to cache processed data for performance
        
    Returns:
        Tuple containing:
            - Processed portfolio DataFrame
            - Dictionary with processing metadata and statistics
    """
    pass

def calculate_component_correlation_matrix(
    weights_data: pd.DataFrame,
    component_list: List[str],
    correlation_method: str = "pearson"
) -> Optional[np.ndarray]:
    """
    Calculate correlation matrix for portfolio components.
    
    Args:
        weights_data: DataFrame with component weight time series
        component_list: Components to include in correlation analysis
        correlation_method: Method for correlation calculation
        
    Returns:
        Correlation matrix as numpy array, or None if calculation fails
    """
    pass

# Complex type hints for nested structures
ComponentStatistics = Dict[str, Dict[str, float]]
TimeSeriesData = Dict[str, Union[pd.DataFrame, List[str], bool]]
ConfigurationSettings = Dict[str, Union[str, int, float, bool, List[str]]]

def generate_comprehensive_portfolio_report(
    portfolio_data: pd.DataFrame,
    analysis_config: ConfigurationSettings,
    output_formats: List[str]
) -> Dict[str, Union[ComponentStatistics, TimeSeriesData]]:
    """Generate comprehensive portfolio analysis report with complex return types."""
    pass
```

## Module and File Organization

### File Naming Conventions

```python
# Module names: lowercase
# utils_data.py
# utils_visuals.py
# reactives_shiny.py

# Test files: test_ prefix
# test_portfolio_analysis.py
# test_utils_data.py
# test_component_statistics.py

# Package names: lowercase_with_underscores
# modules_tab_portfolios/
# utils_dashboard/
```

### Import Organization

```python
"""
Portfolio analysis utilities module.

This module provides comprehensive portfolio analysis functionality
including weight calculations, statistical analysis, and data processing.
"""

# Standard library imports
import copy
import os
import sys
import typing
from datetime import datetime, timedelta
from pathlib import Path

# Third-party imports
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import polars as pl

# Shiny imports
from shiny import ui, render, reactive

# Local imports
from src.dashboard.utils_dashboard.utils_data import (
    get_data_inputs,
    get_data_utils,
    validate_portfolio_data
)
from src.dashboard.utils_dashboard.utils_visuals import (
    create_portfolio_chart,
    save_plot_as_png
)
```

## Testing Standards

### Test File Structure

```python
"""
Unit tests for portfolio statistics calculations.

This module tests all statistical calculation functions to ensure
accuracy, robustness, and proper error handling.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch

# Import functions under test
from src.dashboard.utils_dashboard.utils_data import (
    calculate_portfolio_weight_statistics,
    validate_time_period_selection,
    process_portfolio_component_selection
)


class TestCalculatePortfolioWeightStatistics:
    """Test suite for portfolio weight statistics calculations."""
    
    
    def test_calculate_statistics_with_valid_data(self):
        """Test statistics calculation with valid portfolio data."""
        # Arrange
        test_data = pd.DataFrame({
            "Date": pd.date_range("2020-01-01", periods=100),
            "Component_One": np.random.normal(0.083, 0.005, 100),
            "Component_Two": np.random.normal(0.075, 0.003, 100)
        })
        selected_components = ["Component_One", "Component_Two"]
        
        # Act
        result = calculate_portfolio_weight_statistics(test_data, selected_components)
        
        # Assert
        assert len(result) == 2
        assert "Component_One" in result
        assert "Component_Two" in result
        assert "Latest" in result["Component_One"]
        assert "Average" in result["Component_One"]
        assert result["Component_One"]["StdDev"] > 0


    def test_calculate_statistics_with_empty_dataframe(self):
        """Test statistics calculation with empty DataFrame returns empty dict."""
        # Arrange
        empty_dataframe = pd.DataFrame()
        selected_components = ["Component_One"]
        
        # Act
        result = calculate_portfolio_weight_statistics(empty_dataframe, selected_components)
        
        # Assert
        assert result == {}


    @pytest.mark.parametrize("invalid_input", [
        None,
        "not_a_dataframe",
        123,
        []
    ])
    def test_calculate_statistics_with_invalid_input_types(self, invalid_input):
        """Test statistics calculation with various invalid input types."""
        # Arrange
        selected_components = ["Component_One"]
        
        # Act
        result = calculate_portfolio_weight_statistics(invalid_input, selected_components)
        
        # Assert
        assert result == {}


    def test_calculate_statistics_with_missing_components(self):
        """Test statistics calculation when selected components are missing from data."""
        # Arrange
        test_data = pd.DataFrame({
            "Date": pd.date_range("2020-01-01", periods=10),
            "Component_One": [0.083] * 10
        })
        selected_components = ["Component_One", "Component_Missing"]
        
        # Act  
        result = calculate_portfolio_weight_statistics(test_data, selected_components)
        
        # Assert
        assert result == {}  # Should return empty due to missing component


    def test_calculate_statistics_performance_with_large_dataset(self):
        """Test performance with large dataset (performance test)."""
        # Arrange
        large_data = pd.DataFrame({
            "Date": pd.date_range("2000-01-01", periods=10000),
            "Component_One": np.random.normal(0.083, 0.005, 10000),
            "Component_Two": np.random.normal(0.075, 0.003, 10000)
        })
        selected_components = ["Component_One", "Component_Two"]
        
        # Act & Assert (should complete within reasonable time)
        import time
        start_time = time.time()
        result = calculate_portfolio_weight_statistics(large_data, selected_components)
        end_time = time.time()
        
        # Performance assertion
        assert (end_time - start_time) < 1.0  # Should complete within 1 second
        assert len(result) == 2
```

### Mock Objects for Shiny Testing

```python
@pytest.fixture
def mock_shiny_input():
    """Create mock Shiny input object with realistic behavior."""
    mock_input = Mock()
    
    # Set up reactive method returns
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_time_period.return_value = "5y"
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_viz_type.return_value = "area"
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_show_pct.return_value = False
    
    # Mock component checkboxes
    test_components = ["Component_One", "Component_Two", "Component_Three"]
    for idx, component in enumerate(test_components):
        checkbox_attr = f"input_ID_tab_portfolios_subtab_weights_distribution_component_{component}"
        checkbox_mock = Mock(return_value=(idx < 3))  # First 3 selected by default
        setattr(mock_input, checkbox_attr, checkbox_mock)
    
    return mock_input


def test_component_selection_with_mock_input(mock_shiny_input):
    """Test component selection logic with mocked Shiny input."""
    # Test implementation using mock_shiny_input
    pass
```

## Performance Standards

### Data Processing Optimization

```python
def optimize_large_dataset_processing(
    large_dataset: pd.DataFrame,
    max_processing_points: int = 200,
    enable_polars_optimization: bool = True
) -> pd.DataFrame:
    """
    Optimize large dataset processing with automatic downsampling.
    
    Args:
        large_dataset: Input dataset that may be large
        max_processing_points: Maximum points to retain after optimization
        enable_polars_optimization: Use Polars for heavy processing
        
    Returns:
        Optimized dataset suitable for visualization and analysis
    """
    # Input validation
    if large_dataset is None or large_dataset.empty:
        return pd.DataFrame()
    
    if max_processing_points < 1:
        max_processing_points = 200
    
    # Apply optimization strategies based on size
    if len(large_dataset) <= max_processing_points:
        return large_dataset.copy()
    
    # Use Polars for heavy processing if enabled
    if enable_polars_optimization and len(large_dataset) > 1000:
        try:
            # Convert to Polars for efficient processing
            polars_df = pl.from_pandas(large_dataset)
            
            # Efficient downsampling with Polars
            step_size = len(polars_df) // max_processing_points
            downsampled_polars = polars_df.slice(0, None, step_size)
            
            # Convert back to Pandas for compatibility
            optimized_dataset = downsampled_polars.to_pandas()
            
        except Exception:
            # Fallback to Pandas if Polars processing fails
            step_size = len(large_dataset) // max_processing_points
            optimized_dataset = large_dataset.iloc[::step_size].copy()
    else:
        # Standard Pandas downsampling
        step_size = len(large_dataset) // max_processing_points
        optimized_dataset = large_dataset.iloc[::step_size].copy()
    
    return optimized_dataset
```

### Memory Management

```python
def process_portfolio_data_with_memory_management(
    portfolio_data_source: Path,
    processing_config: dict
) -> pd.DataFrame:
    """
    Process portfolio data with explicit memory management.
    
    Args:
        portfolio_data_source: Path to portfolio data file
        processing_config: Configuration for processing options
        
    Returns:
        Processed portfolio DataFrame
    """
    # Load data efficiently
    try:
        if portfolio_data_source.suffix.lower() == '.parquet':
            # Parquet is most memory efficient
            raw_data = pd.read_parquet(portfolio_data_source)
        else:
            raw_data = pd.read_csv(portfolio_data_source)
    except Exception:
        return pd.DataFrame()
    
    # Process in chunks if dataset is very large
    if len(raw_data) > 100000:  # 100k rows threshold
        processed_chunks = []
        chunk_size = 10000
        
        for chunk_start in range(0, len(raw_data), chunk_size):
            chunk_end = min(chunk_start + chunk_size, len(raw_data))
            data_chunk = raw_data.iloc[chunk_start:chunk_end].copy()
            
            # Process chunk
            processed_chunk = apply_data_processing(data_chunk, processing_config)
            processed_chunks.append(processed_chunk)
            
            # Explicit memory cleanup
            del data_chunk
        
        # Combine processed chunks
        final_data = pd.concat(processed_chunks, ignore_index=True)
        
        # Cleanup
        del processed_chunks
        del raw_data
        
    else:
        # Process normally for smaller datasets
        final_data = apply_data_processing(raw_data, processing_config)
    
    return final_data


def apply_data_processing(data_chunk: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Apply data processing with memory-efficient operations."""
    # Implementation with memory-conscious operations
    pass
```

## Next Steps

Continue with related documentation:

- [Contributing Guide](contributing.md) - Detailed contribution workflow
- [Testing Guide](testing.md) - Comprehensive testing procedures  
- [API Reference](../reference/main.md) - Technical API documentation

These standards ensure consistent, maintainable, and robust code across the QWIM Dashboard project.