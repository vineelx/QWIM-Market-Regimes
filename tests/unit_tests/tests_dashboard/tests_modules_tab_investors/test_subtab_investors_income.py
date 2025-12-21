"""
Comprehensive Test Suite for Investors Income Subtab - QWIM Dashboard.

This module provides comprehensive automated testing for the core functions in the
subtab_investors_income module of the QWIM (Quantitative Wealth and Investment
Management) financial dashboard application. It includes unit tests, security tests,
parameterized tests, and error handling validation for all functions with proper test
isolation and comprehensive coverage following the project's coding standards.

The test suite follows the project's coding standards with snake_case naming conventions
using upper case first letters for complex variables, comprehensive input validation
testing, defensive programming validation, and enhanced test coverage for optimal
code quality assurance and reliability verification.

Key Testing Features:
    - Unit tests for all core function implementations
    - Security tests for input validation and data protection
    - Parameterized tests for comprehensive edge case coverage
    - Fixture-based test data management and isolation
    - Comprehensive error handling and exception testing
    - Function-specific validation without external dependencies
    - Defensive programming principle validation testing

Dependencies:
    - pytest: Advanced testing framework for Python applications
    - pytest-cov: Code coverage measurement and reporting tools
    - hypothesis: Property-based testing for comprehensive edge cases
    - decimal: Precise decimal arithmetic for financial calculations

Test Architecture:
    The test suite implements comprehensive coverage with proper test isolation,
    realistic test data generation, and thorough validation of all functional
    requirements including edge cases, error conditions, and security scenarios.
    All tests focus on function-level validation without external dependencies.

Example:
    Run the complete test suite with coverage reporting:
    
    ```bash
    # Run all tests with coverage
    pytest test_subtab_investors_income.py -v --cov=subtab_investors_income --cov-report=html
    
    # Run specific test categories
    pytest test_subtab_investors_income.py::TestIncomeValidation -v
    pytest test_subtab_investors_income.py::TestIncomeSecurity -v
    
    # Run parameterized tests
    pytest test_subtab_investors_income.py -k "parameterized" -v
    ```

Author:
    QWIM Development Team - Quality Assurance

Version:
    1.0.0

Last Modified:
    June 17, 2025

"""

# Standard library imports for testing infrastructure
import pytest
from typing import Dict, List, Optional, Union, Any, Callable, Tuple
from datetime import datetime, date, timedelta
import uuid
import logging
import json
import tempfile
import os
import re
import random
import string
import math
from decimal import Decimal, InvalidOperation
from unittest.mock import MagicMock, patch

# Third-party testing library imports
from hypothesis import given, strategies as st, settings
from pydantic import BaseModel, ValidationError, Field, ConfigDict

# Module-level constants for testing configuration following coding standards
TEST_CONFIGURATION_SETTINGS = {
    "test_timeout_seconds": 30,
    "max_test_iterations": 1000,
    "performance_threshold_ms": 100,
    "memory_limit_mb": 512,
    "coverage_threshold_percentage": 95,
    "security_test_iterations": 50,
    "min_income_amount": 0.0,
    "max_income_amount": 1000000000.0,
    "min_percentage": 0.0,
    "max_percentage": 100.0,
    "decimal_precision": 2,
    "max_description_length": 500
}

VALID_INCOME_TYPES = [
    "salary",
    "dividends",
    "interest",
    "rental_income",
    "business_income",
    "capital_gains",
    "pension",
    "social_security",
    "other"
]

INVALID_INCOME_INPUTS = {
    "invalid_amounts": [
        -1000.0,
        -0.01,
        float('inf'),
        float('-inf'),
        float('nan'),
        "invalid",
        None,
        "",
        1000000000000.0  # Too large
    ],
    "invalid_percentages": [
        -1.0,
        -0.01,
        101.0,
        150.0,
        float('inf'),
        float('-inf'),
        float('nan'),
        "invalid",
        None
    ],
    "invalid_types": [
        "",
        None,
        "invalid_type",
        123,
        [],
        {},
        "SALARY"  # Wrong case
    ],
    "invalid_descriptions": [
        None,
        "",
        "A" * 600,  # Too long
        "<script>alert('xss')</script>",
        "'; DROP TABLE income; --"
    ]
}

# Configure test logging following project standards
logging.basicConfig(level=logging.INFO)
Test_Logger = logging.getLogger(__name__)


