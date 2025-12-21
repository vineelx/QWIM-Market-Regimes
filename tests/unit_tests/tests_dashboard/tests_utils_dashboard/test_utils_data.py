"""
Comprehensive tests for utils_data module following project coding standards.

Tests defensive programming, input validation, and error handling approaches.
"""

import pytest
import polars as pl
import pandas as pd
import sys
from pathlib import Path
from hypothesis import given, strategies as st
from unittest.mock import Mock, patch
from freezegun import freeze_time
from datetime import datetime, timedelta

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.dashboard.utils_dashboard.utils_data import (
    validate_portfolio_data,
    calculate_portfolio_returns,
    downsample_dataframe,
    get_safe_num_rows_for_DF
)


class TestValidatePortfolioData:
    """Test portfolio data validation following defensive programming standards."""
    
    def test_validate_portfolio_data_none_input(self):
        """Test validation with None input (defensive programming)."""
        # Arrange & Act
        is_valid, error_message = validate_portfolio_data(None)
        
        # Assert
        assert not is_valid
        assert "Portfolio data is None" in error_message


    def test_validate_portfolio_data_empty_dataframe(self):
        """Test validation with empty DataFrame (defensive programming)."""
        # Arrange
        empty_df = pl.DataFrame()
        
        # Act
        is_valid, error_message = validate_portfolio_data(empty_df)
        
        # Assert
        assert not is_valid
        assert "DataFrame is empty" in error_message


    def test_validate_portfolio_data_wrong_type(self):
        """Test validation with wrong data type (input validation)."""
        # Arrange
        wrong_type_data = pd.DataFrame({"Date": ["2023-01-01"], "Value": [100.0]})
        
        # Act
        is_valid, error_message = validate_portfolio_data(wrong_type_data)
        
        # Assert
        assert not is_valid
        assert "must be a Polars DataFrame" in error_message


    def test_validate_portfolio_data_missing_columns(self):
        """Test validation with missing required columns (configuration validation)."""
        # Arrange
        invalid_df = pl.DataFrame({"Price": [100.0, 101.0], "Volume": [1000, 1100]})
        
        # Act
        is_valid, error_message = validate_portfolio_data(invalid_df)
        
        # Assert
        assert not is_valid
        assert "missing required column" in error_message


    def test_validate_portfolio_data_valid_input(self):
        """Test validation with valid input (business logic validation)."""
        # Arrange
        valid_df = pl.DataFrame({
            "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "Value": [100.0, 101.0, 102.0]
        })
        
        # Act
        is_valid, error_message = validate_portfolio_data(valid_df)
        
        # Assert
        assert is_valid
        assert "validation successful" in error_message


    def test_validate_portfolio_data_duplicate_dates(self):
        """Test validation with duplicate dates (business logic validation)."""
        # Arrange
        duplicate_dates_df = pl.DataFrame({
            "Date": ["2023-01-01", "2023-01-01", "2023-01-03"],
            "Value": [100.0, 101.0, 102.0]
        })
        
        # Act
        is_valid, error_message = validate_portfolio_data(duplicate_dates_df)
        
        # Assert
        assert not is_valid
        assert "duplicate date values" in error_message


    @given(
        num_points=st.integers(min_value=2, max_value=10),
        start_value=st.floats(min_value=1.0, max_value=1000.0)
    )
    def test_validate_portfolio_data_property_based(self, num_points, start_value):
        """Property-based test for portfolio validation (hypothesis testing)."""
        # Arrange - Create valid sequential dates to avoid duplicates
        base_date = datetime(2023, 1, 1)
        dates = []
        values = []
        
        for idx in range(num_points):
            current_date = base_date + timedelta(days=idx)
            dates.append(current_date.strftime("%Y-%m-%d"))
            # Generate realistic value progression
            daily_return = 0.001 + (idx % 3) * 0.0005  # Small varying returns
            current_value = start_value * (1.001 ** idx)
            values.append(current_value)
        
        df = pl.DataFrame({
            "Date": dates,
            "Value": values
        })
        
        # Act
        is_valid, error_message = validate_portfolio_data(df)
        
        # Assert
        assert is_valid, f"Valid data should pass validation: {error_message}"


