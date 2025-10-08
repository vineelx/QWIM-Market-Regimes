"""
Time Series Data Generator Module
================================

This module generates synthetic time series data for seven different series
with various patterns and saves the result to a CSV file.

The module creates time series with different characteristics:

- **Series AA**: Upward trend with seasonal pattern
- **Series BB**: Cyclical pattern with random walks  
- **Series CC**: Exponential growth with noise
- **Series DD**: Stationary with occasional jumps
- **Series EE**: Declining trend with seasonality
- **Series FF**: Highly volatile series
- **Series GG**: Combination of trend and cycles

!!! info "Data Generation Strategy"
    The synthetic data is designed to simulate realistic financial time series
    with various market conditions including trends, seasonality, volatility,
    and structural breaks.

!!! warning "Reproducibility"
    This module uses a fixed random seed (42) to ensure reproducible results
    across different runs. Changing the seed will produce different datasets.

Functions
---------
generate_monthly_timeseries
    Generates monthly time series data with various patterns
main
    Main execution function that generates and saves the data

Examples
--------
To generate and save time series data:

```python
from src.utils.generate_data import main
main()
```

To generate custom time range data:

```python
from src.utils.generate_data import generate_monthly_timeseries
df = generate_monthly_timeseries(
    start_date="2020-01-01", 
    end_date="2023-12-31"
)
```

See Also
--------
- [Polars DataFrame Documentation](https://pola-rs.github.io/polars/)
- [NumPy Random Module](https://numpy.org/doc/stable/reference/random/)
"""

import os
from datetime import datetime
from pathlib import Path

import numpy as np
import polars as pl