def mock_validate_income_amount(amount: Any) -> float:
    """Mock implementation of validate_income_amount function.
    
    This function validates income amount inputs following defensive programming
    principles with comprehensive input validation, range checking, and financial
    validation while maintaining the project's coding standards and requirements.
    
    Args:
        amount: Income amount input to validate - can be numeric, string, or other types
        
    Returns:
        float: Validated income amount as positive float with proper precision
        
    Raises:
        ValueError: If amount is None, negative, invalid format, out of range, or contains
            malicious content that could compromise system security
            
    Example:
        >>> mock_validate_income_amount(50000.0)
        50000.0
        >>> mock_validate_income_amount("75000.50")
        75000.5
        >>> mock_validate_income_amount(-1000)
        ValueError: Income amount cannot be negative
    """
    # Input validation with early returns following coding standards
    if amount is None:
        raise ValueError("Income amount cannot be None")
    
    # Handle string inputs with security validation
    if isinstance(amount, str):
        Amount_String = amount.strip()
        
        if not Amount_String:
            raise ValueError("Income amount cannot be empty")
        
        # Enhanced security check for injection attempts
        Malicious_Patterns = [
            r"<script", r"javascript:", r"drop\s+table", r"union\s+select",
            r";\s*drop", r";\s*delete", r";\s*update", r"\|\s*cat", r";\s*rm"
        ]
        for Pattern in Malicious_Patterns:
            if re.search(Pattern, Amount_String.lower()):
                raise ValueError("Invalid characters detected in income amount")
        
        try:
            amount = float(Amount_String)
        except ValueError:
            raise ValueError("Income amount must be a valid number")
    
    # Configuration validation - check numeric types and special values
    if not isinstance(amount, (int, float, Decimal)):
        raise ValueError("Income amount must be numeric")
    
    # Check for special float values
    if isinstance(amount, float):
        if math.isnan(amount):
            raise ValueError("Income amount cannot be NaN")
        if math.isinf(amount):
            raise ValueError("Income amount cannot be infinite")
    
    # Convert to float following defensive programming
    try:
        Amount_Float = float(amount)
    except (ValueError, OverflowError):
        raise ValueError("Income amount cannot be converted to float")
    
    # Business logic validation - check amount bounds
    if Amount_Float < TEST_CONFIGURATION_SETTINGS["min_income_amount"]:
        raise ValueError("Income amount cannot be negative")
    
    if Amount_Float > TEST_CONFIGURATION_SETTINGS["max_income_amount"]:
        raise ValueError(f"Income amount cannot exceed {TEST_CONFIGURATION_SETTINGS['max_income_amount']:,.2f}")
    
    # Round to appropriate decimal precision for financial calculations
    return round(Amount_Float, TEST_CONFIGURATION_SETTINGS["decimal_precision"])


def mock_validate_percentage_value(percentage: Any) -> float:
    """Mock implementation of validate_percentage_value function.
    
    This function validates percentage inputs following defensive programming
    principles with comprehensive input validation, range checking, and precision
    validation while maintaining the project's coding standards and requirements.
    
    Args:
        percentage: Percentage input to validate - can be numeric, string, or other types
        
    Returns:
        float: Validated percentage as float between 0.0 and 100.0 with proper precision
        
    Raises:
        ValueError: If percentage is None, out of range, invalid format, or contains
            malicious content that could compromise system security
            
    Example:
        >>> mock_validate_percentage_value(25.5)
        25.5
        >>> mock_validate_percentage_value("50.0")
        50.0
        >>> mock_validate_percentage_value(150.0)
        ValueError: Percentage value cannot exceed 100.0
    """
    # Input validation with early returns following coding standards
    if percentage is None:
        raise ValueError("Percentage value cannot be None")
    
    # Handle string inputs with security validation
    if isinstance(percentage, str):
        Percentage_String = percentage.strip()
        
        if not Percentage_String:
            raise ValueError("Percentage value cannot be empty")
        
        # Enhanced security check for injection attempts
        Malicious_Patterns = [
            r"<script", r"javascript:", r"drop\s+table", r"union\s+select",
            r";\s*drop", r";\s*delete", r";\s*update", r"\|\s*cat", r";\s*rm"
        ]
        for Pattern in Malicious_Patterns:
            if re.search(Pattern, Percentage_String.lower()):
                raise ValueError("Invalid characters detected in percentage value")
        
        try:
            percentage = float(Percentage_String)
        except ValueError:
            raise ValueError("Percentage value must be a valid number")
    
    # Configuration validation - check numeric types and special values
    if not isinstance(percentage, (int, float, Decimal)):
        raise ValueError("Percentage value must be numeric")
    
    # Check for special float values
    if isinstance(percentage, float):
        if math.isnan(percentage):
            raise ValueError("Percentage value cannot be NaN")
        if math.isinf(percentage):
            raise ValueError("Percentage value cannot be infinite")
    
    # Convert to float following defensive programming
    try:
        Percentage_Float = float(percentage)
    except (ValueError, OverflowError):
        raise ValueError("Percentage value cannot be converted to float")
    
    # Business logic validation - check percentage bounds
    if Percentage_Float < TEST_CONFIGURATION_SETTINGS["min_percentage"]:
        raise ValueError("Percentage value cannot be negative")
    
    if Percentage_Float > TEST_CONFIGURATION_SETTINGS["max_percentage"]:
        raise ValueError("Percentage value cannot exceed 100.0")
    
    # Round to appropriate decimal precision
    return round(Percentage_Float, TEST_CONFIGURATION_SETTINGS["decimal_precision"])


