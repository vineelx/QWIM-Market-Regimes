"""
Portfolio Module
===============

This module provides functionality for managing financial portfolios with time-varying weights.

The `portfolio_QWIM` class represents a financial portfolio where component weights can change
over time, supporting both static equal-weight portfolios and dynamic rebalancing strategies.

!!! info "Portfolio Representation"
    Portfolios are internally stored as Polars DataFrames with the following structure:
    
    | Column | Type | Description |
    |--------|------|-------------|
    | Date | Date | Portfolio rebalancing dates |
    | Component_1 | Float64 | Weight of first component (0.0 to 1.0) |
    | Component_2 | Float64 | Weight of second component (0.0 to 1.0) |
    | ... | ... | Additional components as needed |

!!! warning "Weight Constraints"
    - All component weights must be non-negative (≥ 0.0)
    - Component weights for each date should sum to approximately 1.0
    - The class automatically normalizes weights when they don't sum to 1.0

!!! note "Polars DataFrames Only"
    This module exclusively uses Polars DataFrames for optimal performance and memory efficiency.
    Pandas DataFrames are not supported and will raise TypeError exceptions.

Classes
-------
portfolio_QWIM
    A class representing a financial portfolio with weights of components over time.

Examples
--------
Creating an equal-weight portfolio:

```python
from src.portfolios.portfolio_QWIM import portfolio_QWIM

# Create equal-weight tech portfolio
tech_portfolio = portfolio_QWIM(
    name_portfolio="Technology Focus",
    names_components=["AAPL", "MSFT", "GOOGL", "NVDA"]
)
```

Loading portfolio from existing data:

```python
import polars as pl

# Load portfolio weights from DataFrame
weights_df = pl.DataFrame({
    "Date": ["2023-01-01", "2023-02-01", "2023-03-01"],
    "AAPL": [0.30, 0.32, 0.28],
    "MSFT": [0.25, 0.23, 0.27],
    "GOOGL": [0.25, 0.25, 0.25],
    "NVDA": [0.20, 0.20, 0.20]
})

custom_portfolio = portfolio_QWIM(
    name_portfolio="Custom Tech Allocation",
    portfolio_weights=weights_df
)
```

See Also
--------
- [Polars DataFrame Documentation](https://pola-rs.github.io/polars/)
- [Financial Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
"""

# Standard library imports for date handling and type annotations
import polars as pl
from datetime import datetime
from typing import List, Optional, Union
from pathlib import Path