class TestCalculatePortfolioReturns:
    """Test portfolio returns calculation with defensive programming."""
    
    def test_calculate_portfolio_returns_none_input(self):
        """Test returns calculation with None input (defensive programming)."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Portfolio data is None"):
            calculate_portfolio_returns(None)


    def test_calculate_portfolio_returns_empty_dataframe(self):
        """Test returns calculation with empty DataFrame (defensive programming)."""
        # Arrange
        empty_df = pl.DataFrame()
        
        # Act
        result = calculate_portfolio_returns(empty_df)
        
        # Assert
        assert isinstance(result, pl.Series)
        assert len(result) == 0


    def test_calculate_portfolio_returns_insufficient_data(self):
        """Test returns calculation with insufficient data (business logic validation)."""
        # Arrange
        single_row_df = pl.DataFrame({
            "Date": ["2023-01-01"],
            "Value": [100.0]
        })
        
        # Act
        result = calculate_portfolio_returns(single_row_df)
        
        # Assert
        assert isinstance(result, pl.Series)
        assert len(result) == 0


    def test_calculate_portfolio_returns_valid_data(self):
        """Test returns calculation with valid data (business logic validation)."""
        # Arrange
        valid_df = pl.DataFrame({
            "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "Value": [100.0, 102.0, 104.04]
        })
        
        # Act
        result = calculate_portfolio_returns(valid_df)
        
        # Assert
        assert isinstance(result, pl.Series)
        assert len(result) == 2  # n-1 returns for n values
        assert abs(result[0] - 0.02) < 1e-10  # 2% return
        assert abs(result[1] - 0.02) < 1e-10  # 2% return


    @pytest.mark.parametrize("values,expected_returns", [
        ([100, 110, 121], [0.1, 0.1]),  # 10% returns
        ([100, 90, 81], [-0.1, -0.1]),  # -10% returns
        ([100, 100, 100], [0.0, 0.0]),  # No change
    ])
    def test_calculate_portfolio_returns_parametrized(self, values, expected_returns):
        """Parametrized test for different return scenarios."""
        # Arrange
        df = pl.DataFrame({
            "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "Value": values
        })
        
        # Act
        result = calculate_portfolio_returns(df)
        
        # Assert
        assert len(result) == len(expected_returns)
        for idx, expected in enumerate(expected_returns):
            assert abs(result[idx] - expected) < 1e-10


class TestDownsampleDataframe:
    """Test dataframe downsampling with performance considerations."""
    
    def test_downsample_dataframe_none_input(self):
        """Test downsampling with None input (defensive programming)."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="downsample_dataframe received None dataframe"):
            downsample_dataframe(None)


    def test_downsample_dataframe_wrong_type(self):
        """Test downsampling with wrong type (input validation)."""
        # Arrange
        pandas_df = pd.DataFrame({"Date": ["2023-01-01"], "Value": [100.0]})
        
        # Act & Assert
        with pytest.raises(TypeError, match="must be a Polars DataFrame"):
            downsample_dataframe(pandas_df)


    def test_downsample_dataframe_small_dataset(self):
        """Test downsampling with dataset smaller than max_points (business logic)."""
        # Arrange
        small_df = pl.DataFrame({
            "Date": ["2023-01-01", "2023-01-02"],
            "Value": [100.0, 101.0]
        })
        
        # Act
        result = downsample_dataframe(small_df, max_points=200)
        
        # Assert
        assert result.height == 2  # Should return unchanged
        assert result.equals(small_df)


    def test_downsample_dataframe_large_dataset(self):
        """Test downsampling with large dataset (performance optimization)."""
        # Arrange - Create valid date sequence
        date_range = []
        base_date = datetime(2023, 1, 1)
        
        for idx in range(300):
            current_date = base_date + timedelta(days=idx)
            date_range.append(current_date.strftime("%Y-%m-%d"))
        
        large_df = pl.DataFrame({
            "Date": date_range,
            "Value": [100.0 + idx for idx in range(300)]
        })
        
        # Act
        result = downsample_dataframe(large_df, max_points=100)
        
        # Assert
        assert result.height <= 100
        assert result.height > 0
        assert "Date" in result.columns
        assert "Value" in result.columns


    @pytest.mark.benchmark(group="downsampling")
    def test_downsample_dataframe_performance(self, benchmark):
        """Benchmark test for downsampling performance."""
        # Arrange - Create valid date sequence
        date_range = []
        base_date = datetime(2023, 1, 1)
        
        for idx in range(1000):
            current_date = base_date + timedelta(days=idx)
            date_range.append(current_date.strftime("%Y-%m-%d"))
        
        large_df = pl.DataFrame({
            "Date": date_range,
            "Value": [100.0 + idx * 0.1 for idx in range(1000)]
        })
        
        # Act & Assert
        result = benchmark(downsample_dataframe, large_df, max_points=200)
        assert result.height <= 200


class TestGetSafeNumRowsForDf:
    """Test safe row count functionality with defensive programming."""
    
    def test_get_safe_num_rows_for_df_none_input(self):
        """Test safe row count with None input (defensive programming)."""
        # Arrange & Act
        result = get_safe_num_rows_for_DF(None)
        
        # Assert
        assert result == 0


    def test_get_safe_num_rows_for_df_empty_dataframe(self):
        """Test safe row count with empty DataFrame (defensive programming)."""
        # Arrange
        empty_df = pl.DataFrame()
        
        # Act
        result = get_safe_num_rows_for_DF(empty_df)
        
        # Assert
        assert result == 0


    def test_get_safe_num_rows_for_df_valid_dataframe(self):
        """Test safe row count with valid DataFrame (business logic validation)."""
        # Arrange
        valid_df = pl.DataFrame({
            "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "Value": [100.0, 101.0, 102.0]
        })
        
        # Act
        result = get_safe_num_rows_for_DF(valid_df)
        
        # Assert
        assert result == 3


