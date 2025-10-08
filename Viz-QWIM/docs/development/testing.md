# Testing Guide

This document provides comprehensive testing guidelines for the QWIM Dashboard project, ensuring robust and reliable functionality across all components.

## Testing Philosophy

### Testing Principles

!!! success "Core Testing Principles"
    - **Defensive Testing**: Test edge cases and error conditions extensively
    - **Input Validation**: Verify all input validation scenarios
    - **Data Quality**: Ensure data integrity throughout processing
    - **Performance**: Test with realistic data volumes
    - **User Experience**: Validate interactive behaviors

### Testing Strategy

=== "Unit Testing"
    **Focus**: Individual functions and methods
    
    - Function-level logic validation
    - Input/output verification
    - Edge case handling
    - Error condition testing

=== "Integration Testing"
    **Focus**: Component interactions
    
    - Module integration verification
    - Data flow validation
    - Reactive system testing
    - End-to-end workflows

=== "Performance Testing"
    **Focus**: System performance
    
    - Large dataset handling
    - Memory usage validation
    - Response time verification
    - Scalability assessment

## Test Structure

### Directory Organization

```
tests/
├── unit/                          # Unit tests
│   ├── test_portfolio_analysis.py
│   ├── test_utils_data.py
│   ├── test_utils_visuals.py
│   └── test_reactives_shiny.py
├── integration/                   # Integration tests  
│   ├── test_portfolio_workflow.py
│   ├── test_data_pipeline.py
│   └── test_ui_interactions.py
├── performance/                   # Performance tests
│   ├── test_large_datasets.py
│   └── test_memory_usage.py
├── fixtures/                      # Test data and fixtures
│   ├── sample_portfolio_data.csv
│   ├── test_configurations.json
│   └── mock_data_generators.py
└── conftest.py                    # Pytest configuration
```

### Test Configuration

#### conftest.py

````python
# filepath: [conftest.py](http://_vscodecontentref_/0)
"""
Pytest configuration and shared fixtures for QWIM Dashboard tests.

This module provides common test fixtures, configuration,
and utilities used across all test modules.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
from datetime import datetime, timedelta

# Test configuration
pytest_plugins = ["pytest_mock"]

# Test data constants
TEST_DATA_START_DATE = "2020-01-01"
TEST_DATA_END_DATE = "2024-01-01"
TEST_COMPONENTS = [
    "Component_One", "Component_Two", "Component_Three",
    "Component_Four", "Component_Five", "Component_Six"
]


@pytest.fixture(scope="session")
def test_data_directory():
    """Create temporary directory for test data."""
    temp_dir = tempfile.mkdtemp(prefix="qwim_test_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_portfolio_data():
    """Generate realistic portfolio weights data for testing."""
    dates = pd.date_range(TEST_DATA_START_DATE, TEST_DATA_END_DATE, freq="D")
    np.random.seed(42)  # Reproducible test data
    
    # Generate realistic weight distributions
    base_weights = {
        "Component_One": 0.083,
        "Component_Two": 0.075, 
        "Component_Three": 0.092,
        "Component_Four": 0.088,
        "Component_Five": 0.065,
        "Component_Six": 0.078
    }
    
    portfolio_data = {"Date": dates}
    
    # Add noise to base weights to simulate realistic variations
    for component, base_weight in base_weights.items():
        noise = np.random.normal(0, base_weight * 0.05, len(dates))
        weights = np.maximum(base_weight + noise, 0.001)  # Ensure positive weights
        portfolio_data[component] = weights
    
    return pd.DataFrame(portfolio_data)


@pytest.fixture
def large_portfolio_data():
    """Generate large dataset for performance testing."""
    dates = pd.date_range("2000-01-01", "2024-01-01", freq="D")  # 24 years of daily data
    np.random.seed(123)
    
    large_data = {"Date": dates}
    
    # Generate 12 components for comprehensive testing
    for idx in range(1, 13):
        component_name = f"Component_{idx:02d}"
        base_weight = 0.083 + (idx - 6.5) * 0.001  # Vary around 8.3%
        noise = np.random.normal(0, base_weight * 0.03, len(dates))
        weights = np.maximum(base_weight + noise, 0.001)
        large_data[component_name] = weights
    
    return pd.DataFrame(large_data)


@pytest.fixture
def empty_portfolio_data():
    """Generate empty portfolio data for edge case testing."""
    return pd.DataFrame()


@pytest.fixture
def invalid_portfolio_data():
    """Generate invalid portfolio data for error testing."""
    return pd.DataFrame({
        "NotDate": ["invalid", "data", "format"],
        "InvalidComponent": ["not", "numeric", "values"]
    })


@pytest.fixture
def mock_shiny_input():
    """Mock Shiny input object for testing."""
    mock_input = Mock()
    
    # Set up common input methods
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_time_period.return_value = "5y"
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_select_all_components.return_value = False
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_viz_type.return_value = "area"
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_show_pct.return_value = False
    
    # Mock component selection checkboxes
    for component in TEST_COMPONENTS:
        checkbox_attr = f"input_ID_tab_portfolios_subtab_weights_distribution_component_{component}"
        checkbox_mock = Mock(return_value=False)
        setattr(mock_input, checkbox_attr, checkbox_mock)
    
    # Set first 3 components as selected by default
    for idx in range(3):
        component = TEST_COMPONENTS[idx]
        checkbox_attr = f"input_ID_tab_portfolios_subtab_weights_distribution_component_{component}"
        getattr(mock_input, checkbox_attr).return_value = True
    
    return mock_input


@pytest.fixture  
def mock_shiny_output():
    """Mock Shiny output object for testing."""
    mock_output = Mock()
    return mock_output


@pytest.fixture
def mock_shiny_session():
    """Mock Shiny session object for testing."""
    mock_session = Mock()
    return mock_session


@pytest.fixture
def test_data_utils():
    """Generate test data utilities configuration."""
    return {
        "project_dir": Path.cwd(),
        "max_points_plotting": 200,
        "enable_performance_logging": False,
        "default_time_period": "5y"
    }


@pytest.fixture
def test_reactives_shiny():
    """Generate test reactive values."""
    from unittest.mock import MagicMock
    
    return {
        "Input_Tab_Portfolios_Selected_Components": MagicMock(),
        "Input_Tab_Portfolios_Time_Period": MagicMock(),
        "Output_Tab_Portfolios_Statistics_Data": MagicMock(),
        "Plot_Main_Chart_Data": MagicMock()
    }


@pytest.fixture(autouse=True)
def reset_random_seed():
    """Reset random seed before each test for reproducibility."""
    np.random.seed(42)
    yield
    np.random.seed()  # Reset to random seed after test


# Performance testing fixtures
@pytest.fixture
def performance_threshold_data():
    """Performance thresholds for testing."""
    return {
        "max_processing_time_seconds": 5.0,
        "max_memory_mb": 500,
        "max_plot_rendering_time_seconds": 2.0
    }


# Parametrized fixtures for comprehensive testing
@pytest.fixture(params=["1y", "3y", "5y", "10y", "ytd", "custom"])
def time_period_options(request):
    """Parametrized fixture for different time periods."""
    return request.param


@pytest.fixture(params=["area", "line", "bar", "heatmap"])
def visualization_types(request):
    """Parametrized fixture for different visualization types."""
    return request.param


@pytest.fixture(params=[True, False])
def percentage_modes(request):
    """Parametrized fixture for percentage/absolute modes."""
    return request.param