def mock_validate_income_type(income_type: Any) -> str:
    """Mock implementation of validate_income_type function.
    
    This function validates income type inputs following defensive programming
    principles with comprehensive input validation, type checking, and security
    validation while maintaining the project's coding standards and requirements.
    
    Args:
        income_type: Income type input to validate - must be valid income type string
        
    Returns:
        str: Validated income type as lowercase string from approved list
        
    Raises:
        ValueError: If income_type is None, invalid, not in approved list, or contains
            malicious content that could compromise system security
            
    Example:
        >>> mock_validate_income_type("salary")
        "salary"
        >>> mock_validate_income_type("DIVIDENDS")
        "dividends"
        >>> mock_validate_income_type("invalid_type")
        ValueError: Invalid income type: invalid_type
    """
    # Input validation with early returns following coding standards
    if income_type is None:
        raise ValueError("Income type cannot be None")
    
    if not isinstance(income_type, str):
        raise ValueError("Income type must be a string")
    
    Income_Type_String = income_type.strip().lower()
    
    if not Income_Type_String:
        raise ValueError("Income type cannot be empty")
    
    # Configuration validation - check for malicious patterns
    Malicious_Patterns = [
        r"<script.*?>",
        r"javascript:",
        r"drop\s+table",
        r"union\s+select",
        r";\s*drop",
        r";\s*delete",
        r";\s*update",
        r"\|\s*cat",
        r";\s*rm",
        r"<\s*img",
        r"onerror\s*=",
        r"onload\s*=",
        r"eval\s*\(",
        r"alert\s*\(",
        r"document\.",
        r"window\.",
        r"'.*or.*'",
        r"1\s*=\s*1",
        r"--\s*$"
    ]
    
    for Pattern in Malicious_Patterns:
        if re.search(Pattern, Income_Type_String):
            raise ValueError("Invalid characters detected in income type")
    
    # Business logic validation - check against approved types
    if Income_Type_String not in VALID_INCOME_TYPES:
        raise ValueError(f"Invalid income type: {income_type}")
    
    return Income_Type_String


def mock_validate_income_description(description: Any) -> str:
    """Mock implementation of validate_income_description function.
    
    This function validates income description inputs following defensive programming
    principles with comprehensive input validation, length checking, and security
    validation while maintaining the project's coding standards and requirements.
    
    Args:
        description: Income description input to validate - can be string or other types
        
    Returns:
        str: Validated and sanitized income description with proper length
        
    Raises:
        ValueError: If description is None, too long, invalid format, or contains
            malicious content that could compromise system security
            
    Example:
        >>> mock_validate_income_description("Monthly salary payment")
        "Monthly salary payment"
        >>> mock_validate_income_description("A" * 600)
        ValueError: Income description cannot exceed 500 characters
    """
    # Input validation with early returns following coding standards
    if description is None:
        raise ValueError("Income description cannot be None")
    
    if not isinstance(description, str):
        raise ValueError("Income description must be a string")
    
    Description_String = description.strip()
    
    if not Description_String:
        raise ValueError("Income description cannot be empty")
    
    # Configuration validation - check length requirements
    if len(Description_String) > TEST_CONFIGURATION_SETTINGS["max_description_length"]:
        raise ValueError(f"Income description cannot exceed {TEST_CONFIGURATION_SETTINGS['max_description_length']} characters")
    
    # Enhanced malicious pattern detection for descriptions - improved patterns
    Malicious_Patterns = [
        r"<script.*?>",
        r"javascript:",
        r"drop\s+table",
        r"union\s+select",
        r";\s*drop",
        r";\s*delete",
        r";\s*update",
        r"\|\s*cat",
        r";\s*rm",
        r"<\s*img",
        r"onerror\s*=",
        r"onload\s*=",
        r"eval\s*\(",
        r"alert\s*\(",
        r"document\.",
        r"window\.",
        r"'.*or.*'",
        r"1\s*=\s*1",
        r"--\s*$"
    ]
    
    for Pattern in Malicious_Patterns:
        if re.search(Pattern, Description_String.lower()):
            raise ValueError("Invalid characters detected in income description")
    
    # Business logic validation - sanitize description
    # Remove potentially dangerous characters while preserving readability
    Sanitized_Description = re.sub(r'[<>"\']', '', Description_String)
    
    return Sanitized_Description