class TestIntegrationUtilsData:
    """Integration tests for utils_data module functions."""
    
    def test_full_pipeline_integration(self):
        """Test complete data processing pipeline (integration test)."""
        # Arrange
        test_data = pl.DataFrame({
            "Date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
            "Value": [100.0, 102.0, 104.04, 106.1208]
        })
        
        # Act
        # Step 1: Validate data
        is_valid, error_msg = validate_portfolio_data(test_data)
        assert is_valid, f"Data validation failed: {error_msg}"
        
        # Step 2: Calculate returns
        returns = calculate_portfolio_returns(test_data)
        assert len(returns) == 3
        
        # Step 3: Downsample if needed
        downsampled = downsample_dataframe(test_data, max_points=200)
        assert downsampled.height == 4  # Small dataset, no downsampling
        
        # Step 4: Get safe row count
        row_count = get_safe_num_rows_for_DF(downsampled)
        assert row_count == 4


    @pytest.mark.slow
    def test_large_dataset_integration(self):
        """Integration test with large dataset (marked as slow)."""
        # Arrange - Create large dataset with valid dates
        date_range = []
        value_range = []
        
        base_date = datetime(2020, 1, 1)
        base_value = 1000.0
        growth_rate = 1.001  # 0.1% daily growth
        
        for idx in range(5000):
            current_date = base_date + timedelta(days=idx)
            date_range.append(current_date.strftime("%Y-%m-%d"))
            value_range.append(base_value * (growth_rate ** idx))
        
        large_data = pl.DataFrame({
            "Date": date_range,
            "Value": value_range
        })
        
        # Act & Assert - Full pipeline
        is_valid, _ = validate_portfolio_data(large_data)
        assert is_valid
        
        returns = calculate_portfolio_returns(large_data)
        assert len(returns) == 4999
        
        downsampled = downsample_dataframe(large_data, max_points=200)
        assert downsampled.height <= 200


# Fixtures for test data following project naming standards
@pytest.fixture
def valid_portfolio_data():
    """Fixture providing valid portfolio data for testing."""
    return pl.DataFrame({
        "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Value": [100.0, 102.0, 104.04]
    })


@pytest.fixture
def large_portfolio_data():
    """Fixture providing large portfolio dataset for performance testing."""
    date_range = []
    value_range = []
    
    base_date = datetime(2020, 1, 1)
    base_value = 1000.0
    growth_rate = 1.001  # 0.1% daily growth
    
    for idx in range(1000):
        current_date = base_date + timedelta(days=idx)
        date_range.append(current_date.strftime("%Y-%m-%d"))
        value_range.append(base_value * (growth_rate ** idx))
    
    return pl.DataFrame({
        "Date": date_range,
        "Value": value_range
    })


@pytest.fixture
def invalid_portfolio_data_duplicate_dates():
    """Fixture providing invalid portfolio data with duplicate dates."""
    return pl.DataFrame({
        "Date": ["2023-01-01", "2023-01-01", "2023-01-03"],
        "Value": [100.0, 101.0, 102.0]
    })


@pytest.fixture
def portfolio_weights_data():
    """Fixture providing multi-component portfolio weights data."""
    return pl.DataFrame({
        "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Component_One": [0.25, 0.26, 0.24],
        "Component_Two": [0.30, 0.29, 0.31],
        "Component_Three": [0.20, 0.21, 0.19],
        "Component_Four": [0.15, 0.14, 0.16],
        "Component_Five": [0.10, 0.10, 0.10]
    })


# Helper functions following project coding standards
def create_test_portfolio_data_with_valid_dates(num_points: int = 10, start_value: float = 100.0):
    """
    Helper function to create test portfolio data with valid sequential dates.
    
    Parameters:
        num_points (int): Number of data points to generate
        start_value (float): Starting portfolio value
        
    Returns:
        pl.DataFrame: Generated portfolio data with sequential dates
        
    Notes:
        - Follows project naming standards
        - Uses defensive programming principles
        - Creates realistic data progression with no duplicate dates
    """
    # Input validation with early returns
    if num_points < 1:
        return pl.DataFrame()
    
    if start_value <= 0:
        start_value = 100.0
    
    # Generate realistic portfolio data with sequential dates
    dates = []
    values = []
    
    base_date = datetime(2023, 1, 1)
    current_value = start_value
    
    for idx in range(num_points):
        current_date = base_date + timedelta(days=idx)
        dates.append(current_date.strftime("%Y-%m-%d"))
        
        # Add some realistic volatility
        daily_return = 0.001 + (idx % 5) * 0.0005  # Varying returns
        current_value *= (1 + daily_return)
        values.append(current_value)
    
    return pl.DataFrame({
        "Date": dates,
        "Value": values
    })


# Configuration for test execution
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=utils_data", "--cov-report=html"])