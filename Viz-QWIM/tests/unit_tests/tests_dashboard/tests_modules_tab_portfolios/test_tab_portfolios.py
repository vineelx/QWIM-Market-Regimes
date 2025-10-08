"""
Comprehensive tests for tab_portfolios module following project coding standards.

Tests UI generation, server logic, module coordination, error handling, and integration
scenarios for the main Portfolios tab with defensive programming principles.
"""

import pytest
import polars as pl
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock, call
import plotly.graph_objects as go
import tempfile
import shutil
import os
from io import StringIO, BytesIO
import typing

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the module under test with error handling
try:
    from src.dashboard.modules_tab_portfolios.tab_portfolios import (
        tab_portfolios_ui,
        tab_portfolios_server,
        OUTPUT_DIR,
        TEMP_GRAPHICS_DIR,
        ENABLE_PNG_SAVING_TAB_PORTFOLIOS
    )
except ImportError as import_error:
    pytest.skip(f"Cannot import required modules: {import_error}", allow_module_level=True)

# Import dependencies for mocking
try:
    from shiny import ui, module, reactive, render
    import plotly.io as pio
    HAS_SHINY_DEPENDENCIES = True
except ImportError:
    HAS_SHINY_DEPENDENCIES = False


# Configure pytest to register custom marks properly
def pytest_configure(config):
    """Configure pytest with custom marks."""
    config.addinivalue_line("markers", "slow: mark test as slow running test")
    config.addinivalue_line("markers", "integration: mark test as integration test") 
    config.addinivalue_line("markers", "performance: mark test as performance test")
    config.addinivalue_line("markers", "shiny: mark test as requiring Shiny session")
    config.addinivalue_line("markers", "module_coordination: mark test as module coordination test")


# Module-level fixtures for shared test data


@pytest.fixture(scope="session")
def test_data_directory():
    """Fixture providing test data directory path."""
    return Path(__file__).parent / "test_data"


@pytest.fixture(scope="session")
def project_root_directory():
    """Fixture providing project root directory path."""
    return Path(__file__).parent.parent.parent.parent.parent


@pytest.fixture
def mock_shiny_session():
    """Fixture providing mocked Shiny session components for all subtabs."""
    mock_input = Mock()
    mock_output = Mock()
    mock_session = Mock()
    
    # Set up default input values for all subtabs
    # Portfolio Analysis subtab inputs
    mock_input.input_ID_tab_portfolios_subtab_portfolios_analysis_time_period.return_value = "1y"
    mock_input.input_ID_tab_portfolios_subtab_portfolios_analysis_type.return_value = "returns"
    mock_input.input_ID_tab_portfolios_subtab_portfolios_analysis_include_benchmark.return_value = True
    
    # Portfolio Comparison subtab inputs
    mock_input.input_ID_tab_portfolios_subtab_portfolios_comparison_time_period.return_value = "1y"
    mock_input.input_ID_tab_portfolios_subtab_portfolios_comparison_viz_type.return_value = "normalized"
    mock_input.input_ID_tab_portfolios_subtab_portfolios_comparison_show_diff.return_value = False
    
    # Weights Distribution subtab inputs
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_time_period.return_value = "5y"
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_viz_type.return_value = "area"
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_show_pct.return_value = True
    
    # Mock date range for custom periods
    mock_date_range = [datetime.now() - timedelta(days=365), datetime.now()]
    mock_input.input_ID_tab_portfolios_subtab_portfolios_analysis_date_range.return_value = mock_date_range
    mock_input.input_ID_tab_portfolios_subtab_portfolios_comparison_date_range.return_value = mock_date_range
    mock_input.input_ID_tab_portfolios_subtab_weights_distribution_date_range.return_value = mock_date_range
    
    return mock_input, mock_output, mock_session