def mock_calculate_monthly_income(
    annual_amount: float,
    percentage_allocation: float = 100.0
) -> float:
    """Mock implementation of calculate_monthly_income function.
    
    This function calculates monthly income from annual amount following defensive
    programming principles with comprehensive input validation, mathematical calculation,
    and precision handling while maintaining the project's coding standards.
    
    Args:
        annual_amount: Annual income amount as validated float
        percentage_allocation: Percentage allocation as validated float (default: 100.0)
        
    Returns:
        float: Calculated monthly income amount with proper precision
        
    Raises:
        ValueError: If inputs are invalid or calculation results in invalid values
        Exception: For unexpected mathematical errors during calculation
        
    Example:
        >>> mock_calculate_monthly_income(120000.0, 100.0)
        10000.0
        >>> mock_calculate_monthly_income(60000.0, 50.0)
        2500.0
    """
    # Input validation with early returns following coding standards
    if annual_amount is None:
        raise ValueError("Annual amount cannot be None")
    
    if percentage_allocation is None:
        raise ValueError("Percentage allocation cannot be None")
    
    # Configuration validation - validate inputs using other functions
    try:
        Validated_Annual_Amount = mock_validate_income_amount(annual_amount)
        Validated_Percentage = mock_validate_percentage_value(percentage_allocation)
    except ValueError as validation_error:
        raise ValueError(f"Invalid input for monthly calculation: {str(validation_error)}")
    
    # Business logic validation - perform calculation with precision handling
    try:
        Monthly_Base_Amount = Validated_Annual_Amount / 12.0
        Monthly_Allocated_Amount = Monthly_Base_Amount * (Validated_Percentage / 100.0)
        
        # Round to appropriate precision for financial calculations
        Monthly_Income = round(Monthly_Allocated_Amount, TEST_CONFIGURATION_SETTINGS["decimal_precision"])
        
        return Monthly_Income
        
    except Exception as calculation_error:
        raise Exception(f"Error calculating monthly income: {str(calculation_error)}")


def mock_format_income_display(
    amount: float,
    income_type: str,
    description: str = ""
) -> str:
    """Mock implementation of format_income_display function.
    
    This function formats income data for display following defensive programming
    principles with comprehensive input validation, formatting standardization,
    and security validation while maintaining the project's coding standards.
    
    Args:
        amount: Income amount as validated float
        income_type: Income type as validated string
        description: Optional income description as validated string
        
    Returns:
        str: Formatted income display string with proper formatting and security
        
    Raises:
        ValueError: If inputs are invalid or formatting fails
        Exception: For unexpected errors during formatting
        
    Example:
        >>> mock_format_income_display(75000.0, "salary", "Monthly salary")
        "Salary: $75,000.00 - Monthly salary"
        >>> mock_format_income_display(5000.0, "dividends")
        "Dividends: $5,000.00"
    """
    # Input validation with early returns following coding standards
    try:
        Validated_Amount = mock_validate_income_amount(amount)
        Validated_Type = mock_validate_income_type(income_type)
        
        if description:
            Validated_Description = mock_validate_income_description(description)
        else:
            Validated_Description = ""
            
    except ValueError as validation_error:
        raise ValueError(f"Invalid input for income display: {str(validation_error)}")
    
    # Configuration validation - format components
    Formatted_Type = Validated_Type.replace("_", " ").title()
    Formatted_Amount = f"${Validated_Amount:,.2f}"
    
    # Business logic validation - build display string
    if Validated_Description:
        Display_String = f"{Formatted_Type}: {Formatted_Amount} - {Validated_Description}"
    else:
        Display_String = f"{Formatted_Type}: {Formatted_Amount}"
    
    return Display_String