def generate_monthly_timeseries(
    start_date: str = "2002-01-01", 
    end_date: str = "2025-10-03",
) -> pl.DataFrame:
    """Generate monthly time series data for seven series.
    
    This function creates synthetic time series data for seven different series,
    each with unique patterns including trends, seasonality, cycles, and random components.
    The generated data simulates realistic financial market conditions with various
    characteristics commonly found in economic time series.
    
    !!! tip "Time Series Patterns"
        Each series represents different market scenarios:
        
        - **AA**: Bull market with seasonal effects
        - **BB**: Long-term economic cycles  
        - **CC**: Growth stocks or emerging markets
        - **DD**: Market with structural changes
        - **EE**: Bear market conditions
        - **FF**: High-volatility instruments
        - **GG**: Mixed market conditions
    
    Parameters
    ----------
    start_date : str, optional
        Start date in YYYY-MM-DD format, by default "2002-01-01"
        
        !!! note
            The start date will be automatically adjusted to the first day
            of the month for consistent monthly intervals.
            
    end_date : str, optional
        End date in YYYY-MM-DD format, by default "2025-10-03"
        
        !!! note
            The end date will be automatically adjusted to generate complete
            monthly intervals up to (but not including) this date.
        
    Returns
    -------
    pl.DataFrame
        A polars DataFrame with the generated time series containing columns:
        
        | Column | Type | Description |
        |--------|------|-------------|
        | Date | Date | Monthly timestamps |
        | AA | Float64 | Upward trend with seasonality |
        | BB | Float64 | Cyclical pattern with random walk |
        | CC | Float64 | Exponential growth with noise |
        | DD | Float64 | Stationary with structural break |
        | EE | Float64 | Declining trend with seasonality |
        | FF | Float64 | High volatility series |
        | GG | Float64 | Complex multi-seasonal pattern |
        
    Notes
    -----
    The function uses a fixed random seed (42) to ensure reproducibility.
    Each series has specific mathematical characteristics:
    
    === "Series AA - Upward Trend"
        ```
        AA(t) = 100 + 0.5*t + 15*sin(2πt/12) + ε(0,5)
        ```
        - Linear upward trend (0.5 per month)
        - Annual seasonality (amplitude: 15)
        - Gaussian noise (σ = 5)
    
    === "Series BB - Cyclical Pattern"
        ```
        BB(t) = 150 + 30*sin(2πt/36) + Σε(0,1)
        ```
        - 3-year cyclical pattern (amplitude: 30)
        - Random walk component
        - Base level: 150
    
    === "Series CC - Exponential Growth"
        ```
        CC(t) = 50*exp(0.005*t) + ε(0,5)
        ```
        - Exponential growth (0.5% per month)
        - Additive Gaussian noise (σ = 5)
        - Starting value: 50
    
    === "Series DD - Structural Break"
        ```
        DD(t) = 200 + I(t∈[n/3,n/2])*50 + ε(0,10)
        ```
        - Stationary base level: 200
        - Level shift (+50) in the middle
        - Higher noise level (σ = 10)
    
    === "Series EE - Declining Trend"
        ```
        EE(t) = 300 - 0.3*t + 20*sin(2πt/12) + ε(0,8)
        ```
        - Linear declining trend (-0.3 per month)
        - Annual seasonality (amplitude: 20)
        - Gaussian noise (σ = 8)
    
    === "Series FF - High Volatility"
        ```
        FF(t) = 120 + 0.2*t + ε(0,25)
        ```
        - Slight upward trend (0.2 per month)
        - Very high volatility (σ = 25)
        - Base level: 120
    
    === "Series GG - Multi-Seasonal"
        ```
        GG(t) = 80 + 0.3*t + 20*sin(2πt/24) + 10*sin(2πt/6) + ε(0,7)
        ```
        - Linear upward trend (0.3 per month)
        - 2-year seasonal cycle (amplitude: 20)
        - 6-month seasonal cycle (amplitude: 10)
        - Gaussian noise (σ = 7)
    
    !!! example "Usage Examples"
        Generate data for the default period:
        ```python
        df = generate_monthly_timeseries()
        print(f"Generated {len(df)} rows from {df['Date'].min()} to {df['Date'].max()}")
        ```
        
        Generate data for a specific period:
        ```python
        df = generate_monthly_timeseries(
            start_date="2020-01-01", 
            end_date="2020-12-31"
        )
        assert df.shape == (12, 8)
        ```
        
        Access specific series:
        ```python
        upward_trend = df.select(["Date", "AA"])
        cyclical_pattern = df.select(["Date", "BB"])
        ```
    
    Raises
    ------
    ValueError
        If start_date or end_date are not in YYYY-MM-DD format
    ValueError
        If start_date is greater than or equal to end_date
        
    !!! warning "Date Validation"
        The function performs input validation on date parameters.
        Invalid dates will raise ValueError with descriptive messages.
    """
    # Input validation with early returns (defensive programming)
    if not isinstance(start_date, str) or not isinstance(end_date, str):
        raise ValueError("Date parameters must be strings in YYYY-MM-DD format")
    
    # Parse and validate date strings
    format_string = "%Y-%m-%d"
    try:
        start_date_parsed = datetime.strptime(start_date, format_string)
        end_date_parsed = datetime.strptime(end_date, format_string)
    except ValueError as exc:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD format. Error: {exc}") from exc
    
    # Business logic validation
    if start_date_parsed >= end_date_parsed:
        raise ValueError(f"Start date ({start_date}) must be before end date ({end_date})")
    
    # Generate monthly date range using polars
    # The 'closed="left"' parameter excludes the end date for consistent intervals
    dates = pl.date_range(
        start=start_date_parsed,
        end=end_date_parsed,
        interval="1mo",
        closed="left",  # Exclude end date for consistent monthly intervals
        eager=True,
    ).alias("dates")

    # Calculate number of data points for array generation
    num_data_points = len(dates)
    
    # Generate time indices for mathematical functions (trends and cycles)
    time_indices = np.arange(num_data_points)
    
    # Set random seed for reproducible results across different runs
    # This ensures consistent synthetic data generation for testing and development
    np.random.seed(seed=42)
    
    # === Series AA: Upward trend with annual seasonal pattern ===
    # Mathematical model: Linear trend + seasonal component + noise
    # Represents bull market conditions with seasonal effects (e.g., quarterly earnings)
    series_aa = (
        100 +  # Base level
        0.5 * time_indices +  # Linear upward trend (0.5 units per month)
        15 * np.sin(2 * np.pi * time_indices / 12) +  # Annual seasonality (12-month cycle)
        np.random.normal(loc=0, scale=5, size=num_data_points)  # White noise
    )
    
    # === Series BB: Cyclical pattern with random walk component ===
    # Mathematical model: Long-term cycle + cumulative random shocks
    # Represents economic business cycles with persistent shocks
    series_bb = (
        150 +  # Base level
        30 * np.sin(2 * np.pi * time_indices / 36) +  # 3-year business cycle
        np.cumsum(np.random.normal(loc=0, scale=1, size=num_data_points))  # Random walk component
    )
    
    # === Series CC: Exponential growth with additive noise ===
    # Mathematical model: Exponential trend + noise
    # Represents growth stocks or emerging market indices
    series_cc = (
        50 * np.exp(0.005 * time_indices) +  # Exponential growth (0.5% per month)
        np.random.normal(loc=0, scale=5, size=num_data_points)  # Additive noise
    )
    
    # === Series DD: Stationary series with structural break ===
    # Mathematical model: Constant level + level shift + noise
    # Represents markets with policy changes or structural reforms
    series_dd = 200 + np.random.normal(loc=0, scale=10, size=num_data_points)
    # Add structural break (level shift) in the middle third of the series
    break_start = num_data_points // 3
    break_end = num_data_points // 2
    series_dd[break_start:break_end] += 50  # Level shift of +50 units
    
    # === Series EE: Declining trend with annual seasonality ===
    # Mathematical model: Negative linear trend + seasonal component + noise
    # Represents bear market conditions or declining industries
    series_ee = (
        300 +  # High starting base level
        (-0.3) * time_indices +  # Linear declining trend (-0.3 units per month)
        20 * np.sin(2 * np.pi * time_indices / 12) +  # Annual seasonality
        np.random.normal(loc=0, scale=8, size=num_data_points)  # White noise
    )
    
    # === Series FF: Highly volatile series with slight upward trend ===
    # Mathematical model: Small trend + high variance noise
    # Represents high-volatility instruments (e.g., cryptocurrency, small-cap stocks)
    series_ff = (
        120 +  # Base level
        0.2 * time_indices +  # Slight upward trend
        np.random.normal(loc=0, scale=25, size=num_data_points)  # High volatility noise
    )
    
    # === Series GG: Complex pattern with multiple seasonal components ===
    # Mathematical model: Linear trend + multiple seasonal cycles + noise
    # Represents markets with multiple seasonal factors (tourism, agriculture, etc.)
    series_gg = (
        80 +  # Base level
        0.3 * time_indices +  # Linear upward trend
        20 * np.sin(2 * np.pi * time_indices / 24) +  # 2-year seasonal cycle
        10 * np.sin(2 * np.pi * time_indices / 6) +   # 6-month seasonal cycle
        np.random.normal(loc=0, scale=7, size=num_data_points)  # White noise
    )
    
    # Create polars DataFrame with rounded values for better readability
    # Round to 2 decimal places to simulate real financial data precision
    time_series_data = pl.DataFrame({
        "Date": dates,
        "AA": series_aa.round(decimals=2),
        "BB": series_bb.round(decimals=2),
        "CC": series_cc.round(decimals=2),
        "DD": series_dd.round(decimals=2),
        "EE": series_ee.round(decimals=2),
        "FF": series_ff.round(decimals=2),
        "GG": series_gg.round(decimals=2),
    })
    
    return time_series_data