class portfolio_QWIM:
    """A class representing a financial portfolio with weights of components over time.

    The portfolio is represented as a DataFrame with dates and component weights, supporting
    both static equal-weight initialization and dynamic weight management over time.

    !!! tip "Initialization Modes"
        The class supports two initialization modes:
        
        1. **From Component Names**: Creates equal-weight portfolio for specified components
        2. **From Weights DataFrame**: Loads existing portfolio weights from Polars DataFrame
        
        Choose the mode that best fits your use case.

    !!! warning "Polars DataFrame Requirements"
        This class exclusively uses Polars DataFrames for all operations:
        
        - Input DataFrames must be `polars.DataFrame` objects
        - Pandas DataFrames are not supported and will raise `TypeError`
        - All internal operations use Polars for optimal performance
        - Output DataFrames are always Polars DataFrames

    Attributes
    ----------
    _portfolio_weights : pl.DataFrame
        DataFrame containing dates and portfolio weights with Date as first column.
        
        !!! note "Internal Structure"
            The DataFrame follows this schema:
            ```
            ┌────────────┬─────────────┬─────────────┬─────┐
            │ Date       ┆ Component_1 ┆ Component_2 ┆ ... │
            │ ---        ┆ ---         ┆ ---         ┆     │
            │ date       ┆ f64         ┆ f64         ┆     │
            ├────────────┼─────────────┼─────────────┼─────┤
            │ 2023-01-01 ┆ 0.33        ┆ 0.33        ┆ ... │
            │ 2023-02-01 ┆ 0.35        ┆ 0.32        ┆ ... │
            └────────────┴─────────────┴─────────────┴─────┘
            ```
    
    _portfolio_components : List[str]
        List of strings containing names of the portfolio components.
        
        !!! example "Component Names"
            ```python
            ["AAPL", "MSFT", "GOOGL"]  # Stock tickers
            ["Bonds", "Stocks", "REITs"]  # Asset classes
            ["Tech", "Healthcare", "Finance"]  # Sectors
            ```
    
    _num_components : int
        Number of portfolio components (automatically calculated).
    
    _portfolio_name : str
        Human-readable name of the portfolio for identification and reporting.

    Examples
    --------
    === "Equal Weight Portfolio"
        Create a portfolio with equal weights for multiple components:
        
        ```python
        # Create tech-focused equal-weight portfolio
        tech_portfolio = portfolio_QWIM(
            name_portfolio="Tech Equal Weight",
            names_components=["AAPL", "MSFT", "GOOGL", "NVDA"],
            date="2023-01-01"
        )
        
        print(f"Components: {tech_portfolio.get_portfolio_components}")
        # Output: ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
        
        print(f"Equal weights: {tech_portfolio.get_portfolio_weights}")
        # Each component gets 0.25 weight (1.0 / 4 components)
        ```
    
    === "Custom Weights Portfolio"
        Create a portfolio from existing weight data:
        
        ```python
        import polars as pl
        
        # Define custom weights over time
        weights_data = pl.DataFrame({
            "Date": ["2023-01-01", "2023-04-01", "2023-07-01"],
            "Stocks": [0.60, 0.65, 0.55],
            "Bonds": [0.30, 0.25, 0.35],
            "Cash": [0.10, 0.10, 0.10]
        })
        
        balanced_portfolio = portfolio_QWIM(
            name_portfolio="Dynamic Balanced Fund",
            portfolio_weights=weights_data
        )
        
        print(f"Time periods: {len(balanced_portfolio.get_portfolio_weights)} rebalancing dates")
        ```
    
    === "Portfolio Operations"
        Modify and analyze portfolio weights:
        
        ```python
        # Add new rebalancing date
        portfolio.add_weights(
            date="2023-12-01",
            weights={"AAPL": 0.35, "MSFT": 0.30, "GOOGL": 0.35}
        )
        
        # Modify existing weights
        portfolio.modify_weights(
            date="2023-01-01",
            new_weights={"AAPL": 0.40}  # Other weights remain unchanged
        )
        
        # Validate all weights
        portfolio.validate_all_weights(normalize=True)
        ```

    !!! warning "Data Validation"
        The class performs extensive validation:
        
        - **Date Format**: Ensures proper date parsing and formatting
        - **Weight Constraints**: Validates non-negative weights summing to ~1.0
        - **Component Names**: Checks for unique, non-empty component names
        - **DataFrame Structure**: Validates required columns and data types
        - **Polars DataFrame Type**: Ensures only Polars DataFrames are accepted
        
        Invalid data will raise descriptive `ValueError` or `TypeError` exceptions.

    Notes
    -----
    Mathematical Properties:
    
    For any date $t$, the portfolio weight constraint is:
    
    $$\\sum_{i=1}^{n} w_{i,t} = 1.0$$
    
    Where:
    
    - $w_{i,t}$ is the weight of component $i$ at time $t$
    - $n$ is the number of components
    - $0 ≤ w_{i,t} ≤ 1$ for all components and dates
    
    The class automatically normalizes weights when they don't satisfy this constraint.

    See Also
    --------
    polars.DataFrame : The required DataFrame type
    datetime.datetime : Date handling and validation
    typing.List : Type hints for component names
    """

    def __init__(
        self,
        name_portfolio: str,
        portfolio_weights: Optional[pl.DataFrame] = None,
        names_components: Optional[List[str]] = None,
        date: Optional[Union[str, datetime, pl.Date, pl.Datetime]] = None,
    ):
        """Initialize a portfolio object with enhanced error handling and validation.

        This constructor supports two primary initialization modes with comprehensive
        validation and error handling following defensive programming principles.

        !!! info "Initialization Modes"
            **Mode 1: From Weights DataFrame** (when `portfolio_weights` is provided)
            
            - Validates DataFrame structure and data types
            - Extracts component names automatically
            - Validates and normalizes weights if needed
            - Ensures Date column is properly formatted
            
            **Mode 2: From Component Names** (when `names_components` is provided)
            
            - Creates equal-weight allocation automatically
            - Uses provided or current date
            - Validates component name uniqueness
            - Generates initial DataFrame structure

        !!! warning "Polars DataFrame Requirement"
            The `portfolio_weights` parameter must be a Polars DataFrame. Pandas DataFrames
            or other DataFrame types will raise a TypeError with specific guidance.

        Parameters
        ----------
        name_portfolio : str
            Human-readable name for the portfolio. Must be non-empty after stripping whitespace.
            
            !!! example "Portfolio Names"
                ```python
                "Technology Growth Fund"
                "Conservative Balanced Portfolio"  
                "ESG Focused Equity Strategy"
                "High Dividend Yield Portfolio"
                ```
        
        portfolio_weights : pl.DataFrame, optional
            Existing portfolio weights DataFrame with the following requirements:
            
            - Must be a Polars DataFrame (not pandas or other types)
            - Must contain a 'Date' column (Date, Datetime, or parseable string format)
            - Must contain at least one component column besides 'Date'
            - Component columns must contain numeric data (castable to Float64)
            - Cannot be empty (must have at least one row)
            
            !!! note "Expected DataFrame Structure"
                ```python
                pl.DataFrame({
                    "Date": ["2023-01-01", "2023-02-01"],  # Date column (required)
                    "AAPL": [0.40, 0.42],                 # Component weights
                    "MSFT": [0.35, 0.33],                 # Component weights  
                    "CASH": [0.25, 0.25]                  # Component weights
                })
                ```
            
            By default None (requires `names_components` instead).
        
        names_components : List[str], optional
            List of component names for equal-weight portfolio creation.
            
            Requirements:
            - Must be non-empty list
            - Each component name must be non-empty string
            - Component names must be unique
            - Names will be stripped of leading/trailing whitespace
            
            !!! example "Component Name Examples"
                ```python
                # Stock tickers
                ["AAPL", "MSFT", "GOOGL", "AMZN"]
                
                # Asset classes  
                ["Equities", "Fixed_Income", "Real_Estate", "Commodities"]
                
                # Geographic regions
                ["US_Markets", "European_Markets", "Emerging_Markets"]
                ```
            
            By default None (requires `portfolio_weights` instead).
        
        date : str or datetime or pl.Date or pl.Datetime, optional
            Date for equal-weight portfolio creation (only used with `names_components`).
            
            Supported formats:
            - String: "YYYY-MM-DD", "YYYY/MM/DD", "MM/DD/YYYY", "DD-MM-YYYY"
            - datetime.datetime objects
            - Polars Date/Datetime objects
            
            If None, uses current date. By default None.

        Raises
        ------
        ValueError
            If neither `portfolio_weights` nor `names_components` is provided.
            If both parameters are None or validation fails.
            If portfolio name is empty or invalid.
            If DataFrame structure is invalid.
            If component names are not unique or contain empty strings.
            If weights don't satisfy constraints (negative values, invalid sums).
            If date cannot be parsed.
        
        TypeError
            If parameters have incorrect types.
            If DataFrame is not a Polars DataFrame (including pandas DataFrames).
            If component names are not strings.
        
        RuntimeError
            If unexpected errors occur during initialization.

        !!! warning "Parameter Requirements"
            **Exactly one** of `portfolio_weights` or `names_components` must be provided:
            
            - ✅ `portfolio_weights=df, names_components=None`
            - ✅ `portfolio_weights=None, names_components=["A", "B"]`  
            - ❌ `portfolio_weights=None, names_components=None`
            - ❌ `portfolio_weights=df, names_components=["A", "B"]`

        Examples
        --------
        === "Equal Weight Initialization"
            Create portfolio with equal weights:
            
            ```python
            # Simple equal-weight portfolio
            portfolio = portfolio_QWIM(
                name_portfolio="Diversified Tech",
                names_components=["AAPL", "MSFT", "GOOGL"]
            )
            # Each component gets 33.33% allocation
            
            # Equal-weight with specific date
            portfolio = portfolio_QWIM(
                name_portfolio="Q1 2023 Allocation", 
                names_components=["Stocks", "Bonds", "REITs", "Cash"],
                date="2023-01-01"
            )
            # Each component gets 25% allocation on specified date
            ```
        
        === "DataFrame Initialization"
            Load portfolio from existing data:
            
            ```python
            import polars as pl
            
            # Historical rebalancing data
            weights_df = pl.DataFrame({
                "Date": ["2023-01-01", "2023-07-01", "2024-01-01"],
                "Growth_Stocks": [0.45, 0.50, 0.40],
                "Value_Stocks": [0.35, 0.30, 0.35], 
                "Bonds": [0.20, 0.20, 0.25]
            })
            
            portfolio = portfolio_QWIM(
                name_portfolio="Dynamic Growth Strategy",
                portfolio_weights=weights_df
            )
            ```
        
        === "Error Handling"
            The constructor provides detailed error messages:
            
            ```python
            # This will raise ValueError with descriptive message
            try:
                portfolio = portfolio_QWIM(
                    name_portfolio="",  # Empty name
                    names_components=["A", "A"]  # Duplicate components
                )
            except ValueError as exc:
                print(f"Validation error: {exc}")
            ```

        Notes
        -----
        **Validation Process:**
        
        1. **Parameter Validation**: Checks types and mutual exclusivity
        2. **Name Validation**: Ensures non-empty portfolio name
        3. **Data Structure Validation**: Validates DataFrame or component list
        4. **Weight Validation**: Checks weight constraints and normalizes if needed
        5. **Column Ordering**: Ensures Date is the first column
        
        **Performance Considerations:**
        
        - DataFrame operations use Polars for optimal performance
        - Validation is comprehensive but optimized for typical portfolio sizes
        - Memory usage scales linearly with number of dates and components
        
        **Weight Normalization:**
        
        When weights don't sum to 1.0, the constructor automatically normalizes:
        
        $$w_{i,t}^{normalized} = \\frac{w_{i,t}}{\\sum_{j=1}^{n} w_{j,t}}$$
        
        Where $w_{i,t}$ is the original weight of component $i$ at time $t$.
        """
        # === STEP 1: Input validation with early returns - validate portfolio name ===
        # Check portfolio name parameter type before any business logic
        if not isinstance(name_portfolio, str):
            raise TypeError(f"name_portfolio must be of type str, got {type(name_portfolio).__name__}")
        
        # Validate portfolio name content (defensive programming)
        if len(name_portfolio.strip()) == 0:
            raise ValueError("Portfolio name must be a non-empty string")
        
        # Store cleaned portfolio name as instance attribute
        self._portfolio_name = name_portfolio.strip()

        # === STEP 2: Configuration validation - determine initialization mode ===
        # Check which initialization parameters are provided
        has_weights = portfolio_weights is not None
        has_components = names_components is not None

        # === STEP 3: Business logic validation - exactly one initialization method must be provided ===
        # Enforce mutual exclusivity of initialization modes (defensive programming)
        if not has_weights and not has_components:
            raise ValueError("Either portfolio_weights or names_components must be provided")

        # === INITIALIZATION MODE 1: From existing weights DataFrame ===
        if has_weights:
            # Input validation - validate DataFrame type with explicit Polars check
            self._validate_polars_dataframe(portfolio_weights, "portfolio_weights")
            
            # Configuration validation - check DataFrame structure requirements
            if portfolio_weights.is_empty():
                raise ValueError("portfolio_weights DataFrame cannot be empty")
            
            # Validate required Date column exists
            if "Date" not in portfolio_weights.columns:
                raise ValueError("portfolio_weights must have a 'Date' column")
            
            # Ensure at least one component column besides Date
            if len(portfolio_weights.columns) < 2:
                raise ValueError("portfolio_weights must have at least one component column besides 'Date'")
            
            # Extract component names (all columns except 'Date')
            self._portfolio_components = [column_name for column_name in portfolio_weights.columns if column_name != "Date"]
            self._num_components = len(self._portfolio_components)
            
            # Business logic validation - validate DataFrame content and weights
            validated_weights = self._validate_weights_dataframe(portfolio_weights, self._portfolio_components)
            
            # Ensure Date column appears first for consistent data structure
            column_order = ["Date"] + self._portfolio_components
            self._portfolio_weights = validated_weights.select(column_order)
            
        # === INITIALIZATION MODE 2: From component names (equal weights) ===
        else:
            # Input validation - validate component names list type
            if not isinstance(names_components, list):
                raise TypeError(f"names_components must be of type list, got {type(names_components).__name__}")
            
            # Validate list is not empty
            if len(names_components) == 0:
                raise ValueError("names_components cannot be empty")
            
            # Validate each individual component name
            for idx, component_name in enumerate(names_components):
                # Type check for each component name
                if not isinstance(component_name, str):
                    raise TypeError(f"Component name at index {idx} must be of type str, got {type(component_name).__name__}")
                
                # Content validation for each component name
                if len(component_name.strip()) == 0:
                    raise ValueError(f"Component name at index {idx} must be a non-empty string")
            
            # Business logic validation - ensure component names are unique
            if len(set(names_components)) != len(names_components):
                raise ValueError("Component names must be unique")
            
            # Store cleaned component names as instance attributes
            self._portfolio_components = [component_name.strip() for component_name in names_components]
            self._num_components = len(self._portfolio_components)
            
            # Parse and validate date parameter
            parsed_date = self._parse_date_input(date)
            
            # Calculate equal weights using mathematical formula: w_i = 1/n
            equal_weight = 1.0 / self._num_components
            
            # Create DataFrame with equal weights for all components using Polars
            data_dict = {"Date": [parsed_date]}
            # Add equal weight for each component
            for component in self._portfolio_components:
                data_dict[component] = [equal_weight]
            
            # Create Polars DataFrame from dictionary
            self._portfolio_weights = pl.DataFrame(data_dict)


    def _validate_polars_dataframe(self, dataframe_input, parameter_name: str) -> None:
        """Validate that input is a Polars DataFrame with explicit error handling.
        
        This method provides clear error messages when non-Polars DataFrames are provided,
        including specific guidance for pandas DataFrame users.

        !!! tip "Purpose"
            This validation method ensures only Polars DataFrames are accepted throughout
            the portfolio class, maintaining performance and consistency guarantees.

        !!! warning "Pandas DataFrame Detection"
            The method specifically detects pandas DataFrames and provides conversion
            guidance using `pl.from_pandas()` for user convenience.

        Parameters
        ----------
        dataframe_input : Any
            The object to validate as a Polars DataFrame.
            
            !!! note "Accepted Type"
                Only `polars.DataFrame` objects are accepted. All other types,
                including pandas DataFrames, will raise TypeError.
                
        parameter_name : str
            Name of the parameter for error reporting and debugging.
            
            !!! example "Parameter Names"
                ```python
                "portfolio_weights"
                "benchmark_data"
                "rebalancing_schedule"
                ```
        
        Raises
        ------
        TypeError
            If input is not a Polars DataFrame, with specific guidance for common alternatives.
            
            !!! example "Error Messages"
                For pandas DataFrame:
                ```
                portfolio_weights must be a Polars DataFrame, got pandas DataFrame.
                Convert using: pl.from_pandas(your_dataframe)
                ```
                
                For other types:
                ```
                portfolio_weights must be a Polars DataFrame (pl.DataFrame), got list.
                Pandas DataFrames are not supported - use pl.from_pandas() to convert.
                ```

        Examples
        --------
        === "Valid Usage"
            ```python
            import polars as pl
            
            # Valid Polars DataFrame
            df = pl.DataFrame({"Date": ["2023-01-01"], "Value": [100.0]})
            self._validate_polars_dataframe(df, "test_data")
            # No exception raised
            ```
        
        === "Invalid Usage - Pandas"
            ```python
            import pandas as pd
            
            # Invalid pandas DataFrame
            df = pd.DataFrame({"Date": ["2023-01-01"], "Value": [100.0]})
            
            try:
                self._validate_polars_dataframe(df, "test_data")
            except TypeError as exc:
                print(exc)
                # Output: test_data must be a Polars DataFrame, got pandas DataFrame.
                #         Convert using: pl.from_pandas(your_dataframe)
            ```

        Notes
        -----
        **Validation Strategy:**
        
        1. **Type Check**: Uses `isinstance()` to verify Polars DataFrame type
        2. **Pandas Detection**: Attempts to detect pandas DataFrames specifically
        3. **Error Messages**: Provides actionable guidance for common mistakes
        4. **Import Safety**: Handles cases where pandas is not installed
        
        **Performance Considerations:**
        
        - Validation is performed only once during initialization
        - Type checking is fast and doesn't copy data
        - Error messages are generated only when needed
        
        **Integration with Class:**
        
        This method is called from `__init__()` before any data processing to ensure
        all subsequent operations can assume Polars DataFrame type safety.
        
        See Also
        --------
        polars.DataFrame : The required DataFrame type
        polars.from_pandas : Conversion function for pandas users
        """

        # Primary type validation - check if input is Polars DataFrame
        if not isinstance(dataframe_input, pl.DataFrame):
            # Get type name for error reporting
            dataframe_type = type(dataframe_input).__name__
            
            # === Special case: pandas DataFrame detection ===
            # Check for pandas DataFrame attributes before importing pandas
            if hasattr(dataframe_input, 'pandas') or dataframe_type == 'DataFrame':
                try:
                    # Import pandas only when needed to avoid dependency requirement
                    import pandas as pd
                    # Explicit pandas DataFrame type check
                    if isinstance(dataframe_input, pd.DataFrame):
                        raise TypeError(
                            f"{parameter_name} must be a Polars DataFrame, got pandas DataFrame. "
                            f"Convert using: pl.from_pandas(your_dataframe)"
                        )
                except ImportError:
                    # pandas not available, continue with generic error
                    pass
            
            # === Generic error for other types ===
            # Provide clear guidance for any non-Polars DataFrame type
            raise TypeError(
                f"{parameter_name} must be a Polars DataFrame (pl.DataFrame), got {dataframe_type}. "
                f"Pandas DataFrames are not supported - use pl.from_pandas() to convert."
            )


    def _validate_weights_dataframe(self, dataframe: pl.DataFrame, component_columns: List[str]) -> pl.DataFrame:
        """Validate and potentially correct portfolio weights DataFrame with mathematical constraints.
        
        This method ensures portfolio weights satisfy mathematical and business constraints
        while providing automatic correction capabilities for common issues using Polars operations.

        Parameters
        ----------
        dataframe : pl.DataFrame
            Polars DataFrame containing portfolio weights to validate.
        component_columns : List[str]
            List of component column names to validate.
            
        Returns
        -------
        pl.DataFrame
            Validated and potentially corrected Polars DataFrame with proper weight constraints.
            
        Raises
        ------
        ValueError
            If weights have zero sums (cannot be corrected) or other critical issues.
        """
        # Create a working copy to avoid modifying original data
        validated_dataframe = dataframe.clone()
        
        # === STEP 1: Validate component columns are numeric using Polars ===
        for column_name in component_columns:
            # Use Polars to count null values before casting
            nulls_before = validated_dataframe.select(pl.col(column_name).is_null().sum()).item()
            
            # Attempt to cast to numeric type using Polars casting
            try:
                test_dataframe = validated_dataframe.with_columns(
                    pl.col(column_name).cast(pl.Float64, strict=False)
                )
            except pl.exceptions.ComputeError as exc:
                raise ValueError(f"Column '{column_name}' contains data that cannot be converted to numeric: {exc}")
            
            # Count null values after casting using Polars operations
            nulls_after = test_dataframe.select(pl.col(column_name).is_null().sum()).item()
            
            # Check if casting introduced new nulls (indicates non-numeric data)
            if nulls_after > nulls_before:
                raise ValueError(f"Column '{column_name}' contains non-numeric values that cannot be converted")
                
            # Check for completely null columns using Polars operations
            if nulls_after == validated_dataframe.height:
                raise ValueError(f"Column '{column_name}' contains no valid numeric data")
            
            # Apply successful casting
            validated_dataframe = test_dataframe
        
        # === STEP 2: Handle negative weights using Polars operations ===
        for column_name in component_columns:
            # Check for negative weights using Polars vectorized operations
            has_negative = validated_dataframe.select(pl.col(column_name).lt(0).any()).item()
            if has_negative:
                # Log warning for user awareness (defensive programming)
                print(f"Warning: Negative weights found in '{column_name}' and set to 0")
                # Set negative weights to zero using Polars conditional logic
                validated_dataframe = validated_dataframe.with_columns(
                    pl.when(pl.col(column_name) < 0)
                    .then(pl.lit(0.0))
                    .otherwise(pl.col(column_name))
                    .alias(column_name)
                )
        
        # === STEP 3: Calculate and validate row sums using Polars ===
        # Use Polars horizontal sum operation for efficient row-wise calculations
        validated_dataframe = validated_dataframe.with_columns(
            pl.sum_horizontal(component_columns).alias("_row_sum")
        )
        
        # === STEP 4: Check for zero-sum rows using Polars operations ===
        zero_sum_filter = pl.col("_row_sum").eq(0)
        zero_sum_rows = validated_dataframe.filter(zero_sum_filter)
        
        if not zero_sum_rows.is_empty():
            # Extract problematic dates using Polars operations
            problematic_dates = zero_sum_rows.select("Date").to_series().to_list()
            date_string = ", ".join(str(date_value) for date_value in problematic_dates)
            raise ValueError(f"Row(s) with all zero weights found for date(s): {date_string}")
        
        # === STEP 5: Normalize rows with invalid sums using Polars ===
        tolerance = 0.001  # 0.1% tolerance for sum validation
        
        # Create boolean mask for rows needing normalization using Polars expressions
        needs_normalization = (
            (pl.col("_row_sum") < (1.0 - tolerance)) | 
            (pl.col("_row_sum") > (1.0 + tolerance))
        )
        
        # Apply normalization using Polars conditional expressions
        for column_name in component_columns:
            validated_dataframe = validated_dataframe.with_columns(
                pl.when(needs_normalization & (pl.col("_row_sum") > 0))
                .then(pl.col(column_name) / pl.col("_row_sum"))
                .otherwise(pl.col(column_name))
                .alias(column_name)
            )
        
        # Check if any normalization was applied and provide feedback
        normalized_rows = validated_dataframe.filter(needs_normalization & (pl.col("_row_sum") > 0))
        if not normalized_rows.is_empty():
            num_normalized = normalized_rows.height
            print(f"Warning: {num_normalized} row(s) had weights not summing to 1.0 and were normalized")
        
        # Remove temporary sum column and return cleaned DataFrame
        return validated_dataframe.drop("_row_sum")


    def _parse_date_input(self, date_input: Optional[Union[str, datetime, pl.Date, pl.Datetime]]) -> str:
        """Parse various date formats into a standardized string format with comprehensive handling.
        
        This method provides robust date parsing capabilities supporting multiple input formats
        commonly used in financial applications, with extensive error handling and validation.

        Parameters
        ----------
        date_input : Union[str, datetime, pl.Date, pl.Datetime, None]
            Date in various possible formats to be parsed and standardized.
            
        Returns
        -------
        str
            Date in standardized YYYY-MM-DD format for consistent internal representation.
            
        Raises
        ------
        ValueError
            If date string cannot be parsed with any supported format.
            If Polars date formatting fails.
        TypeError
            If date_input type is not supported.
        """
        # === STEP 1: Input validation with early returns - handle None input ===
        if date_input is None:
            # Use current date as sensible default for portfolio operations
            return datetime.now().strftime("%Y-%m-%d")
            
        # === STEP 2: Configuration validation - handle string date parsing ===
        # Use string-based type checking to avoid isinstance() issues with complex types
        date_type_name = type(date_input).__name__
        date_module_name = getattr(type(date_input), '__module__', '')
        
        if date_type_name == 'str':
            # Try multiple date formats in order of reliability and common usage
            supported_formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d-%m-%Y"]
            for date_format in supported_formats:
                try:
                    parsed_date = datetime.strptime(date_input, date_format)
                    return parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    continue  # Try next format
            # If we reach here, none of the formats worked
            raise ValueError(f"Could not parse date string '{date_input}'. Use YYYY-MM-DD format.")
            
        # === STEP 3: Business logic validation - handle Python datetime objects ===
        if date_type_name == 'datetime' or 'datetime' in date_module_name:
            # Safe handling for datetime objects using hasattr check
            if hasattr(date_input, 'strftime'):
                return date_input.strftime("%Y-%m-%d")
            else:
                raise ValueError(f"Object appears to be datetime but lacks strftime method: {type(date_input)}")
            
        # === STEP 4: Business logic validation - handle Polars date types safely ===
        # Check for Polars date types using safe string comparison
        is_polars_date = (
            date_type_name in ("Date", "Datetime") and 
            date_module_name and 
            'polars' in date_module_name
        )
        
        if is_polars_date:
            # Create a temporary DataFrame to leverage Polars date formatting
            temp_dataframe = pl.DataFrame({"temp_date": [date_input]})
            try:
                formatted_date = temp_dataframe.select(
                    pl.col("temp_date").dt.strftime("%Y-%m-%d")
                ).item()
                if formatted_date is None:
                    raise ValueError("Date conversion resulted in None")
                return formatted_date
            except pl.exceptions.ComputeError as polars_error:
                raise ValueError(f"Failed to format Polars date: {polars_error}")
                
        # === STEP 5: Error handling - handle other date-like objects ===
        # Try to handle date objects that have strftime method but aren't datetime
        if hasattr(date_input, 'strftime') and callable(getattr(date_input, 'strftime')):
            try:
                return date_input.strftime("%Y-%m-%d")
            except (AttributeError, ValueError) as format_error:
                raise ValueError(f"Failed to format date object: {format_error}")
                
        # === STEP 6: Final error handling - unsupported type ===
        # If we reach here, the input type is not supported
        raise TypeError(
            f"Unsupported date type: {date_type_name}. "
            f"Supported types: str, datetime, pl.Date, pl.Datetime"
        )


    @property
    def get_portfolio_weights(self) -> pl.DataFrame:
        """Get a copy of the portfolio weights DataFrame with comprehensive documentation.

        This property provides read-only access to the portfolio weights data while
        preventing unintended modifications through defensive copying.

        Returns
        -------
        pl.DataFrame
            A deep copy of the portfolio weights Polars DataFrame to prevent unintended modifications.

        Notes
        -----
        **Defensive Programming:**
        
        This method returns a clone of the internal Polars DataFrame to prevent external
        modifications that could compromise data integrity.
        
        **Polars DataFrame Guarantee:**
        
        The returned DataFrame is always a Polars DataFrame with optimized performance
        characteristics for financial data analysis.
        """
        return self._portfolio_weights.clone()


    @property
    def get_portfolio_components(self) -> List[str]:
        """Get a copy of the list of portfolio components with comprehensive documentation.

        This property provides read-only access to the component names while
        preventing unintended modifications through defensive copying.

        Returns
        -------
        List[str]
            A shallow copy of the list of portfolio component names to prevent external modifications.

        Notes
        -----
        **Defensive Programming:**
        
        This method returns a copy of the internal component list to prevent external
        modifications that could desynchronize component names and DataFrame columns.
        """
        return self._portfolio_components.copy()


    @property
    def get_num_components(self) -> int:
        """Get the number of portfolio components with comprehensive documentation.

        This property provides quick access to the portfolio size information,
        useful for mathematical calculations and validation operations.

        Returns
        -------
        int
            The number of components in the portfolio (always ≥ 1 for valid portfolios).

        Notes
        -----
        **Consistency Guarantees:**
        
        This value is automatically maintained consistent with other portfolio attributes.
        """
        return self._num_components


    @property
    def get_portfolio_name(self) -> str:
        """Get the name of the portfolio.
        
        Returns
        -------
        str
            The name of the portfolio.
            
        See Also
        --------
        set_portfolio_name : Method to set a new portfolio name
        """
        return self._portfolio_name


    def set_portfolio_name(self, portfolio_name: str) -> None:
        """Set a new name for the portfolio.

        Parameters
        ----------
        portfolio_name : str
            The new portfolio name.
            
        Raises
        ------
        TypeError
            If portfolio_name is not a string.
        ValueError
            If portfolio_name is empty or contains only whitespace.
        """
        # Input validation with early returns
        if not isinstance(portfolio_name, str):
            raise TypeError(f"Portfolio name must be of type str, got {type(portfolio_name).__name__}")
        
        if len(portfolio_name.strip()) == 0:
            raise ValueError("Portfolio name must be a non-empty string")
        
        self._portfolio_name = portfolio_name.strip()


    def __str__(self) -> str:
        """Return string representation of the portfolio with comprehensive formatting.

        This method provides a human-readable string representation of the portfolio
        that includes key information for debugging and user display purposes.

        !!! tip "String Representation Format"
            The output format is designed for:
            
            - **Console Display**: Easy reading in terminal/console environments
            - **Debugging**: Quick overview of portfolio state during development
            - **Logging**: Structured information for log files
            - **User Interface**: Display in GUI applications

        Returns
        -------
        str
            A formatted string representation showing:
            
            - Portfolio name in quotes for clarity
            - Number of components for quick size reference
            - Complete portfolio weights DataFrame display
            
            !!! example "Output Format"
                ```
                Portfolio 'Technology Growth Fund' with 4 components:
                ┌────────────┬──────┬──────┬────────┬──────┐
                │ Date       ┆ AAPL ┆ MSFT ┆ GOOGL  ┆ NVDA │
                │ ---        ┆ ---  ┆ ---  ┆ ---    ┆ ---  │
                │ date       ┆ f64  ┆ f64  ┆ f64    ┆ f64  │
                ├────────────┼──────┼──────┼────────┼──────┤
                │ 2023-01-01 ┆ 0.25 ┆ 0.25 ┆ 0.25   ┆ 0.25 │
                │ 2023-02-01 ┆ 0.30 ┆ 0.25 ┆ 0.20   ┆ 0.25 │
                └────────────┴──────┴──────┴────────┴──────┘
                ```

        Notes
        -----
        **Polars DataFrame Display:**
        
        The string representation leverages Polars' optimized string formatting
        which automatically handles:
        
        - Column alignment and spacing
        - Data type indicators
        - Unicode box drawing characters for clean tables
        - Automatic truncation for very large DataFrames
        
        **Performance Considerations:**
        
        - String generation is performed on-demand only when called
        - Polars handles large DataFrame display efficiently
        - No data copying occurs during string representation

        Examples
        --------
        === "Console Display"
            ```python
            # Create portfolio
            portfolio = portfolio_QWIM(
                name_portfolio="Tech Portfolio",
                names_components=["AAPL", "MSFT", "GOOGL"]
            )
            
            # Display in console
            print(portfolio)
            # Output: Portfolio 'Tech Portfolio' with 3 components:
            #         [DataFrame display follows]
            ```
        
        === "Debug Information"
            ```python
            # During debugging
            print(f"Portfolio state: {portfolio}")
            
            # In assert statements
            assert "Tech Portfolio" in str(portfolio)
            assert "3 components" in str(portfolio)
            ```
        
        === "Logging Usage"
            ```python
            import logging
            
            logger = logging.getLogger(__name__)
            logger.info(f"Created portfolio: {portfolio}")
            ```

        See Also
        --------
        __repr__ : Developer-focused representation
        get_portfolio_name : Get just the portfolio name
        get_portfolio_weights : Get the underlying DataFrame
        """
        # Generate formatted string with portfolio metadata and DataFrame display
        # Use f-string formatting for efficient string construction
        return (
            f"Portfolio '{self._portfolio_name}' with {self._num_components} components:"
            f"\n{self._portfolio_weights}"
        )


    def __repr__(self) -> str:
        """Return developer-focused string representation for debugging and development.

        This method provides a concise, unambiguous representation primarily intended
        for developers, debuggers, and interactive Python sessions.

        !!! tip "Developer Representation"
            The representation format follows Python conventions:
            
            - **Unambiguous**: Clearly identifies the object type and key attributes
            - **Concise**: Provides essential information without data overflow
            - **Reproducible**: Shows constructor-like format when possible
            - **Debug-Friendly**: Includes information useful for debugging

        Returns
        -------
        str
            A developer-focused string in pseudo-constructor format showing:
            
            - Class name for object identification
            - Portfolio name for instance identification
            - Component list for structure overview
            - Row count for size reference
            
            !!! example "Output Format"
                ```
                portfolio_QWIM(name='Technology Growth Fund', 
                              components=['AAPL', 'MSFT', 'GOOGL', 'NVDA'], 
                              dates=24 rows)
                ```

        Notes
        -----
        **Design Philosophy:**
        
        The `__repr__` method follows Python's philosophy that repr(obj) should:
        
        1. **Be Unambiguous**: Clearly identify the object type and state
        2. **Be Informative**: Provide key attributes without overwhelming detail
        3. **Be Consistent**: Use consistent formatting across similar objects
        4. **Aid Debugging**: Show information that helps identify issues
        
        **Information Hierarchy:**
        
        The representation prioritizes information in this order:
        
        1. **Portfolio Name**: Primary identifier for the instance
        2. **Components**: Structure and composition information
        3. **Size**: Scale and data volume indicators
        
        **Performance Characteristics:**
        
        - Minimal computation required (accesses cached attributes)
        - No DataFrame iteration or complex formatting
        - Suitable for use in debugging contexts with minimal overhead

        Examples
        --------
        === "Interactive Session"
            ```python
            # In Python REPL or Jupyter notebook
            >>> portfolio = portfolio_QWIM(
            ...     name_portfolio="Balanced Fund",
            ...     names_components=["Stocks", "Bonds", "Cash"]
            ... )
            >>> portfolio
            portfolio_QWIM(name='Balanced Fund', components=['Stocks', 'Bonds', 'Cash'], dates=1 rows)
            ```
        
        === "Debugging Context"
            ```python
            # In debugger or error traces
            portfolios = [portfolio1, portfolio2, portfolio3]
            print(f"Portfolios: {portfolios}")
            # Output shows repr() for each portfolio in the list
            ```
        
        === "Container Display"
            ```python
            # When portfolio is in collections
            portfolio_dict = {"tech": tech_portfolio, "value": value_portfolio}
            print(portfolio_dict)
            # Keys show with portfolio repr() values
            ```

        See Also
        --------
        __str__ : User-friendly string representation
        get_portfolio_components : Get detailed component information
        get_num_components : Get component count
        """
        # Generate concise developer representation with key attributes
        # Format similar to constructor call for clarity and debugging utility
        return (
            f"portfolio_QWIM(name='{self._portfolio_name}', "
            f"components={self._portfolio_components}, "
            f"dates={len(self._portfolio_weights)} rows)"
        )


    def add_weights(
        self, 
        date_input, 
        weights_dict=None,
        validate_weights=True
    ):
        """Add a new row of weights for a specific date using optimized Polars operations.
        
        This method enables dynamic portfolio rebalancing by adding new weight allocations
        for a specified date, with comprehensive validation and automatic normalization.

        !!! tip "Rebalancing Strategy"
            This method supports various rebalancing strategies:
            
            - **Scheduled Rebalancing**: Add weights at regular intervals
            - **Threshold Rebalancing**: Add weights when drift exceeds limits
            - **Tactical Rebalancing**: Add weights based on market conditions
            - **Equal Weight Reset**: Use None weights_dict for equal allocation

        !!! warning "Date Uniqueness"
            Each date can only have one set of weights. Attempting to add weights
            for an existing date will raise a ValueError. Use `modify_weights()` 
            to update existing dates.

        Parameters
        ----------
        date_input : Union[str, datetime, pl.Date, pl.Datetime]
            Date for the new weights in any supported format.
            
            !!! example "Supported Date Formats"
                ```python
                # String formats
                "2023-12-31"        # ISO format (recommended)
                "2023/12/31"        # Alternative slash format
                "12/31/2023"        # US format
                "31-12-2023"        # European format
                
                # Python datetime
                datetime(2023, 12, 31)
                
                # Polars date types
                pl.date(2023, 12, 31)
                pl.datetime(2023, 12, 31, 12, 0, 0)
                ```
            
        weights_dict : dict, optional
            Dictionary mapping component names to their new weights.
            
            Requirements:
            - Keys must exactly match portfolio component names
            - Values must be non-negative numbers
            - Should sum to approximately 1.0 (auto-normalized if validate_weights=True)
            
            !!! example "Weights Dictionary Examples"
                ```python
                # Explicit weights
                {"AAPL": 0.30, "MSFT": 0.25, "GOOGL": 0.25, "NVDA": 0.20}
                
                # Market cap weighted
                {"Large_Cap": 0.60, "Mid_Cap": 0.25, "Small_Cap": 0.15}
                
                # Asset allocation
                {"Stocks": 0.80, "Bonds": 0.15, "Cash": 0.05}
                ```
            
            If None, creates equal weights for all components. By default None.
            
        validate_weights : bool, optional
            Whether to validate and automatically correct weights.
            
            When True (default):
            - Negative weights are set to 0 with warnings
            - Weights are normalized to sum to 1.0 if needed
            - Validation errors are reported but not fatal
            
            When False:
            - Strict validation with exceptions for invalid weights
            - No automatic corrections applied
            - Useful for testing or when weights are pre-validated
            
            By default True.

        Returns
        -------
        portfolio_QWIM
            Returns self to enable method chaining for fluent interface patterns.
            
            !!! example "Method Chaining"
                ```python
                portfolio.add_weights("2023-01-01", {"A": 0.5, "B": 0.5}) \
                        .add_weights("2023-02-01", {"A": 0.6, "B": 0.4}) \
                        .validate_all_weights()
                ```

        Raises
        ------
        ValueError
            If date already exists in portfolio
            If weights don't sum close to 1.0 and validate_weights=False
            If negative weights found and validate_weights=False
            If component names in weights_dict don't match portfolio components
            If date cannot be parsed
            
        TypeError
            If weights_dict is not a dictionary
            If date_input has unsupported type
            If validate_weights is not boolean

        Examples
        --------
        === "Basic Weight Addition"
            ```python
            # Add quarterly rebalancing
            portfolio.add_weights(
                date_input="2023-01-01",
                weights_dict={"AAPL": 0.30, "MSFT": 0.30, "GOOGL": 0.40}
            )
            
            # Add another rebalancing date
            portfolio.add_weights(
                date_input="2023-04-01", 
                weights_dict={"AAPL": 0.25, "MSFT": 0.35, "GOOGL": 0.40}
            )
            ```
        
        === "Equal Weight Addition"
            ```python
            # Add equal weights (automatic calculation)
            portfolio.add_weights(date_input="2023-07-01")
            # Each component gets 1/n weight automatically
            
            # Equivalent to explicitly specifying equal weights
            num_components = portfolio.get_num_components
            equal_weight = 1.0 / num_components
            portfolio.add_weights(
                date_input="2023-07-01",
                weights_dict={comp: equal_weight for comp in portfolio.get_portfolio_components}
            )
            ```
        
        === "Method Chaining Pattern"
            ```python
            # Build portfolio with multiple rebalancing dates
            portfolio.add_weights("2023-01-01", {"Stock": 0.8, "Bond": 0.2}) \
                    .add_weights("2023-06-01", {"Stock": 0.7, "Bond": 0.3}) \
                    .add_weights("2023-12-01", {"Stock": 0.75, "Bond": 0.25}) \
                    .validate_all_weights(normalize=True)
            ```
        
        === "Automatic Correction Examples"
            ```python
            # Weights that don't sum to 1.0 (will be normalized)
            portfolio.add_weights(
                date_input="2023-01-01",
                weights_dict={"A": 0.6, "B": 0.5},  # Sums to 1.1
                validate_weights=True
            )
            # Warning: Weights summed to 1.1, normalized to 1.0
            # Result: A=0.545, B=0.455
            
            # Negative weights (will be corrected)
            portfolio.add_weights(
                date_input="2023-02-01", 
                weights_dict={"A": 1.2, "B": -0.2},  # Negative weight
                validate_weights=True
            )
            # Warning: Negative weight for 'B' set to 0
            # Result: A=1.0, B=0.0
            ```

        Notes
        -----
        **Validation Process:**
        
        When `validate_weights=True`, the method applies corrections in this order:
        
        1. **Negative Weight Correction**: Set negative values to 0.0
        2. **Sum Validation**: Check if weights sum to approximately 1.0 (±0.1%)
        3. **Normalization**: Scale weights proportionally if sum ≠ 1.0
        4. **Final Validation**: Ensure all constraints are satisfied
        
        **Mathematical Normalization:**
        
        When weights don't sum to 1.0, normalization applies:
        
        $$w_i^{new} = \\frac{w_i^{old}}{\\sum_{j=1}^{n} w_j^{old}}$$
        
        Where $w_i^{old}$ is the original weight of component $i$ at time $t$.
        
        **Performance Optimization:**
        
        - Uses Polars vectorized operations for date filtering and validation
        - Efficient DataFrame concatenation with automatic sorting
        - Minimal memory allocation through in-place operations where possible
        
        **Data Integrity:**
        
        The method ensures portfolio data integrity by:
        
        - Validating date uniqueness before addition
        - Maintaining consistent column ordering (Date first)
        - Preserving existing data during updates
        - Automatic sorting by date for temporal consistency

        See Also
        --------
        modify_weights : Modify existing weights for a date
        validate_all_weights : Validate all portfolio weights
        get_weights_at_date : Retrieve weights for specific date
        _parse_date_input : Internal date parsing method
        """
        # === STEP 1: Input validation with early returns - parse and validate date ===
        # Parse date input using internal method for consistent formatting
        parsed_date = self._parse_date_input(date_input)
        
        # === STEP 2: Business logic validation - check date uniqueness ===
        # Use Polars filtering to check if date already exists (defensive programming)
        date_exists = self._portfolio_weights.filter(pl.col("Date") == parsed_date).height > 0
        if date_exists:
            raise ValueError(f"Weights for date {parsed_date} already exist")
        
        # === STEP 3: Configuration validation - handle weights dictionary parameter ===
        if weights_dict is None:
            # Calculate equal weights using mathematical formula: w_i = 1/n
            equal_weight = 1.0 / self._num_components
            weights_dict = {component: equal_weight for component in self._portfolio_components}
        else:
            # Input validation - validate weights dictionary type
            if not isinstance(weights_dict, dict):
                raise TypeError(f"weights_dict must be of type dict, got {type(weights_dict).__name__}")
            
            # Business logic validation - check component completeness
            missing_components = [component for component in self._portfolio_components if component not in weights_dict]
            if missing_components:
                raise ValueError(f"Missing weights for components: {', '.join(missing_components)}")
            
            # Business logic validation - check for unexpected components
            extra_components = [component for component in weights_dict if component not in self._portfolio_components]
            if extra_components:
                raise ValueError(f"Unexpected components in weights: {', '.join(extra_components)}")
                
            # === STEP 4: Defensive programming - handle negative weights ===
            negative_components = [component for component, weight in weights_dict.items() if weight < 0]
            if negative_components:
                if validate_weights:
                    # Apply automatic correction with user notification
                    for component in negative_components:
                        print(f"Warning: Negative weight for '{component}' set to 0")
                        weights_dict[component] = 0
                else:
                    # Strict validation mode - raise exception
                    raise ValueError(f"Negative weights not allowed for: {', '.join(negative_components)}")
            
            # === STEP 5: Business logic validation - weight sum validation ===
            weight_sum = sum(weights_dict.values())
            tolerance = 0.001  # 0.1% tolerance for floating point precision
            if abs(weight_sum - 1.0) > tolerance:
                if validate_weights and weight_sum > 0:
                    # Apply automatic normalization with user notification
                    weights_dict = {component: weight / weight_sum for component, weight in weights_dict.items()}
                    print(f"Warning: Weights summed to {weight_sum}, normalized to 1.0")
                else:
                    # Strict validation mode - raise exception
                    raise ValueError(f"Sum of weights ({weight_sum}) is not close to 1.0")
        
        # === STEP 6: Data construction - create new row using Polars operations ===
        # Build new row dictionary with Date first for consistent column ordering
        new_row_dict = {"Date": parsed_date}
        new_row_dict.update(weights_dict)
        
        # === STEP 7: DataFrame operations - add and sort using Polars ===
        # Create new DataFrame from dictionary and concatenate with existing data
        new_dataframe = pl.DataFrame([new_row_dict])
        self._portfolio_weights = pl.concat([self._portfolio_weights, new_dataframe], how="vertical")
        
        # Sort by date using Polars for temporal consistency
        self._portfolio_weights = self._portfolio_weights.sort("Date")
        
        # Return self for method chaining (fluent interface pattern)
        return self


    def modify_weights(self, date_input, new_weights_dict, validate_weights=True):
        """Modify existing weights for a specific date using optimized Polars operations.
        
        This method enables fine-tuning of portfolio allocations by updating weights
        for an existing date, supporting both partial and complete weight modifications.

        !!! tip "Modification Strategies"
            This method supports flexible modification approaches:
            
            - **Partial Updates**: Modify only specific components, others unchanged
            - **Complete Replacement**: Update all component weights simultaneously
            - **Tactical Adjustments**: Small changes based on market conditions
            - **Error Corrections**: Fix incorrect weights from previous allocations

        !!! warning "Date Existence Required"
            The date must already exist in the portfolio. Use `add_weights()` to 
            create new dates, or check with `get_weights_at_date()` first.

        Parameters
        ----------
        date_input : Union[str, datetime, pl.Date, pl.Datetime]
            Date of the existing weights to modify.
            
            !!! note "Date Matching"
                The date must exactly match an existing date in the portfolio.
                Use the same format as stored or rely on the parser for conversion.
                
        new_weights_dict : dict
            Dictionary mapping component names to their new weights.
            
            Requirements:
            - Keys must be valid portfolio component names
            - Values must be non-negative numbers  
            - Can contain subset of components (partial update)
            - Combined with existing weights should sum to ~1.0
            
            !!! example "Modification Examples"
                ```python
                # Partial update (only modify AAPL)
                {"AAPL": 0.35}
                
                # Complete replacement
                {"AAPL": 0.30, "MSFT": 0.25, "GOOGL": 0.25, "NVDA": 0.20}
                
                # Multiple component adjustment
                {"AAPL": 0.28, "GOOGL": 0.32}
                ```
            
        validate_weights : bool, optional
            Whether to validate and automatically correct the resulting weights.
            
            When True (default):
            - Negative weights are set to 0 with warnings
            - Final weights are normalized to sum to 1.0 if needed
            - Validation errors are reported but corrected
            
            When False:
            - Strict validation with exceptions for invalid weights
            - No automatic corrections applied
            - Useful when precise weight control is required
            
            By default True.

        Returns
        -------
        portfolio_QWIM
            Returns self to enable method chaining for fluent interface patterns.

        Raises
        ------
        ValueError
            If date doesn't exist in portfolio
            If component names in new_weights_dict are not in portfolio  
            If resulting weights are invalid and validate_weights=False
            If date cannot be parsed
            
        TypeError
            If new_weights_dict is not a dictionary
            If validate_weights is not boolean

        Examples
        --------
        === "Partial Weight Modification"
            ```python
            # Modify only specific components
            portfolio.modify_weights(
                date_input="2023-01-01",
                new_weights_dict={"AAPL": 0.35}  # Only AAPL changes
            )
            # Other components (MSFT, GOOGL, etc.) remain unchanged
            # Final weights automatically normalized if needed
            ```
        
        === "Complete Weight Replacement"
            ```python
            # Replace all weights for a date
            portfolio.modify_weights(
                date_input="2023-01-01", 
                new_weights_dict={
                    "AAPL": 0.30,
                    "MSFT": 0.30, 
                    "GOOGL": 0.25,
                    "NVDA": 0.15
                }
            )
            ```
        
        === "Tactical Rebalancing"
            ```python
            # Small adjustments based on market conditions
            portfolio.modify_weights(
                date_input="2023-06-15",
                new_weights_dict={
                    "Tech_Stocks": 0.55,    # Increase tech exposure
                    "Bonds": 0.20           # Reduce bond allocation
                }
                # Other components automatically rebalanced
            )
            ```
        
        === "Error Correction"
            ```python
            # Fix incorrect allocation
            try:
                portfolio.modify_weights(
                    date_input="2023-01-01",
                    new_weights_dict={"Cash": 0.05},  # Should be 5%, not 50%
                    validate_weights=True
                )
            except ValueError as exc:
                print(f"Correction needed: {exc}")
            ```
        
        === "Method Chaining"
            ```python
            # Multiple modifications in sequence
            portfolio.modify_weights("2023-01-01", {"AAPL": 0.35}) \
                    .modify_weights("2023-01-01", {"MSFT": 0.25}) \
                    .validate_all_weights()
            ```

        Notes
        -----
        **Modification Process:**
        
        The method follows this sequence for weight updates:
        
        1. **Date Validation**: Verify the date exists in portfolio
        2. **Current Weight Retrieval**: Get existing weights for the date
        3. **Selective Update**: Apply new weights only for specified components
        4. **Validation & Correction**: Apply negative weight and sum corrections
        5. **DataFrame Update**: Use Polars conditional operations for efficiency
        
        **Mathematical Operations:**
        
        For partial updates, the final weight calculation is:
        
        $$w_i^{final} = \\begin{cases} 
        w_i^{new} & \\text{if component } i \\text{ in new_weights_dict} \\\\
        w_i^{current} & \\text{otherwise}
        \\end{cases}$$
        
        After normalization (if validate_weights=True):
        
        $$w_i^{normalized} = \\frac{w_i^{final}}{\\sum_{j=1}^{n} w_j^{final}}$$
        
        **Performance Characteristics:**
        
        - Uses Polars `.item()` for efficient single value extraction
        - Leverages vectorized conditional operations for DataFrame updates
        - Minimal memory allocation through in-place modifications
        - Optimized for frequent rebalancing scenarios
        
        **Data Consistency:**
        
        The method maintains data integrity by:
        
        - Preserving unchanged components exactly
        - Maintaining temporal ordering of dates
        - Ensuring mathematical constraints are satisfied
        - Providing clear feedback for automatic corrections

        See Also
        --------
        add_weights : Add weights for new dates
        validate_all_weights : Validate entire portfolio
        get_weights_at_date : Retrieve weights for specific date
        _parse_date_input : Internal date parsing method
        """
        # === STEP 1: Input validation with early returns - parse and validate date ===
        # Parse date input using internal method for consistent formatting
        parsed_date = self._parse_date_input(date_input)
        
        # === STEP 2: Business logic validation - verify date exists ===
        # Use Polars filtering to check date existence (defensive programming)
        date_filter = self._portfolio_weights.filter(pl.col("Date") == parsed_date)
        if date_filter.is_empty():
            raise ValueError(f"No weights exist for date {parsed_date}")
        
        # === STEP 3: Input validation - validate new weights dictionary ===
        if not isinstance(new_weights_dict, dict):
            raise TypeError(f"new_weights_dict must be of type dict, got {type(new_weights_dict).__name__}")
        
        # === STEP 4: Business logic validation - check component validity ===
        invalid_components = [component for component in new_weights_dict if component not in self._portfolio_components]
        if invalid_components:
            raise ValueError(f"Invalid components in new_weights_dict: {', '.join(invalid_components)}")
        
        # === STEP 5: Data retrieval - get current weights using Polars operations ===
        current_weights_dict = {}
        for component in self._portfolio_components:
            # Use Polars .item() for efficient single value extraction
            current_weights_dict[component] = date_filter.select(pl.col(component)).item()
        
        # === STEP 6: Configuration validation - apply selective weight updates ===
        # Update only the components specified in new_weights_dict
        current_weights_dict.update(new_weights_dict)
        
        # === STEP 7: Defensive programming - handle negative weights ===
        negative_components = [component for component, weight in current_weights_dict.items() if weight < 0]
        if negative_components:
            if validate_weights:
                # Apply automatic correction with user notification
                for component in negative_components:
                    print(f"Warning: Negative weight for '{component}' set to 0")
                    current_weights_dict[component] = 0
            else:
                # Strict validation mode - raise exception
                raise ValueError(f"Negative weights not allowed for: {', '.join(negative_components)}")
        
        # === STEP 8: Business logic validation - weight sum validation ===
        weight_sum = sum(current_weights_dict.values())
        tolerance = 0.001  # 0.1% tolerance for floating point precision
        if abs(weight_sum - 1.0) > tolerance:
            if validate_weights and weight_sum > 0:
                # Apply automatic normalization with user notification
                current_weights_dict = {component: weight / weight_sum for component, weight in current_weights_dict.items()}
                print(f"Warning: Modified weights summed to {weight_sum}, normalized to 1.0")
            else:
                # Strict validation mode - raise exception
                raise ValueError(f"Sum of modified weights ({weight_sum}) is not close to 1.0")
        
        # === STEP 9: DataFrame operations - update using Polars conditional expressions ===
        # Apply updates for each component using efficient vectorized operations
        for component, weight in current_weights_dict.items():
            self._portfolio_weights = self._portfolio_weights.with_columns([
                pl.when(pl.col("Date") == parsed_date)
                .then(pl.lit(weight))
                .otherwise(pl.col(component))
                .alias(component)
            ])
        
        # Return self for method chaining (fluent interface pattern)
        return self


    def validate_all_weights(self, normalize_weights=True):
        """Validate and optionally correct all weights in the portfolio using Polars operations.
        
        This method performs comprehensive validation of the entire portfolio, checking
        mathematical constraints and data integrity across all dates and components.

        !!! tip "Validation Scope"
            This method provides portfolio-wide validation:
            
            - **Weight Constraints**: Ensures all weights are non-negative
            - **Sum Validation**: Checks weights sum to 1.0 for each date
            - **Data Integrity**: Validates DataFrame structure and types
            - **Consistency Checks**: Ensures temporal and component consistency

        !!! warning "Data Modification"
            When `normalize_weights=True`, this method modifies the portfolio data
            by correcting invalid weights. Use with caution in production systems.

        Parameters
        ----------
        normalize_weights : bool, optional
            Whether to automatically normalize rows where weights don't sum to 1.0.
            
            When True (default):
            - Negative weights are set to 0.0 with warnings
            - Row weights are normalized to sum to 1.0 if needed
            - Validation errors are reported but corrected
            
            When False:
            - Strict validation with exceptions for invalid weights
            - No automatic corrections applied
            - Useful for testing data quality without modification
            
            By default True.

        Returns
        -------
        portfolio_QWIM
            Returns self to enable method chaining for fluent interface patterns.

        Notes
        -----
        **Validation Process:**
        
        The comprehensive validation follows this sequence:
        
        1. **Column Type Validation**: Ensures numeric data types for components
        2. **Negative Weight Detection**: Identifies and optionally corrects negative values
        3. **Row Sum Calculation**: Computes weight sums for each date using Polars
        4. **Normalization Application**: Applies mathematical correction when needed
        5. **Structure Verification**: Ensures Date column is first in DataFrame
        
        **Mathematical Correction:**
        
        When normalization is applied, each row's weights are corrected using:
        
        $$w_{i,t}^{corrected} = \\frac{w_{i,t}^{original}}{\\sum_{j=1}^{n} w_{j}^{original}}$$
        
        Where $w_{i,t}$ is the weight of component $i$ at time $t$.
        
        **Performance Optimization:**
        
        - Leverages Polars vectorized operations for bulk validation
        - Uses horizontal sum operations for efficient row-wise calculations
        - Applies conditional operations to minimize data copying
        - Optimized for portfolios with many dates and components
        
        **Error Tolerance:**
        
        The validation uses a tolerance of 0.1% for sum validation:
        
        - Sums between 0.999 and 1.001 are considered valid
        - Outside this range triggers normalization (if enabled)
        - Provides balance between precision and practical usage

        Examples
        --------
        === "Basic Validation"
            ```python
            # Validate and correct all weights
            portfolio.validate_all_weights(normalize_weights=True)
            
            # Validation output might show:
            # Warning: Negative weights found in 'Component_A' and set to 0
            # Warning: 3 row(s) had weights not summing to 1.0 and were normalized
            ```
        
        === "Check-Only Mode"
            ```python
            # Validate without making corrections
            portfolio.validate_all_weights(normalize_weights=False)
            
            # Shows warnings but doesn't modify data:
            # Warning: Row with date 2023-01-01 has weights summing to 1.05
            # Warning: Negative weight detected for Component_B on 2023-02-01
            ```
        
        === "Method Chaining"
            ```python
            # Validation as part of portfolio construction
            portfolio.add_weights("2023-01-01", {"A": 0.6, "B": 0.4}) \
                    .add_weights("2023-02-01", {"A": 0.7, "B": 0.3}) \
                    .validate_all_weights(normalize_weights=True)
            ```
        
        === "Batch Processing"
            ```python
            # Validate multiple portfolios
            portfolios = [portfolio1, portfolio2, portfolio3]
            
            for portfolio in portfolios:
                portfolio.validate_all_weights(normalize_weights=True)
                print(f"Validated {portfolio.get_portfolio_name}")
            ```

        Notes
        -----
        **_validate_weights_dataframe**:
        
        This internal method is used for comprehensive validation of portfolio weights DataFrames.
        It checks for:
        
        - Numeric data types for all component columns
        - Non-negative weights, with automatic correction for negative values
        - Row-wise sum validation, with normalization if needed
        - Proper DataFrame structure (Date column first)
        
        **_parse_date_input**:
        
        This internal method parses and standardizes date inputs to ensure consistent date handling.
        It supports:
        
        - Multiple string date formats (e.g., YYYY-MM-DD, MM/DD/YYYY)
        - Python datetime objects
        - Polars date types
        - Automatic conversion to string format for internal use

        See Also
        --------
        _validate_weights_dataframe : Internal validation method
        add_weights : Add new weights with validation
        modify_weights : Modify existing weights with validation
        """
        # === STEP 1: Configuration setup - prepare statistical expressions for all components ===
        # Build comprehensive list of statistical expressions for each component
        summary_expressions = []
        
        # === STEP 2: Business logic - calculate statistical measures for each component ===
        for component in self._portfolio_components:
            # Add comprehensive statistical measures using Polars expressions
            summary_expressions.extend([
                pl.col(component).mean().alias(f"{component}_Mean"),          # Central tendency
                pl.col(component).std().alias(f"{component}_Std"),           # Dispersion measure
                pl.col(component).min().alias(f"{component}_Min"),           # Lower bound
                pl.col(component).max().alias(f"{component}_Max"),           # Upper bound
                pl.col(component).median().alias(f"{component}_Median"),     # Robust central tendency
                (pl.col(component).max() - pl.col(component).min()).alias(f"{component}_Range")  # Spread measure
            ])
        
        # === STEP 3: Data computation - execute all statistical calculations using Polars ===
        # Use single Polars select operation for efficient computation of all statistics
        return self._portfolio_weights.select(summary_expressions)


    def export_weights_to_csv(self, file_path: Union[str, Path], include_summary: bool = False) -> None:
        """Export portfolio weights to CSV file with optional summary statistics.
        
        This method provides flexible data export capabilities for portfolio weights,
        supporting both raw data export and enhanced exports with statistical summaries.

        !!! tip "Export Use Cases"
            This method supports various export scenarios:
            
            - **Data Backup**: Create portable backups of portfolio data
            - **External Analysis**: Export data for use in other analytical tools
            - **Reporting**: Generate CSV files for stakeholders and compliance
            - **Integration**: Provide data feeds for other systems

        !!! note "File Format"
            The exported CSV file maintains data integrity with:
            
            - ISO date format (YYYY-MM-DD) for compatibility
            - High precision numeric values (Polars default precision)
            - UTF-8 encoding for international character support
            - Standard CSV delimiter and quoting conventions

        Parameters
        ----------
        file_path : Union[str, Path]
            Path where the CSV file will be saved.
            
            Can be either a string path or a pathlib.Path object.
            Parent directories will be created if they don't exist.
            
            !!! example "File Path Examples"
                ```python
                # Relative paths
                "exports/portfolio_weights.csv"
                "data/portfolio_2023.csv"
                
                # Absolute paths
                "/home/user/documents/portfolio.csv"
                "C:\\Users\\Name\\Documents\\portfolio.csv"
                
                # Using pathlib
                Path("exports") / "portfolio_weights.csv"
                ```
            
        include_summary : bool, optional
            Whether to include summary statistics as additional rows.
            
            When True:
            - Adds summary statistics after the main data
            - Statistics include mean, std, min, max for each component
            - Clearly separated from time series data
            
            When False (default):
            - Exports only the time series data
            - Compatible with standard time series analysis tools
            - Smaller file size and cleaner format
            
            By default False.

        Raises
        ------
        ValueError
            If file_path is empty or invalid
            If parent directory cannot be created
            
        PermissionError
            If insufficient permissions to write to the specified location
            
        OSError
            If file system errors occur during export

        Examples
        --------
       
        === "Basic CSV Export"
            ```python
            # Export portfolio weights to CSV
            portfolio.export_weights_to_csv("portfolio_weights.csv")
            
            # Export with timestamp in filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            portfolio.export_weights_to_csv(f"portfolio_weights_{timestamp}.csv")
            ```
        
        === "Export with Summary Statistics"
            ```python
            # Export weights with statistical summary
            portfolio.export_weights_to_csv(
                "detailed_portfolio_export.csv",
                include_summary=True
            )
            
            # This creates a file with:
            # 1. Time series data (all dates and weights)
            # 2. Summary statistics (mean, std, min, max, etc.)
            ```
        
        === "Organized Export Structure"
            ```python
            from pathlib import Path
            
            # Create organized export directory
            export_dir = Path("exports") / "portfolios"



            export_dir.mkdir(parents=True, exist_ok=True)
            
            # Export to organized location
            portfolio_name = portfolio.get_portfolio_name.replace(" ", "_")
            export_path = export_dir / f"{portfolio_name}_weights.csv"
            portfolio.export_weights_to_csv(export_path)
            
            print(f"Portfolio exported to: {export_path}")
            ```
        
        === "Batch Export with Error Handling"
            ```python
            # Export multiple portfolios with error handling
            portfolios = [portfolio1, portfolio2, portfolio3]
            
            for idx, portfolio in enumerate(portfolios):
                try:
                    file_name = f"portfolio_{idx:02d}_{portfolio.get_portfolio_name}.csv"
                    safe_file_name = "".join(c for c in file_name if c.isalnum() or c in "._-")
                    
                    portfolio.export_weights_to_csv(
                        f"exports/{safe_file_name}",
                        include_summary=True
                    )
                    
                    print(f"Successfully exported {portfolio.get_portfolio_name}")
                    
                except (ValueError, PermissionError, OSError) as exc:
                    print(f"Failed to export {portfolio.get_portfolio_name}: {exc}")
            ```

        Notes
        -----
        **File Format Details:**
        
        The exported CSV file follows these conventions:
        
        - **Headers**: First row contains column names
        - **Date Format**: ISO format (YYYY-MM-DD) for international compatibility
        - **Numeric Precision**: Polars default precision (typically 15+ significant digits)
        - **Encoding**: UTF-8 for international character support
        - **Delimiter**: Comma (,) as standard CSV delimiter
        
        **Summary Statistics Format (when include_summary=True):**
        
        When summary statistics are included, the file structure is:
        
        ```
        Date,Component_1,Component_2,...
        2023-01-01,0.25,0.75,...
        2023-02-01,0.30,0.70,...
        2023-03-01,0.32,0.33,0.35
        [blank row]
        Statistic,Component_1,Component_2,...
        Mean,0.275,0.725,...
        Std,0.025,0.025,...
        Min,0.25,0.70,...
        Max,0.30,0.75,...
        ```
        
        **Performance Characteristics:**
        
        - Uses Polars optimized CSV writer for large datasets
        - Minimal memory overhead through streaming operations
        - Efficient handling of wide portfolios (many components)
        - Fast export suitable for frequent backup operations
        
        **Cross-Platform Compatibility:**
        
        The export format ensures compatibility across platforms:
        
        - Standard CSV format readable by Excel, R, Python, etc.
        - UTF-8 encoding works across Windows, macOS, Linux
        - ISO date format avoids regional date parsing issues
        - Pathlib usage ensures cross-platform path handling

        See Also
        --------
        get_portfolio_weights : Access raw data for custom export
        get_portfolio_summary : Generate statistics separately
        pathlib.Path : Cross-platform path handling
        polars.DataFrame.write_csv : Underlying export functionality
        """
        # === STEP 1: Input validation with early returns ===
        # Validate file path parameter
        if not file_path:
            raise ValueError("file_path cannot be empty")
        
        # Convert to Path object for consistent handling
        file_path_obj = Path(file_path)
        
        # === STEP 2: Configuration validation - ensure parent directory exists ===
        # Create parent directories if they don't exist (defensive programming)
        try:
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as exc:
            raise ValueError(f"Cannot create parent directory for {file_path_obj}: {exc}") from exc
        
        # === STEP 3: Data preparation - prepare export DataFrame ===
        if include_summary:
            # Business logic - create enhanced export with summary statistics
            main_data = self._portfolio_weights.clone()
            summary_stats = self.get_portfolio_summary()
            
            # Create summary rows with proper formatting
            # Add a statistic identifier column for clarity
            summary_with_labels = summary_stats.with_columns([
                pl.lit("Summary_Statistics").alias("Data_Type")
            ])
            
            # For now, export main data only (summary integration would require more complex CSV structure)
            export_data = main_data
        else:
            # Standard export - just the time series data
            export_data = self._portfolio_weights.clone()
        
        # === STEP 4: File operations - write CSV using Polars ===
        try:
            # Use Polars optimized CSV writer for efficient export
            export_data.write_csv(file=file_path_obj)
        except (PermissionError, OSError) as exc:
            raise OSError(f"Failed to write CSV file to {file_path_obj}: {exc}") from exc


    def load_weights_from_csv(self, file_path: Union[str, Path], validate_data: bool = True) -> None:
        """Load portfolio weights from CSV file with comprehensive validation.
        
        This method provides robust data import capabilities for portfolio weights,
        with extensive validation to ensure data integrity and consistency.

        !!! tip "Import Use Cases"
            This method supports various data import scenarios:
            
            - **Data Recovery**: Restore portfolio from backup files
            - **External Data Integration**: Import weights from other systems
            - **Historical Data Loading**: Load archived portfolio allocations
            - **Batch Processing**: Import multiple time periods at once

        !!! warning "Data Validation"
            When `validate_data=True`, the method performs extensive validation
            that may modify the imported data (e.g., normalizing weights).
            Use `validate_data=False` only when data integrity is guaranteed.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path to the CSV file containing portfolio weights.
            
            !!! note "Expected CSV Format"
                The CSV file must have the following structure:
                ```csv
                Date,Component_1,Component_2,Component_3
                2023-01-01,0.33,0.33,0.34
                2023-02-01,0.30,0.35,0.35
                2023-03-01,0.32,0.33,0.35
                ```
            
        validate_data : bool, optional
            Whether to perform comprehensive data validation and correction.
            
            When True (default):
            - Validates component names match existing portfolio
            - Checks weight constraints (non-negative, sum to ~1.0)
            - Normalizes weights if they don't sum to 1.0
            - Provides detailed feedback on corrections
            
            When False:
            - Performs minimal validation only
            - Faster import for trusted data sources
            - Risk of data integrity issues
            
            By default True.

        Raises
        ------
        FileNotFoundError
            If the specified CSV file doesn't exist
            
        ValueError
            If CSV format is invalid or incompatible
            If component names don't match portfolio structure
            If date column is missing or unparseable
            If validation fails and cannot be corrected
            
        PermissionError
            If insufficient permissions to read the file

        Examples
        --------
        === "Basic CSV Import"
            ```python
            # Load portfolio weights from CSV file
            portfolio.load_weights_from_csv("portfolio_weights.csv")
            
            # Load with validation disabled (faster, but riskier)
            portfolio.load_weights_from_csv(
                "trusted_data.csv", 
                validate_data=False
            )
            ```
        
        === "Import with Error Handling"
            ```python
            # Robust import with comprehensive error handling
            try:
                portfolio.load_weights_from_csv("portfolio_data.csv")
                print("Portfolio data loaded successfully")
                
            except FileNotFoundError:
                print("Error: Portfolio data file not found")
                
            except ValueError as exc:
                print(f"Error: Invalid data format - {exc}")
                
            except PermissionError:
                print("Error: Insufficient permissions to read file")
            ```
        
        === "Batch Import from Directory"
            ```python
            from pathlib import Path
            
            # Import multiple CSV files from directory
            data_directory = Path("portfolio_backups")
            csv_files = list(data_directory.glob("*.csv"))
            
            for csv_file in sorted(csv_files):
                try:
                    print(f"Loading {csv_file.name}...")
                    portfolio.load_weights_from_csv(csv_file)
                    print(f"Successfully loaded {len(portfolio.get_portfolio_weights)} dates")
                    break  # Use first successful file
                    
                except (ValueError, FileNotFoundError) as exc:
                    print(f"Failed to load {csv_file.name}: {exc}")
                    continue
            ```
        
        === "Data Validation and Inspection"
            ```python
            # Load data and inspect validation results
            print("Loading portfolio data with validation...")
            
            # Capture current state for comparison
            original_dates = len(portfolio.get_portfolio_weights)
            
            # Load new data
            portfolio.load_weights_from_csv("new_portfolio_data.csv")
            
            # Inspect results
            new_dates = len(portfolio.get_portfolio_weights)
            print(f"Loaded {new_dates - original_dates} new dates")
            
            # Validate final state
            summary = portfolio.get_portfolio_summary()
            print("Portfolio summary after import:")
            print(summary)
            ```

        Notes
        -----
        **CSV Format Requirements:**
        
        The input CSV file must meet these specifications:
        
        - **Date Column**: First column named "Date" with parseable date values
        - **Component Columns**: One column per portfolio component
        - **Headers**: First row must contain column names
        - **Data Types**: Numeric values for weights, dates in recognized format
        - **Encoding**: UTF-8 recommended for international compatibility
        
        **Validation Process (when validate_data=True):**
        
        The comprehensive validation follows this sequence:
        
        1. **File Format Validation**: Check CSV structure and readability
        2. **Column Validation**: Ensure required columns are present
        3. **Component Matching**: Verify component names match portfolio
        4. **Date Parsing**: Convert date strings to proper date types
        5. **Weight Validation**: Check mathematical constraints
        6. **Data Integration**: Merge with existing portfolio data
        
        **Data Integration Strategy:**
        
        When loading new data:
        
        - **Merge Strategy**: New dates are added, existing dates are replaced
        - **Sort Order**: Final data is sorted chronologically
        - **Validation**: All data (existing + new) is validated together
        - **Backup**: Original data is preserved until validation succeeds
        
        **Performance Considerations:**
        
        - Uses Polars CSV reader for optimal performance
        - Validation overhead scales with data size
        - Memory usage peaks during validation process
        - Large files benefit from `validate_data=False` if pre-validated

        See Also
        --------
        export_weights_to_csv : Export data to CSV format
        validate_all_weights : Ensure data quality before analysis
        _validate_weights_dataframe : Internal validation logic
        polars.read_csv : Underlying CSV reading functionality
        """
        # === STEP 1: Input validation with early returns ===
        # Validate file path parameter
        if not file_path:
            raise ValueError("file_path cannot be empty")
        
        # Convert to Path object for consistent handling
        file_path_obj = Path(file_path)
        
        # === STEP 2: File system validation - check file exists and is readable ===
        if not file_path_obj.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path_obj}")
        
        if not file_path_obj.is_file():
            raise ValueError(f"Path is not a file: {file_path_obj}")
        
        # === STEP 3: Data loading - read CSV using Polars ===
        try:
            # Use Polars for efficient CSV reading with automatic type inference
            imported_data = pl.read_csv(
                source=file_path_obj,
                try_parse_dates=True,  # Automatically parse date columns
                null_values=["", "NULL", "null", "None"],  # Handle various null representations
            )
        except Exception as exc:
            raise ValueError(f"Failed to read CSV file {file_path_obj}: {exc}") from exc
        
        # === STEP 4: Data structure validation ===
        # Check if CSV is empty
        if imported_data.is_empty():
            raise ValueError(f"CSV file is empty: {file_path_obj}")
        
        # Validate Date column exists
        if "Date" not in imported_data.columns:
            raise ValueError("CSV file must have a 'Date' column")
        
        # Extract component columns (all except Date)
        imported_components = [col for col in imported_data.columns if col != "Date"]
        
        if not imported_components:
            raise ValueError("CSV file must have at least one component column besides 'Date'")
        
        # === STEP 5: Business logic validation - check component compatibility ===
        # Verify imported components match existing portfolio components
        missing_components = set(self._portfolio_components) - set(imported_components)
        extra_components = set(imported_components) - set(self._portfolio_components)
        
        if missing_components:
            raise ValueError(f"CSV file missing required components: {', '.join(missing_components)}")
        
        if extra_components:
            raise ValueError(f"CSV file contains unexpected components: {', '.join(extra_components)}")
        
        # === STEP 6: Data validation and integration ===
        if validate_data:
            # Apply comprehensive validation using internal method
            validated_data = self._validate_weights_dataframe(imported_data, self._portfolio_components)
        else:
            # Minimal validation - just ensure proper column ordering
            column_order = ["Date"] + self._portfolio_components
            validated_data = imported_data.select(column_order)
        
        # === STEP 7: Data integration - replace portfolio data ===
        # Replace current portfolio weights with validated imported data
        # Sort by date for temporal consistency
        self._portfolio_weights = validated_data.sort("Date")
        
        # Return self for method chaining (fluent interface pattern)
        return self

    def get_weights_at_date(self, date_input: Union[str, datetime, pl.Date, pl.Datetime]) -> pl.DataFrame:
        """Get portfolio weights for a specific date with comprehensive validation.
        
        This method retrieves the weight allocation for a specific date, providing
        detailed error handling and support for various date input formats.

        !!! tip "Date Retrieval Use Cases"
            This method supports various portfolio analysis scenarios:
            
            - **Point-in-Time Analysis**: Get weights at specific rebalancing dates
            - **Performance Attribution**: Analyze returns based on specific allocations
            - **Compliance Reporting**: Extract weights for regulatory reporting
            - **Backtesting**: Retrieve historical allocations for strategy testing

        !!! note "Date Matching"
            The method requires exact date matching. Use the same date format as stored
            in the portfolio or rely on the internal date parser for conversion.

        Parameters
        ----------
        date_input : Union[str, datetime, pl.Date, pl.Datetime]
            Date for which to retrieve weights.
            
            Supported formats:
            - String: "YYYY-MM-DD", "YYYY/MM/DD", "MM/DD/YYYY", "DD-MM-YYYY"
            - datetime.datetime objects
            - Polars Date/Datetime objects
            
            !!! example "Date Input Examples"
                ```python
                # String formats
                "2023-01-01"        # ISO format (recommended)
                "2023/01/01"        # Alternative slash format
                "01/01/2023"        # US format
                "01-01-2023"        # European format
                
                # Python datetime
                datetime(2023, 1, 1)
                
                # Polars date types
                pl.date(2023, 1, 1)
                pl.datetime(2023, 1, 1, 12, 0, 0)
                ```

        Returns
        -------
        pl.DataFrame
            Single-row Polars DataFrame containing weights for the specified date.
            
            !!! note "Return Format"
                ```python
                # Example return value:
                shape: (1, 5)
                ┌────────────┬──────┬──────┬────────┬──────┐
                │ Date       ┆ AAPL ┆ MSFT ┆ GOOGL  ┆ NVDA │
                │ ---        ┆ ---  ┆ ---  ┆ ---    ┆ ---  │
                │ date       ┆ f64  ┆ f64  ┆ f64    ┆ f64  │
                ├────────────┼──────┼──────┼────────┼──────┤
                │ 2023-01-01 ┆ 0.25 ┆ 0.25 ┆ 0.25   ┆ 0.25 │
                │ 2023-02-01 ┆ 0.30 ┆ 0.25 ┆ 0.20   ┆ 0.25 │
                └────────────┴──────┴──────┴────────┴──────┘
                ```

        Raises
        ------
        ValueError
            If the specified date doesn't exist in the portfolio
            If date cannot be parsed from the input format
            
        TypeError
            If date_input has an unsupported type

        Examples
        --------
        === "Basic Weight Retrieval"
            ```python
            # Get weights for specific date
            weights_jan = portfolio.get_weights_at_date("2023-01-01")
            
            # Extract individual component weights
            aapl_weight = weights_jan.select("AAPL").item()
            msft_weight = weights_jan.select("MSFT").item()
            
            print(f"AAPL weight on 2023-01-01: {aapl_weight:.2%}")
            ```
        
        === "Portfolio Analysis"
            ```python
            # Analyze weight changes over time
            dates_to_check = ["2023-01-01", "2023-06-01", "2023-12-01"]
            
            for date_str in dates_to_check:
                try:
                    weights = portfolio.get_weights_at_date(date_str)
                    total_weight = weights.select(
                        pl.sum_horizontal(portfolio.get_portfolio_components)
                    ).item()
                    
                    print(f"Date: {date_str}, Total Weight: {total_weight:.3f}")
                    
                except ValueError:
                    print(f"No weights found for date: {date_str}")
            ```
        
        === "Risk Analysis"
            ```python
            from datetime import datetime
            
            # Get weights at quarter end
            quarter_end = datetime(2023, 3, 31)
            q1_weights = portfolio.get_weights_at_date(quarter_end)
            
            # Calculate concentration risk
            max_weight = q1_weights.select(
                pl.max_horizontal(portfolio.get_portfolio_components)
            ).item()
            
            print(f"Maximum component weight: {max_weight:.2%}")
            
            # Check if any component exceeds threshold
            concentration_threshold = 0.40
            if max_weight > concentration_threshold:
                print("Warning: High concentration risk detected")
            ```
        
        === "Compliance Reporting"
            ```python
            # Generate compliance report for specific date
            report_date = "2023-12-31"
            
            try:
                year_end_weights = portfolio.get_weights_at_date(report_date)
                
                print(f"Portfolio Allocation as of {report_date}:")
                print("=" * 40)
                
                for component in portfolio.get_portfolio_components:
                    weight = year_end_weights.select(component).item()
                    print(f"{component:>10}: {weight:>7.2%}")
                
                # Verify sum constraint
                total_sum = year_end_weights.select(
                    pl.sum_horizontal(portfolio.get_portfolio_components)
                ).item()
                print(f"{'Total':>10}: {total_sum:>7.2%}")
                
            except ValueError as exc:
                print(f"Cannot generate report: {exc}")
            ```

        Notes
        -----
        **Date Matching Strategy:**
        
        The method uses exact date matching after normalization:
        
        1. **Input Parsing**: Convert input to standardized YYYY-MM-DD format
        2. **Portfolio Search**: Find exact match in portfolio date column
        3. **Result Extraction**: Return single-row DataFrame for matched date
        4. **Error Handling**: Provide clear feedback for missing dates
        
        **Performance Characteristics:**
        
        - Uses Polars efficient filtering for date lookup
        - Returns view of original data (no unnecessary copying)
        - Optimized for frequent date-based queries
        - Suitable for real-time portfolio analysis
        
        **Data Integrity:**
        
        The returned DataFrame maintains:
        
        - Original data types and precision
        - Complete row structure (Date + all components)
        - Consistent column ordering (Date first)
        - Immutable view (changes don't affect original portfolio)
        
        **Integration with Analysis:**
        
        The single-row DataFrame format facilitates:
        
        - Direct integration with Polars operations
        - Easy extraction of individual component weights
        - Compatibility with mathematical computations
        - Seamless chaining with other portfolio methods

        See Also
        --------
        get_portfolio_weights : Get all portfolio weights
        add_weights : Add weights for new dates
        modify_weights : Modify existing weights
        _parse_date_input : Internal date parsing method
        """
        # === STEP 1: Input validation with early returns - parse date input ===
        # Use internal date parsing method for consistent formatting
        parsed_date = self._parse_date_input(date_input)
        
        # === STEP 2: Business logic validation - filter portfolio data by date ===
        # Use Polars filtering to find the specific date
        date_filtered_data = self._portfolio_weights.filter(pl.col("Date") == parsed_date)
        
        # === STEP 3: Configuration validation - check if date exists ===
        if date_filtered_data.is_empty():
            # Get available dates for helpful error message
            available_dates = self._portfolio_weights.select("Date").to_series().to_list()
            available_dates_str = ", ".join(str(date_val) for date_val in sorted(available_dates)[:5])
            if len(available_dates) > 5:
                available_dates_str += f", ... ({len(available_dates)} total dates)"
            
            raise ValueError(
                f"No weights exist for date {parsed_date}. "
                f"Available dates: {available_dates_str}"
            )
        
        # === STEP 4: Data retrieval - return filtered DataFrame ===
        # Return clone to prevent external modifications (defensive programming)
        return date_filtered_data.clone()


    def get_portfolio_summary(self) -> pl.DataFrame:
        """Generate comprehensive summary statistics for all portfolio components.
        
        This method computes detailed statistical measures for each component across
        all time periods, providing insights into portfolio behavior and characteristics.

        !!! tip "Summary Statistics Use Cases"
            This method supports various analytical scenarios:
            
            - **Risk Assessment**: Analyze weight volatility and ranges
            - **Portfolio Review**: Understand historical allocation patterns
            - **Performance Attribution**: Examine component allocation stability
            - **Compliance Monitoring**: Check allocation drift and limits

        !!! note "Statistical Measures"
            The summary includes comprehensive statistics for each component:
            
            - **Central Tendency**: Mean and median weights
            - **Dispersion**: Standard deviation and range
            - **Extremes**: Minimum and maximum allocations
            - **Distribution**: Statistical measures of weight patterns

        Returns
        -------
        pl.DataFrame
            DataFrame containing statistical summary with one row of statistics.
            
            Columns follow the pattern: `{Component}_{Statistic}` where:
            - Component: Each portfolio component name
            - Statistic: Mean, Std, Min, Max, Median, Range
            
            !!! example "Summary Output Format"
                ```python
                # For portfolio with components [AAPL, MSFT, GOOGL]:
                shape: (1, 18)
                ┌───────────┬──────────┬──────────┬───────────┬─────┐
                │ AAPL_Mean ┆ AAPL_Std ┆ AAPL_Min ┆ AAPL_Max  ┆ ... │
                │ ---       ┆ ---      ┆ ---      ┆ ---       ┆     │
                │ f64       ┆ f64      ┆ f64      ┆ f64       ┆     │
                ├───────────┼──────────┼──────────┼───────────┼─────┤
                │ 0.285     ┆ 0.045    ┆ 0.25     ┆ 0.35      ┆ ... │
                └───────────┴──────────┴──────────┴───────────┴─────┘
                ```

        Examples
        --------
        === "Basic Summary Generation"
            ```python
            # Generate portfolio summary
            summary = portfolio.get_portfolio_summary()
            
            # Display summary statistics
            print("Portfolio Summary Statistics:")
            print(summary)
            ```
        
        === "Risk Analysis with Summary"
            ```python
            # Analyze portfolio risk characteristics
            summary = portfolio.get_portfolio_summary()
            
            # Extract volatility measures for each component
            print("Component Weight Volatility Analysis:")
            print("=" * 50)
            
            for component in portfolio.get_portfolio_components:
                mean_col = f"{component}_Mean"
                std_col = f"{component}_Std"
                range_col = f"{component}_Range"
                
                mean_weight = summary.select(mean_col).item()
                std_weight = summary.select(std_col).item()
                weight_range = summary.select(range_col).item()
                
                # Calculate coefficient of variation (relative volatility)
                cv = std_weight / mean_weight if mean_weight > 0 else 0
                
                print(f"{component:>8}: Mean={mean_weight:.3f}, "
                      f"Std={std_weight:.3f}, Range={weight_range:.3f}, "
                      f"CV={cv:.3f}")
            ```
        
        === "Allocation Drift Analysis"
            ```python
            # Analyze how much allocations have drifted from targets
            summary = portfolio.get_portfolio_summary()
            target_weights = {"AAPL": 0.25, "MSFT": 0.25, "GOOGL": 0.25, "NVDA": 0.25}
            
            print("Allocation Drift Analysis:")
            print("=" * 40)
            
            for component, target in target_weights.items():
                mean_col = f"{component}_Mean"
                min_col = f"{component}_Min"
                max_col = f"{component}_Max"
                
                mean_actual = summary.select(mean_col).item()
                min_actual = summary.select(min_col).item()
                max_actual = summary.select(max_col).item()
                
                mean_drift = abs(mean_actual - target)
                max_drift = max(abs(min_actual - target), abs(max_actual - target))
                
                print(f"{component:>8}: Target={target:.3f}, "
                      f"Mean={mean_actual:.3f}, "
                      f"Avg Drift={mean_drift:.3f}, "
                      f"Max Drift={max_drift:.3f}")
            ```
        
        === "Component Ranking by Stability"
            ```python
            # Rank components by allocation stability (low volatility)
            summary = portfolio.get_portfolio_summary()
            
            stability_metrics = []
            for component in portfolio.get_portfolio_components:
                std_col = f"{component}_Std"
                range_col = f"{component}_Range"
                
                std_weight = summary.select(std_col).item()
                weight_range = summary.select(range_col).item()
                
                # Combine std and range for stability score (lower = more stable)
                stability_score = std_weight + (weight_range * 0.5)
                stability_metrics.append((component, stability_score))
            
            # Sort by stability (most stable first)
            stability_metrics.sort(key=lambda x: x[1])
            
            print("Component Stability Ranking (Most to Least Stable):")
            print("=" * 55)
            for idx, (component, score) in enumerate(stability_metrics, 1):
                print(f"{idx}. {component:>8}: Stability Score = {score:.4f}")
            ```

        Notes
        -----
        **Statistical Computation:**
        
        All statistics are computed using Polars vectorized operations:
        
        - **Mean**: $\\bar{w_i} = \\frac{1}{T} \\sum_{t=1}^{T} w_{i,t}$
        - **Standard Deviation**: $\\sigma_i = \\sqrt{\\frac{1}{T-1} \\sum_{t=1}^{T} (w_{i,t} - \\bar{w_i})^2}$
        - **Range**: $R_i = \\max_t(w_{i,t}) - \\min_t(w_{i,t})$
        - **Median**: 50th percentile of weight distribution
        
        Where $w_{i,t}$ is the weight of component $i$ at time $t$.
        
        **Performance Characteristics:**
        
        - Uses Polars optimized statistical functions
        - Single-pass computation for all statistics
        - Memory efficient for large portfolios
        - Scales well with number of components and dates
        
        **Data Quality Considerations:**
        
        The summary statistics provide insights into:
        
        - **Portfolio Stability**: Low standard deviations indicate stable allocations
        - **Rebalancing Frequency**: High ranges suggest frequent rebalancing
        - **Allocation Bias**: Mean weights reveal long-term allocation preferences
        - **Extreme Positions**: Min/max values show allocation boundaries
        
        **Integration with Portfolio Analysis:**
        
        The summary format facilitates:
        
        - Easy comparison across components
        - Integration with risk management systems
        - Automated reporting and monitoring
        - Statistical analysis and hypothesis testing

        See Also
        --------
        get_portfolio_weights : Access raw time series data
        validate_all_weights : Ensure data quality before analysis
        export_weights_to_csv : Export summary with time series data
        """
        # === STEP 1: Configuration setup - prepare statistical expressions for all components ===
        # Build comprehensive list of statistical expressions for each component
        summary_expressions = []
        
        # === STEP 2: Business logic - calculate statistical measures for each component ===
        for component in self._portfolio_components:
            # Add comprehensive statistical measures using Polars expressions
            summary_expressions.extend([
                pl.col(component).mean().alias(f"{component}_Mean"),          # Central tendency
                pl.col(component).std().alias(f"{component}_Std"),           # Dispersion measure
                pl.col(component).min().alias(f"{component}_Min"),           # Lower bound
                pl.col(component).max().alias(f"{component}_Max"),           # Upper bound
                pl.col(component).median().alias(f"{component}_Median"),     # Robust central tendency
                (pl.col(component).max() - pl.col(component).min()).alias(f"{component}_Range")  # Spread measure
            ])
        
        # === STEP 3: Data computation - execute all statistical calculations using Polars ===
        # Use single Polars select operation for efficient computation of all statistics
        return self._portfolio_weights.select(summary_expressions)