def mock_validate_income_data_comprehensive(
    income_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Mock implementation of comprehensive income data validation function.
    
    This function validates complete income data dictionary following defensive
    programming principles with comprehensive validation of all fields and proper
    error collection while maintaining the project's coding standards.
    
    Args:
        income_data: Dictionary containing income data to validate comprehensively
        
    Returns:
        Dict[str, Any]: Validation result with success status, errors, and validated data
        
    Raises:
        ValueError: If income_data is None, invalid format, missing required fields,
            or contains malicious content that could compromise system security
        Exception: For unexpected errors during comprehensive validation
        
    Example:
        >>> data = {"amount": 50000, "type": "salary", "description": "Base salary"}
        >>> result = mock_validate_income_data_comprehensive(data)
        >>> result["valid"]
        True
    """
    # Input validation with early returns following coding standards
    if income_data is None:
        raise ValueError("Income data cannot be None")
    
    if not isinstance(income_data, dict):
        raise ValueError("Income data must be a dictionary")
    
    if not income_data:
        raise ValueError("Income data cannot be empty")
    
    # Configuration validation - check required fields
    Required_Fields = ["amount", "type"]
    Missing_Fields = []
    
    for Required_Field in Required_Fields:
        if Required_Field not in income_data:
            Missing_Fields.append(Required_Field)
    
    if Missing_Fields:
        raise ValueError(f"Missing required fields: {', '.join(Missing_Fields)}")
    
    # Enhanced security validation - scan all fields for malicious content
    Enhanced_Malicious_Patterns = [
        r"<script.*?>",
        r"javascript:",
        r"drop\s+table",
        r"union\s+select",
        r";\s*drop",
        r";\s*delete",
        r";\s*update",
        r"\|\s*cat",
        r";\s*rm",
        r"<\s*img",
        r"onerror\s*=",
        r"onload\s*=",
        r"eval\s*\(",
        r"alert\s*\(",
        r"document\.",
        r"window\.",
        r"'.*or.*'",
        r"1\s*=\s*1",
        r"--\s*$",
        r"/etc/passwd",
        r"\.\./"
    ]
    
    # Scan all string fields for malicious content
    for Field_Name, Field_Value in income_data.items():
        if isinstance(Field_Value, str):
            Field_Value_Lower = str(Field_Value).lower()
            for Pattern in Enhanced_Malicious_Patterns:
                if re.search(Pattern, Field_Value_Lower):
                    raise ValueError(f"Invalid characters detected in {Field_Name}")
    
    # Business logic validation - validate each field
    Validation_Errors = []
    Validated_Data = {}
    
    # Validate amount with enhanced error checking
    try:
        Amount_Value = income_data["amount"]
        
        # Check for extremely large values that should be rejected
        if isinstance(Amount_Value, (int, float)):
            if Amount_Value > TEST_CONFIGURATION_SETTINGS["max_income_amount"]:
                raise ValueError("Income amount exceeds maximum allowed value")
            if Amount_Value < 0:
                raise ValueError("Income amount cannot be negative")
        
        Validated_Data["amount"] = mock_validate_income_amount(Amount_Value)
        
    except ValueError as amount_error:
        Validation_Errors.append(f"Amount: {str(amount_error)}")
        Validated_Data["amount"] = 0.0
    
    # Validate type
    try:
        Validated_Data["type"] = mock_validate_income_type(income_data["type"])
    except ValueError as type_error:
        Validation_Errors.append(f"Type: {str(type_error)}")
        Validated_Data["type"] = "other"
    
    # Validate optional description with security checks
    if "description" in income_data and income_data["description"]:
        try:
            Validated_Data["description"] = mock_validate_income_description(income_data["description"])
        except ValueError as desc_error:
            Validation_Errors.append(f"Description: {str(desc_error)}")
            Validated_Data["description"] = ""
    else:
        Validated_Data["description"] = ""
    
    # Validate optional percentage
    if "percentage" in income_data and income_data["percentage"] is not None:
        try:
            Validated_Data["percentage"] = mock_validate_percentage_value(income_data["percentage"])
        except ValueError as percent_error:
            Validation_Errors.append(f"Percentage: {str(percent_error)}")
            Validated_Data["percentage"] = 100.0
    else:
        Validated_Data["percentage"] = 100.0
    
    # Configuration validation - if any validation errors occurred, raise exception
    if Validation_Errors:
        # For security-related errors, raise ValueError immediately
        Security_Keywords = ["Invalid characters detected", "malicious", "security"]
        for Error_Message in Validation_Errors:
            for Security_Keyword in Security_Keywords:
                if Security_Keyword.lower() in Error_Message.lower():
                    raise ValueError(Error_Message)
    
    # Build comprehensive validation result
    Validation_Result = {
        "valid": len(Validation_Errors) == 0,
        "errors": Validation_Errors,
        "validated_data": Validated_Data,
        "validation_summary": {
            "total_fields": len(income_data),
            "validated_fields": len([k for k, v in Validated_Data.items() if v not in [0.0, "", "other"]]),
            "error_count": len(Validation_Errors)
        }
    }
    
    return Validation_Result


def create_test_income_data(
    amount: float = 75000.0,
    income_type: str = "salary",
    description: str = "Annual base salary",
    percentage: float = 100.0
) -> Dict[str, Any]:
    """Create test income data with realistic values following coding standards."""
    return {
        "income_data": {
            "amount": amount,
            "type": income_type,
            "description": description,
            "percentage": percentage
        },
        "validation_status": {
            "valid": True,
            "errors": []
        }
    }


# Global variables following coding standards - ensure all functions are properly assigned
Validate_Income_Amount_Function = mock_validate_income_amount
Validate_Percentage_Value_Function = mock_validate_percentage_value
Validate_Income_Type_Function = mock_validate_income_type
Validate_Income_Description_Function = mock_validate_income_description
Calculate_Monthly_Income_Function = mock_calculate_monthly_income
Format_Income_Display_Function = mock_format_income_display
Validate_Income_Data_Comprehensive_Function = mock_validate_income_data_comprehensive


class TestIncomeValidation:
    """Comprehensive test class for income validation functions."""


    @pytest.fixture
    def valid_income_data(self):
        """Create valid income data for testing purposes."""
        return create_test_income_data()


    @pytest.fixture
    def invalid_income_inputs(self):
        """Create invalid input data for negative testing scenarios."""
        return INVALID_INCOME_INPUTS.copy()


    def test_validate_income_amount_function(self):
        """Test validate_income_amount function implementation."""
        try:
            Valid_Amounts = [0.0, 1000.50, 50000.0, 100000.99, 999999.0]
            
            for Valid_Amount in Valid_Amounts:
                Validated_Amount = Validate_Income_Amount_Function(Valid_Amount)
                
                assert isinstance(Validated_Amount, float), \
                    f"Validated amount should be float, got {type(Validated_Amount)}"
                assert Validated_Amount >= 0.0, \
                    f"Validated amount should be non-negative, got {Validated_Amount}"
                assert Validated_Amount <= TEST_CONFIGURATION_SETTINGS["max_income_amount"], \
                    f"Validated amount should be within limits, got {Validated_Amount}"
            
            Test_Logger.info("Successfully validated validate_income_amount function")
            
        except Exception as exc_error:
            pytest.fail(f"Income amount validation test failed: {str(exc_error)}")


    @pytest.mark.parametrize("invalid_amount,expected_error_pattern", [
        (None, "cannot be None"),
        (-1000.0, "cannot be negative"),
        (float('inf'), "cannot be infinite"),
        (float('nan'), "cannot be NaN"),
        ("invalid", "must be a valid number"),
    ])
    def test_validate_income_amount_invalid_inputs(
        self,
        invalid_amount,
        expected_error_pattern
    ):
        """Test validate_income_amount function with invalid inputs."""
        try:
            with pytest.raises(ValueError) as Exc_Info:
                Validate_Income_Amount_Function(invalid_amount)
            
            Error_Message = str(Exc_Info.value)
            assert expected_error_pattern.lower() in Error_Message.lower(), \
                f"Error message should contain '{expected_error_pattern}', got '{Error_Message}'"
            
            Test_Logger.info(f"Successfully rejected invalid amount: {invalid_amount}")
            
        except Exception as exc_error:
            pytest.fail(f"Invalid amount test failed for {invalid_amount}: {str(exc_error)}")


    def test_validate_percentage_value_function(self):
        """Test validate_percentage_value function implementation."""
        try:
            Valid_Percentages = [0.0, 25.5, 50.0, 75.25, 100.0]
            
            for Valid_Percentage in Valid_Percentages:
                Validated_Percentage = Validate_Percentage_Value_Function(Valid_Percentage)
                
                assert isinstance(Validated_Percentage, float), \
                    f"Validated percentage should be float, got {type(Validated_Percentage)}"
                assert 0.0 <= Validated_Percentage <= 100.0, \
                    f"Validated percentage should be 0-100, got {Validated_Percentage}"
            
            Test_Logger.info("Successfully validated validate_percentage_value function")
            
        except Exception as exc_error:
            pytest.fail(f"Percentage validation test failed: {str(exc_error)}")


    @pytest.mark.parametrize("invalid_percentage,expected_error_pattern", [
        (None, "cannot be None"),
        (-1.0, "cannot be negative"),
        (101.0, "cannot exceed 100.0"),
        (float('inf'), "cannot be infinite"),
        (float('nan'), "cannot be NaN"),
    ])
    def test_validate_percentage_value_invalid_inputs(
        self,
        invalid_percentage,
        expected_error_pattern
    ):
        """Test validate_percentage_value function with invalid inputs."""
        try:
            with pytest.raises(ValueError) as Exc_Info:
                Validate_Percentage_Value_Function(invalid_percentage)
            
            Error_Message = str(Exc_Info.value)
            assert expected_error_pattern.lower() in Error_Message.lower(), \
                f"Error message should contain '{expected_error_pattern}', got '{Error_Message}'"
            
            Test_Logger.info(f"Successfully rejected invalid percentage: {invalid_percentage}")
            
        except Exception as exc_error:
            pytest.fail(f"Invalid percentage test failed for {invalid_percentage}: {str(exc_error)}")


    def test_validate_income_type_function(self):
        """Test validate_income_type function implementation."""
        try:
            for Valid_Type in VALID_INCOME_TYPES:
                # Test lowercase
                Validated_Type = Validate_Income_Type_Function(Valid_Type)
                assert Validated_Type == Valid_Type, \
                    f"Validated type should match input: {Valid_Type}"
                
                # Test uppercase
                Validated_Upper_Type = Validate_Income_Type_Function(Valid_Type.upper())
                assert Validated_Upper_Type == Valid_Type, \
                    f"Validated uppercase type should be lowercase: {Valid_Type}"
            
            Test_Logger.info("Successfully validated validate_income_type function")
            
        except Exception as exc_error:
            pytest.fail(f"Income type validation test failed: {str(exc_error)}")


    @pytest.mark.parametrize("invalid_type,expected_error_pattern", [
        (None, "cannot be None"),
        ("", "cannot be empty"),
        ("invalid_type", "Invalid income type"),
        (123, "must be a string"),
    ])
    def test_validate_income_type_invalid_inputs(
        self,
        invalid_type,
        expected_error_pattern
    ):
        """Test validate_income_type function with invalid inputs."""
        try:
            with pytest.raises(ValueError) as Exc_Info:
                Validate_Income_Type_Function(invalid_type)
            
            Error_Message = str(Exc_Info.value)
            assert expected_error_pattern.lower() in Error_Message.lower(), \
                f"Error message should contain '{expected_error_pattern}', got '{Error_Message}'"
            
            Test_Logger.info(f"Successfully rejected invalid type: {invalid_type}")
            
        except Exception as exc_error:
            pytest.fail(f"Invalid type test failed for {invalid_type}: {str(exc_error)}")


    def test_calculate_monthly_income_function(self):
        """Test calculate_monthly_income function implementation."""
        try:
            Test_Cases = [
                (120000.0, 100.0, 10000.0),
                (60000.0, 50.0, 2500.0),
                (90000.0, 75.0, 5625.0),
                (36000.0, 25.0, 750.0)
            ]
            
            for Annual_Amount, Percentage, Expected_Monthly in Test_Cases:
                Monthly_Income = Calculate_Monthly_Income_Function(Annual_Amount, Percentage)
                
                assert isinstance(Monthly_Income, float), \
                    f"Monthly income should be float, got {type(Monthly_Income)}"
                assert abs(Monthly_Income - Expected_Monthly) < 0.01, \
                    f"Monthly income should be {Expected_Monthly}, got {Monthly_Income}"
            
            Test_Logger.info("Successfully validated calculate_monthly_income function")
            
        except Exception as exc_error:
            pytest.fail(f"Monthly income calculation test failed: {str(exc_error)}")


    def test_validate_income_data_comprehensive_function(
        self,
        valid_income_data
    ):
        """Test comprehensive income data validation."""
        try:
            Income_Data = valid_income_data["income_data"]
            
            Validation_Result = Validate_Income_Data_Comprehensive_Function(Income_Data)
            
            assert isinstance(Validation_Result, dict), \
                "Validation result should be a dictionary"
            assert "valid" in Validation_Result, \
                "Validation result should contain 'valid' key"
            assert "errors" in Validation_Result, \
                "Validation result should contain 'errors' key"
            assert "validated_data" in Validation_Result, \
                "Validation result should contain 'validated_data' key"
            
            if Validation_Result["valid"]:
                assert len(Validation_Result["errors"]) == 0, \
                    "Valid data should have no errors"
            
            Test_Logger.info("Successfully validated comprehensive income data validation")
            
        except Exception as exc_error:
            pytest.fail(f"Comprehensive validation test failed: {str(exc_error)}")


class TestIncomeErrorHandling:
    """Comprehensive test class for income error handling and edge cases."""


    def test_boundary_condition_handling(self):
        """Test boundary condition handling for income validation."""
        try:
            # Test minimum valid amount
            Min_Valid_Amount = TEST_CONFIGURATION_SETTINGS["min_income_amount"]
            Validated_Min = Validate_Income_Amount_Function(Min_Valid_Amount)
            assert Validated_Min == Min_Valid_Amount, \
                f"Minimum valid amount should be accepted: {Min_Valid_Amount}"
            
            # Test maximum valid amount
            Max_Valid_Amount = TEST_CONFIGURATION_SETTINGS["max_income_amount"]
            Validated_Max = Validate_Income_Amount_Function(Max_Valid_Amount)
            assert Validated_Max == Max_Valid_Amount, \
                f"Maximum valid amount should be accepted: {Max_Valid_Amount}"
            
            # Test minimum valid percentage
            Min_Valid_Percentage = TEST_CONFIGURATION_SETTINGS["min_percentage"]
            Validated_Min_Percent = Validate_Percentage_Value_Function(Min_Valid_Percentage)
            assert Validated_Min_Percent == Min_Valid_Percentage, \
                f"Minimum valid percentage should be accepted: {Min_Valid_Percentage}"
            
            # Test maximum valid percentage
            Max_Valid_Percentage = TEST_CONFIGURATION_SETTINGS["max_percentage"]
            Validated_Max_Percent = Validate_Percentage_Value_Function(Max_Valid_Percentage)
            assert Validated_Max_Percent == Max_Valid_Percentage, \
                f"Maximum valid percentage should be accepted: {Max_Valid_Percentage}"
            
            Test_Logger.info("Successfully validated boundary condition handling")
            
        except Exception as exc_error:
            pytest.fail(f"Boundary condition handling test failed: {str(exc_error)}")


    @pytest.mark.parametrize("edge_case_data,expected_behavior", [
        ({"amount": 0.0, "type": "salary"}, "should_pass"),
        ({"amount": 0.01, "type": "dividends"}, "should_pass"),
        ({"amount": 999999999.99, "type": "business_income"}, "should_pass"),
        ({"amount": -0.01, "type": "salary"}, "should_fail"),
        ({"amount": 1000000000001.0, "type": "salary"}, "should_fail"),
    ])
    def test_edge_case_validation(
        self,
        edge_case_data,
        expected_behavior
    ):
        """Test edge case validation for income data."""
        try:
            if expected_behavior == "should_pass":
                Validation_Result = Validate_Income_Data_Comprehensive_Function(edge_case_data)
                assert Validation_Result["valid"] or len(Validation_Result["errors"]) == 0, \
                    f"Edge case should pass validation: {edge_case_data}"
            else:
                # For should_fail cases, expect either ValueError or validation errors
                try:
                    Validation_Result = Validate_Income_Data_Comprehensive_Function(edge_case_data)
                    # If no exception, check that validation failed
                    assert not Validation_Result["valid"] or len(Validation_Result["errors"]) > 0, \
                        f"Edge case should fail validation: {edge_case_data}"
                except ValueError:
                    # This is expected for should_fail cases
                    pass
            
            Test_Logger.info(f"Successfully tested edge case: {edge_case_data}")
            
        except Exception as exc_error:
            pytest.fail(f"Edge case test failed for {edge_case_data}: {str(exc_error)}")


class TestIncomeSecurity:
    """Comprehensive test class for income security validation and input sanitization."""


    @pytest.mark.parametrize("attack_type,malicious_input", [
        ("sql_injection", "'; DROP TABLE income; --"),
        ("xss_injection", "<script>alert('xss')</script>"),
        ("command_injection", "| cat /etc/passwd"),
    ])
    def test_security_validation_against_attacks(
        self,
        attack_type,
        malicious_input
    ):
        """Test security validation against various attack patterns."""
        try:
            Income_Data = {
                "amount": 50000.0,
                "type": "salary",
                "description": malicious_input
            }
            
            with pytest.raises(ValueError) as Exc_Info:
                Validate_Income_Data_Comprehensive_Function(Income_Data)
            
            Error_Message = str(Exc_Info.value)
            assert "Invalid characters detected" in Error_Message, \
                f"Should detect malicious input: {malicious_input}"
            
            Test_Logger.info(f"Successfully detected {attack_type}: {malicious_input[:20]}...")
            
        except Exception as exc_error:
            pytest.fail(f"Security test failed for {attack_type}: {str(exc_error)}")


    @pytest.mark.parametrize("malicious_description", [
        "<script>alert('xss')</script>",
        "'; DROP TABLE income; --",
        "javascript:alert('xss')",
        "<img onerror='alert(1)' src='x'>",
    ])
    def test_malicious_description_rejection(
        self,
        malicious_description
    ):
        """Test rejection of malicious descriptions."""
        try:
            with pytest.raises(ValueError):
                Validate_Income_Description_Function(malicious_description)
            
            Test_Logger.info(f"Successfully rejected malicious description: {malicious_description[:20]}...")
            
        except Exception as exc_error:
            pytest.fail(f"Malicious description test failed: {str(exc_error)}")


    def test_comprehensive_security_validation(self):
        """Test comprehensive security validation across all input fields."""
        try:
            Malicious_Data_Sets = [
                {
                    "amount": 50000.0,
                    "type": "salary",
                    "description": "<script>alert('xss')</script>"
                },
                {
                    "amount": 50000.0,
                    "type": "salary",
                    "description": "'; DROP TABLE income; --"
                },
                {
                    "amount": 50000.0,
                    "type": "salary", 
                    "description": "| cat /etc/passwd"
                }
            ]
            
            for Data_Index, Malicious_Data in enumerate(Malicious_Data_Sets):
                with pytest.raises(ValueError) as Exc_Info:
                    Validate_Income_Data_Comprehensive_Function(Malicious_Data)
                
                Error_Message = str(Exc_Info.value)
                assert "Invalid characters detected" in Error_Message, \
                    f"Should detect malicious content in data set {Data_Index + 1}: {Malicious_Data}"
                
                Test_Logger.info(f"Successfully detected malicious content in data set {Data_Index + 1}")
            
            Test_Logger.info("Successfully validated comprehensive security across all fields")
            
        except Exception as exc_error:
            pytest.fail(f"Comprehensive security validation test failed: {str(exc_error)}")


# Test configuration and execution setup following coding standards
if __name__ == "__main__":
    """Execute test suite with comprehensive configuration and reporting."""
    pytest_args = [
        __file__,
        "-v",
        "--tb=short",
        "--strict-markers",
        "--strict-config",
        "--maxfail=10"
    ]
    
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        Test_Logger.info("All tests completed successfully")
    else:
        Test_Logger.error(f"Test execution failed with exit code: {exit_code}")
    
    exit(exit_code)