@pytest.fixture
def comprehensive_sample_data():
    """Fixture providing comprehensive sample data for all portfolio analysis modules."""
    # Generate realistic time series data
    num_days = 1000
    base_date = datetime.now() - timedelta(days=num_days)
    dates = [(base_date + timedelta(days=idx)).strftime("%Y-%m-%d") for idx in range(num_days)]
    
    # Portfolio data with realistic returns
    portfolio_base_value = 10000.0
    portfolio_values = []
    current_portfolio_value = portfolio_base_value
    
    for idx in range(num_days):
        daily_return = np.random.normal(0.0008, 0.012)  # 0.08% daily return, 1.2% volatility
        current_portfolio_value *= (1 + daily_return)
        portfolio_values.append(current_portfolio_value)
    
    # Benchmark data with correlation to portfolio
    benchmark_base_value = 10000.0
    benchmark_values = []
    current_benchmark_value = benchmark_base_value
    
    for idx in range(num_days):
        daily_return = np.random.normal(0.0006, 0.010)  # Slightly lower return and volatility
        current_benchmark_value *= (1 + daily_return)
        benchmark_values.append(current_benchmark_value)
    
    # ETF weights data
    etf_components = ["Component_One", "Component_Two", "Component_Three", "Component_Four", "Component_Five"]
    weights_dates = dates[::30]  # Monthly rebalancing
    
    weights_data = {"Date": weights_dates}
    for component in etf_components:
        # Generate realistic weights that sum approximately to 1
        weights = np.random.dirichlet([1] * len(etf_components), len(weights_dates))
        component_weights = weights[:, etf_components.index(component)]
        weights_data[component] = component_weights.tolist()
    
    # ETF time series data
    etf_time_series_data = {"Date": dates}
    for component in etf_components:
        base_price = 100.0
        prices = []
        current_price = base_price
        
        for idx in range(num_days):
            daily_return = np.random.normal(0.0005, 0.015)
            current_price *= (1 + daily_return)
            prices.append(current_price)
        
        etf_time_series_data[component] = prices
    
    return {
        "My_Portfolio": pl.DataFrame({"Date": dates, "Value": portfolio_values}),
        "Benchmark_Portfolio": pl.DataFrame({"Date": dates, "Value": benchmark_values}),
        "Weights_My_Portfolio": pl.DataFrame(weights_data),
        "Time_Series_ETFs": pl.DataFrame(etf_time_series_data)
    }


@pytest.fixture
def mock_data_utils():
    """Fixture providing mock data utilities configuration."""
    return {
        "theme": "material",
        "export_enabled": True,
        "performance_optimization": True,
        "max_data_points": 1000,
        "default_time_period": "1y",
        "enable_caching": True,
        "error_handling_mode": "graceful"
    }


@pytest.fixture
def mock_reactives_shiny():
    """Fixture providing mock reactive variables for cross-module communication."""
    return {
        "Selected_Time_Period": "1y",
        "Global_Portfolio_Data": None,
        "Global_Benchmark_Data": None,
        "Cross_Module_Settings": {},
        "Export_Configuration": {"enabled": False, "format": "png"},
        "User_Preferences": {"theme": "light", "precision": 2}
    }