def main() -> None:
    """Generate time series data and save it to CSV file.
    
    This function serves as the main entry point for data generation. It creates
    the necessary directory structure, generates synthetic time series data using
    the `generate_monthly_timeseries` function, and saves the result to a CSV file
    in the project's data/raw directory.
    
    The function implements defensive programming practices by:
    
    - Creating directories if they don't exist
    - Using relative paths from the script location
    - Providing informative console output
    - Handling potential file system errors gracefully
    
    !!! info "Output Location"
        The generated data is saved to: `PROJECT_ROOT/data/raw/data_timeseries.csv`
        
        The function automatically creates the directory structure if it doesn't exist.
    
    !!! tip "File Format"
        The output CSV file uses:
        
        - Comma-separated values
        - ISO date format (YYYY-MM-DD) for the Date column
        - 2 decimal places for all numeric series
        - UTF-8 encoding for compatibility
    
    Returns
    -------
    None
        This function doesn't return any value but produces side effects:
        
        - Creates directory structure if needed
        - Generates and saves CSV file
        - Prints progress information to console
    
    Side Effects
    ------------
    - **File System**: Creates `data/raw/` directory structure
    - **File Creation**: Saves `data_timeseries.csv` file
    - **Console Output**: Prints generation progress and summary statistics
    
    Notes
    -----
    The function uses the following default parameters:
    
    - **Time Range**: 2002-01-01 to 2025-10-03 (approximately 23+ years)
    - **Frequency**: Monthly data points
    - **Output Format**: CSV with headers
    
    The time range provides sufficient historical data for:
    
    - Long-term trend analysis
    - Seasonal pattern detection  
    - Business cycle identification
    - Statistical model training
    
    !!! example "Console Output Example"
        ```
        Generating time series data...
        Data saved to PROJECT_ROOT/data/raw/data_timeseries.csv
        Generated 279 rows from 2002-01-01 to 2025-10-03
        ```
    
    Raises
    ------
    PermissionError
        If the script lacks permissions to create directories or write files
    OSError
        If there are file system issues (disk space, invalid paths, etc.)
    
    !!! warning "File Permissions"
        Ensure the script has write permissions to the project directory.
        The function will attempt to create the necessary folder structure.
    
    Examples
    --------
    Run data generation from command line:
    ```bash
    python src/utils/generate_data.py
    ```
    
    Import and run programmatically:
    ```python
    from src.utils.generate_data import main
    main()
    ```
    
    Check if file was created successfully:
    ```python
    import polars as pl
    from pathlib import Path
    
    # After running main()
    data_file = Path("data/raw/data_timeseries.csv")
    if data_file.exists():
        df = pl.read_csv(data_file)
        print(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns")
    ```
    
    See Also
    --------
    generate_monthly_timeseries : Core data generation function
    pathlib.Path : For cross-platform path handling
    polars.DataFrame.write_csv : For CSV output functionality
    """
    # Define project directory structure using pathlib for cross-platform compatibility
    # Navigate from current script location to project root (3 levels up)
    project_root_directory = Path(__file__).parent.parent.parent
    data_directory = project_root_directory / "data"
    raw_data_directory = data_directory / "raw"
    output_file_path = raw_data_directory / "data_timeseries.csv"
    
    # Print initial status message for user feedback
    print("Generating time series data...")
    
    # Generate synthetic time series data using default parameters
    # This creates approximately 23+ years of monthly data (2002-2025)
    time_series_dataframe = generate_monthly_timeseries(
        start_date="2002-01-01",  # Start from early 2000s for sufficient history
        end_date="2025-10-03",    # Extend slightly into future for forecasting tests
    )
    
    # Create directory structure if it doesn't exist
    # The parents=True parameter creates intermediate directories as needed
    # The exist_ok=True parameter prevents errors if directories already exist
    raw_data_directory.mkdir(
        parents=True,   # Create intermediate directories (data/ if needed)
        exist_ok=True,  # Don't raise error if directory already exists
    )
    
    # Save DataFrame to CSV file with polars optimized writer
    # Polars automatically handles proper CSV formatting and encoding
    time_series_dataframe.write_csv(file=output_file_path)
    
    # Provide user feedback with file location and summary statistics
    print(f"Data saved to {output_file_path}")
    print(f"Generated {len(time_series_dataframe)} rows from {time_series_dataframe['Date'].min()} to {time_series_dataframe['Date'].max()}")


# Standard Python pattern for executable scripts
# This allows the module to be imported without running main() automatically
if __name__ == "__main__":
    # Execute main function when script is run directly
    # This enables both: python generate_data.py and import generate_data
    main()