@pytest.fixture
def temp_output_directory(tmp_path):
    """Fixture providing temporary output directory for testing file operations."""
    temp_dir = tmp_path / "test_output"
    temp_graphics_dir = temp_dir / "temp-graphics"
    temp_graphics_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir, temp_graphics_dir


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Fixture to set up test environment for each test with proper cleanup."""
    # Setup code before each test
    original_enable_png = ENABLE_PNG_SAVING_TAB_PORTFOLIOS
    
    yield
    
    # Cleanup code after each test
    # Restore original settings
    pass


@pytest.fixture
def mock_subtab_modules():
    """Fixture providing mocked subtab UI and server modules."""
    with patch('src.dashboard.modules_tab_portfolios.tab_portfolios.subtab_portfolios_analysis_ui') as mock_analysis_ui, \
         patch('src.dashboard.modules_tab_portfolios.tab_portfolios.subtab_portfolios_analysis_server') as mock_analysis_server, \
         patch('src.dashboard.modules_tab_portfolios.tab_portfolios.subtab_portfolios_comparison_ui') as mock_comparison_ui, \
         patch('src.dashboard.modules_tab_portfolios.tab_portfolios.subtab_portfolios_comparison_server') as mock_comparison_server, \
         patch('src.dashboard.modules_tab_portfolios.tab_portfolios.subtab_weights_distribution_ui') as mock_weights_ui, \
         patch('src.dashboard.modules_tab_portfolios.tab_portfolios.subtab_weights_distribution_server') as mock_weights_server:
        
        # Create mock UI elements
        mock_ui_element = Mock()
        mock_ui_element.tagify = Mock(return_value="<div>Mock UI Element</div>")
        mock_ui_element.children = []
        
        mock_analysis_ui.return_value = mock_ui_element
        mock_comparison_ui.return_value = mock_ui_element
        mock_weights_ui.return_value = mock_ui_element
        
        # Create mock server instances
        mock_server_instance = Mock()
        mock_server_instance.status = "initialized"
        mock_server_instance.module_id = "test_module"
        
        mock_analysis_server.return_value = mock_server_instance
        mock_comparison_server.return_value = mock_server_instance
        mock_weights_server.return_value = mock_server_instance
        
        yield {
            'analysis_ui': mock_analysis_ui,
            'analysis_server': mock_analysis_server,
            'comparison_ui': mock_comparison_ui,
            'comparison_server': mock_comparison_server,
            'weights_ui': mock_weights_ui,
            'weights_server': mock_weights_server,
            'ui_element': mock_ui_element,
            'server_instance': mock_server_instance
        }


@pytest.fixture
def mock_shiny_ui_components():
    """Fixture providing mocked Shiny UI components for tab navigation."""
    with patch('shiny.ui.nav_panel') as mock_nav_panel, \
         patch('shiny.ui.navset_tab') as mock_navset_tab:
        
        # Create mock UI elements
        mock_panel = Mock()
        mock_panel.title = "Test Panel"
        mock_panel.content = Mock()
        
        mock_navset = Mock()
        mock_navset.panels = []
        mock_navset.id = "test_navset"
        
        mock_nav_panel.return_value = mock_panel
        mock_navset_tab.return_value = mock_navset
        
        yield {
            'nav_panel': mock_nav_panel,
            'navset_tab': mock_navset_tab,
            'panel': mock_panel,
            'navset': mock_navset
        }


class TestTabPortfoliosConstants:
    """Test module constants and configuration validation."""
    

    def test_output_directory_constants_validation(self):
        """Test output directory constants are properly configured (configuration validation)."""
        # Assert
        assert OUTPUT_DIR is not None
        assert isinstance(OUTPUT_DIR, Path)
        assert str(OUTPUT_DIR) == "output"
        
        # Test directory structure expectations
        expected_path_components = str(OUTPUT_DIR).split(os.sep)
        assert "output" in expected_path_components


    def test_temp_graphics_directory_constants_validation(self):
        """Test temp graphics directory constants are properly configured (configuration validation)."""
        # Assert
        assert TEMP_GRAPHICS_DIR is not None
        assert isinstance(TEMP_GRAPHICS_DIR, Path)
        assert "temp-graphics" in str(TEMP_GRAPHICS_DIR)
        
        # Test parent-child relationship
        assert TEMP_GRAPHICS_DIR.parent == OUTPUT_DIR


    def test_module_constants_consistency(self):
        """Test consistency across module constants (configuration validation)."""
        # Assert directory relationships
        assert TEMP_GRAPHICS_DIR.is_relative_to(OUTPUT_DIR)
        
        # Test naming conventions
        assert "output" in str(OUTPUT_DIR).lower()
        assert "graphics" in str(TEMP_GRAPHICS_DIR).lower()
        assert "temp" in str(TEMP_GRAPHICS_DIR).lower()


class TestTabPortfoliosUI:
    """Test UI generation, navigation structure, and component integration."""
    

    def test_tab_portfolios_ui_basic_structure_validation(self, mock_subtab_modules, mock_shiny_ui_components, mock_data_utils, comprehensive_sample_data):
        """Test basic UI structure and navigation generation (business logic validation)."""
        # Arrange
        data_utils = mock_data_utils
        data_inputs = comprehensive_sample_data
        
        # Act
        ui_result = tab_portfolios_ui(
            "ID_tab_portfolios",
            data_utils,
            data_inputs)
        
        # Assert
        assert ui_result is not None
        
        # Verify subtab UI functions were called with correct parameters
        mock_subtab_modules['analysis_ui'].assert_called_once()
        mock_subtab_modules['comparison_ui'].assert_called_once()  
        mock_subtab_modules['weights_ui'].assert_called_once()
        
        # Verify correct module IDs were used
        analysis_call_args = mock_subtab_modules['analysis_ui'].call_args
        assert analysis_call_args[1]['id'] == "ID_tab_portfolios_subtab_portfolios_analysis"
        
        comparison_call_args = mock_subtab_modules['comparison_ui'].call_args
        assert comparison_call_args[1]['id'] == "ID_tab_portfolios_subtab_portfolios_comparison"
        
        weights_call_args = mock_subtab_modules['weights_ui'].call_args
        assert weights_call_args[1]['id'] == "ID_tab_portfolios_subtab_weights_distribution"


    def test_tab_portfolios_ui_parameter_distribution(self, mock_subtab_modules, mock_shiny_ui_components, mock_data_utils, comprehensive_sample_data):
        """Test proper parameter distribution to all subtab modules (configuration validation)."""
        # Arrange
        data_utils = mock_data_utils
        data_inputs = comprehensive_sample_data
        
        # Act
        ui_result = tab_portfolios_ui(
            "ID_tab_portfolios",
            data_utils, 
            data_inputs)
        
        # Assert parameter distribution
        # All subtabs should receive the same data_utils and data_inputs
        for ui_mock in [mock_subtab_modules['analysis_ui'], mock_subtab_modules['comparison_ui'], mock_subtab_modules['weights_ui']]:
            call_args = ui_mock.call_args
            assert call_args[1]['data_utils'] == data_utils
            assert call_args[1]['data_inputs'] == data_inputs


    def test_tab_portfolios_ui_with_empty_data_inputs(self, mock_subtab_modules, mock_shiny_ui_components, mock_data_utils):
        """Test UI generation with empty data inputs (defensive programming)."""
        # Arrange
        data_utils = mock_data_utils
        empty_data_inputs = {}
        
        # Act
        ui_result = tab_portfolios_ui(
            "ID_tab_portfolios",
            data_utils, 
            empty_data_inputs)
        
        # Assert
        assert ui_result is not None
        
        # Verify all subtab UIs were still called (should handle empty data gracefully)
        mock_subtab_modules['analysis_ui'].assert_called_once()
        mock_subtab_modules['comparison_ui'].assert_called_once()
        mock_subtab_modules['weights_ui'].assert_called_once()


    def test_tab_portfolios_ui_with_none_parameters(self, mock_subtab_modules, mock_shiny_ui_components):
        """Test UI generation with None parameters (defensive programming)."""
        # Arrange
        data_utils_none = None
        data_inputs_none = None
        
        # Act
        ui_result = tab_portfolios_ui(
            "ID_tab_portfolios",
            data_utils_none, 
            data_inputs_none)
        
        # Assert
        assert ui_result is not None
        
        # Verify subtab UIs handle None parameters gracefully
        for ui_mock in [mock_subtab_modules['analysis_ui'], mock_subtab_modules['comparison_ui'], mock_subtab_modules['weights_ui']]:
            call_args = ui_mock.call_args
            assert call_args[1]['data_utils'] is None
            assert call_args[1]['data_inputs'] is None


    # def test_tab_portfolios_ui_navigation_panel_structure(self, mock_subtab_modules, mock_shiny_ui_components, mock_data_utils, comprehensive_sample_data):
    #     """Test navigation panel structure and naming (configuration validation)."""
    #     # Arrange
    #     data_utils = mock_data_utils
    #     data_inputs = comprehensive_sample_data
        
    #     # Act
    #     ui_result = tab_portfolios_ui(
    #         "ID_tab_portfolios",
    #         data_utils, 
    #         data_inputs)
        
    #     # Assert
    #     # Verify nav_panel was called for each subtab with correct titles
    #     assert mock_shiny_ui_components['nav_panel'].call_count == 3
        
    #     nav_panel_calls = mock_shiny_ui_components['nav_panel'].call_args_list
    #     panel_titles = [call[0][0] for call in nav_panel_calls]
        
    #     expected_titles = ["Portfolio Analysis", "Portfolio Comparison", "Weights Distribution"]
    #     assert all(title in panel_titles for title in expected_titles)


    def test_tab_portfolios_ui_navset_configuration(self, mock_subtab_modules, mock_shiny_ui_components, mock_data_utils, comprehensive_sample_data):
        """Test navset tab configuration and ID assignment (configuration validation)."""
        # Arrange
        data_utils = mock_data_utils
        data_inputs = comprehensive_sample_data
        
        # Act
        ui_result = tab_portfolios_ui(
            "ID_tab_portfolios",
            data_utils, 
            data_inputs)
        
        # Assert
        # Verify navset_tab was called once with proper ID
        mock_shiny_ui_components['navset_tab'].assert_called_once()
        
        navset_call_args = mock_shiny_ui_components['navset_tab'].call_args
        # The ID should be passed as a keyword argument
        assert 'id' in navset_call_args.kwargs
        assert navset_call_args.kwargs['id'] == "ID_tab_portfolios_tabs_all"


    def test_tab_portfolios_ui_with_large_datasets(self, mock_subtab_modules, mock_shiny_ui_components, mock_data_utils):
        """Test UI generation with large datasets (business logic validation)."""
        # Arrange
        data_utils = mock_data_utils
        
        # Create large datasets
        num_rows = 10000
        large_dates = [(datetime.now() - timedelta(days=idx)).strftime("%Y-%m-%d") for idx in range(num_rows)]
        large_values = [10000.0 + idx * 0.1 for idx in range(num_rows)]
        
        large_data_inputs = {
            "My_Portfolio": pl.DataFrame({"Date": large_dates, "Value": large_values}),
            "Benchmark_Portfolio": pl.DataFrame({"Date": large_dates, "Value": large_values}),
            "Weights_My_Portfolio": pl.DataFrame({"Date": large_dates[::100], "Component_One": [0.5] * 100}),
            "Time_Series_ETFs": pl.DataFrame({"Date": large_dates, "ETF_One": large_values})
        }
        
        # Act
        ui_result = tab_portfolios_ui(
            "ID_tab_portfolios",
            data_utils, 
            large_data_inputs)
        
        # Assert
        assert ui_result is not None
        
        # Verify all subtabs received the large datasets
        for ui_mock in [mock_subtab_modules['analysis_ui'], mock_subtab_modules['comparison_ui'], mock_subtab_modules['weights_ui']]:
            call_args = ui_mock.call_args
            portfolio_data = call_args[1]['data_inputs']['My_Portfolio']
            assert portfolio_data.height == num_rows


    def test_tab_portfolios_ui_module_id_naming_conventions(self, mock_subtab_modules, mock_shiny_ui_components, mock_data_utils, comprehensive_sample_data):
        """Test module ID naming conventions compliance (configuration validation)."""
        # Arrange
        data_utils = mock_data_utils
        data_inputs = comprehensive_sample_data
        
        # Act
        ui_result = tab_portfolios_ui(
            "ID_tab_portfolios",
            data_utils, 
            data_inputs)
        
        # Assert module ID naming conventions
        expected_id_patterns = [
            "ID_tab_portfolios_subtab_portfolios_analysis",
            "ID_tab_portfolios_subtab_portfolios_comparison", 
            "ID_tab_portfolios_subtab_weights_distribution"
        ]
        
        actual_ids = []
        for ui_mock in [mock_subtab_modules['analysis_ui'], mock_subtab_modules['comparison_ui'], mock_subtab_modules['weights_ui']]:
            call_args = ui_mock.call_args
            actual_ids.append(call_args[1]['id'])
        
        # Verify IDs follow project naming convention
        for actual_id in actual_ids:
            assert actual_id.startswith("ID_tab_portfolios_subtab_")
            assert len(actual_id) > 20  # Should be descriptive
            assert actual_id.replace("_", "").isalnum()  # Only alphanumeric and underscores

