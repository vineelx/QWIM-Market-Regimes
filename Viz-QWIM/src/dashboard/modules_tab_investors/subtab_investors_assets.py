"""Investor Assets Subtab Module.

This module provides comprehensive asset input and management functionality for
the investors tab of the QWIM financial dashboard. It creates professional
input forms for collecting and managing financial asset information from both
primary and partner investors across different asset categories.

The module includes:
- Taxable asset input and management
- Tax-deferred asset tracking (401k, IRA, etc.)
- Tax-free asset management (Roth accounts, municipal bonds)
- Real-time calculation and validation
- Professional UI components with enhanced styling
- Responsive design for different screen sizes

Key Features:
    - Enhanced numeric input components with currency formatting
    - Real-time validation and error handling
    - Professional card-based layout design
    - Comprehensive asset categorization system
    - Multi-investor support (primary and partner)
    - Automatic total calculations and summaries
    - Integration with summary reporting systems

Dependencies:
    - shiny: Web application framework for Python reactive programming
    - typing: Type hints and annotations for enhanced code clarity
    - utils_enhanced_ui_components: Custom UI components with professional styling
    - utils_enhanced_formatting: Financial formatting and display utilities

Architecture:
    The module implements a clean separation of concerns with dedicated functions
    for UI generation and server-side logic. All components follow enhanced UI
    patterns with consistent styling and comprehensive validation.

Example:
    Basic usage in the investors tab:
    
    ```python
    from subtab_investors_assets import (
        subtab_investors_assets_ui,
        subtab_investors_assets_server
    )
    
    # Create the assets subtab UI component
    assets_ui = subtab_investors_assets_ui(data_utils, data_inputs)
    
    # Initialize the assets subtab server logic
    def investors_server(input, output, session):
        subtab_investors_assets_server(input, output, session, data_utils, data_inputs, reactives_shiny)
    ```

Note:
    This module follows the project's Shiny naming conventions and integrates
    seamlessly with the enhanced UI component system for consistent styling
    and behavior across the application.

Author:
    QWIM Development Team

Version:
    1.0.0

Last Modified:
    June 19, 2025

"""

from shiny import ui, module, render, reactive
import typing
from typing import Dict, Any, Optional, List
import polars as pl
import pandas as pd

# Import enhanced UI components following project standards
from src.dashboard.utils_dashboard.utils_enhanced_ui_components import (
    create_enhanced_numeric_input,
    create_enhanced_card_section,
    create_enhanced_summary_display,
    ComponentVariant)

from src.dashboard.utils_dashboard.reactives_shiny import (
    get_value_from_shiny_input_numeric,
    get_value_from_shiny_input_text)

from src.dashboard.utils_dashboard.utils_visuals import (
    create_enhanced_summary_table_multi_column)

from src.dashboard.utils_dashboard.utils_enhanced_formatting import (
    extract_numeric_from_currency_string,
    format_enhanced_currency_display,
    format_currency_value)

from src.dashboard.utils_dashboard.utils_visuals import (
    create_enhanced_summary_table_multi_column)

from src.dashboard.utils_dashboard.utils_enhanced_validation import (
    validate_and_constrain_numeric_value)


@module.ui
def subtab_investors_assets_ui(
    data_utils: Dict[str, Any],
    data_inputs: Dict[str, Any]
) -> ui.div:
    """Create user interface for comprehensive investor asset input and management.
    
    Generates a professional UI layout for collecting and managing financial asset
    information from both primary and partner investors. The interface includes
    enhanced input components with validation, professional styling, and real-time
    calculation capabilities across different asset categories and tax treatments.
    
    Args:
        data_utils (Dict[str, Any]): Utility functions and configuration data
            for the dashboard application functionality.
        data_inputs (Dict[str, Any]): Default input values and validation rules
            for asset input components and form initialization.
    
    Returns:
        ui.div: Complete UI layout including:
            - Primary investor asset input section
            - Partner investor asset input section  
            - Asset category breakdown forms
            - Real-time summary displays and totals
            - Professional card-based layout design
            
    UI Structure:
        ```
        Asset Management Interface
        ├── Primary Investor Assets
        │   ├── Taxable Assets Input
        │   ├── Tax Deferred Assets Input
        │   └── Tax Free Assets Input
        ├── Partner Investor Assets
        │   ├── Taxable Assets Input
        │   ├── Tax Deferred Assets Input
        │   └── Tax Free Assets Input
        └── Asset Summary Displays
            ├── Total Primary Assets
            ├── Total Partner Assets
            └── Combined Asset Total
        ```
        
    Note:
        All input components are fully editable and include comprehensive
        validation, currency formatting, and real-time updates. The interface
        adapts to different screen sizes for optimal user experience.
    """
    return ui.div(
        # Main section header
        ui.h3("Asset Information", class_="text-center mb-4"),
        
        # Primary and Partner investor sections in responsive layout
        ui.row(
            # Primary Investor Assets Section
            ui.column(
                6,
                create_enhanced_card_section(
                    title="Primary Investor Assets",
                    content=[
                        # Asset Categories
                        ui.h5("Asset Categories", class_="mb-3 text-primary"),
                        
                        # Taxable Assets Input
                        create_enhanced_numeric_input(
                            input_ID="input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable",
                            label_text="Taxable Assets",
                            min_value=0,
                            max_value=100000000,
                            step_size=1000,
                            default_value=0,
                            currency_format=True,
                            prefix_symbol="$",
                            # help_text="Total value of taxable investment accounts",
                            tooltip_text="Enter taxable asset value",
                            required_field=False,
                            disabled_state=False,
                            input_width="100%"
                        ),
                        
                        # Tax Deferred Assets Input
                        create_enhanced_numeric_input(
                            input_ID="input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred",
                            label_text="Tax Deferred Assets",
                            min_value=0,
                            max_value=100000000,
                            step_size=1000,
                            default_value=0,
                            currency_format=True,
                            prefix_symbol="$",
                            # help_text="Total value of tax-deferred accounts (401k, Traditional IRA, etc.)",
                            tooltip_text="Enter tax-deferred asset value",
                            required_field=False,
                            disabled_state=False,
                            input_width="100%"
                        ),
                        
                        # Tax Free Assets Input
                        create_enhanced_numeric_input(
                            input_ID="input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free",
                            label_text="Tax Free Assets",
                            min_value=0,
                            max_value=100000000,
                            step_size=1000,
                            default_value=0,
                            currency_format=True,
                            prefix_symbol="$",
                            # help_text="Total value of tax-free accounts (Roth IRA, Roth 401k, etc.)",
                            tooltip_text="Enter tax-free asset value",
                            required_field=False,
                            disabled_state=False,
                            input_width="100%"
                        )
                    ],
                    icon_class="fas fa-university",
                    card_class="h-100 shadow-sm border-primary"
                )
            ),
            
            # Partner Investor Assets Section
            ui.column(
                6,
                create_enhanced_card_section(
                    title="Partner Investor Assets",
                    content=[
                        # Asset Categories
                        ui.h5("Asset Categories", class_="mb-3 text-info"),
                        
                        # Taxable Assets Input
                        create_enhanced_numeric_input(
                            input_ID="input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable",
                            label_text="Taxable Assets",
                            min_value=0,
                            max_value=100000000,
                            step_size=1000,
                            default_value=0,
                            currency_format=True,
                            prefix_symbol="$",
                            # help_text="Total value of taxable investment accounts",
                            tooltip_text="Enter taxable asset value",
                            required_field=False,
                            disabled_state=False,
                            input_width="100%"
                        ),
                        
                        # Tax Deferred Assets Input
                        create_enhanced_numeric_input(
                            input_ID="input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred",
                            label_text="Tax Deferred Assets",
                            min_value=0,
                            max_value=100000000,
                            step_size=1000,
                            default_value=0,
                            currency_format=True,
                            prefix_symbol="$",
                            # help_text="Total value of tax-deferred accounts (401k, Traditional IRA, etc.)",
                            tooltip_text="Enter tax-deferred asset value",
                            required_field=False,
                            disabled_state=False,
                            input_width="100%"
                        ),
                        
                        # Tax Free Assets Input
                        create_enhanced_numeric_input(
                            input_ID="input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free",
                            label_text="Tax Free Assets",
                            min_value=0,
                            max_value=100000000,
                            step_size=1000,
                            default_value=0,
                            currency_format=True,
                            prefix_symbol="$",
                            # help_text="Total value of tax-free accounts (Roth IRA, Roth 401k, etc.)",
                            tooltip_text="Enter tax-free asset value",
                            required_field=False,
                            disabled_state=False,
                            input_width="100%"
                        )
                    ],
                    icon_class="fas fa-piggy-bank",
                    card_class="h-100 shadow-sm border-info"
                )
            )
        ),
        
        # Asset Summary Section
        ui.row(
            # Primary Investor Total Assets (leftmost)
            ui.column(
                4,
                create_enhanced_summary_display(
                    summary_id="output_ID_tab_investors_subtab_investors_assets_investor_primary_total",
                    title="Total Assets for Investor Primary",
                    icon_class="fas fa-calculator",
                    background_class="bg-light",
                    border_variant=ComponentVariant.SUCCESS
                )
            ),
            
            # Combined Assets Total (middle)
            ui.column(
                4,
                create_enhanced_summary_display(
                    summary_id="output_ID_tab_investors_subtab_investors_assets_combined_total",
                    title="Combined Total Assets",
                    icon_class="fas fa-chart-bar",
                    background_class="bg-success",
                    text_class="text-white",
                    border_variant=ComponentVariant.SUCCESS
                )
            ),
            
            # Partner Investor Total Assets (rightmost)
            ui.column(
                4,
                create_enhanced_summary_display(
                    summary_id="output_ID_tab_investors_subtab_investors_assets_investor_partner_total",
                    title="Total Assets for Investor Partner",
                    icon_class="fas fa-calculator",
                    background_class="bg-light",
                    border_variant=ComponentVariant.INFO
                )
            )
        ),

        ui.row(
            ui.column(
                12,
                ui.card(
                    ui.card_header(
                        ui.h4("Investor Assets Overview", class_="text-center")
                    ),                        
                    ui.card_body(
                        ui.div(
                            ui.output_ui("output_ID_tab_investors_subtab_investors_assets_table_main"),
                            style="min-height: 300px; border: 1px dashed #ccc; padding: 10px;"
                        ),
                        class_="text-center"
                    )
                )
            )
        ),
        
        # Add custom CSS to ensure inputs are fully interactive
        ui.tags.style("""
        /* Ensure all numeric inputs are fully editable */
        input[type="number"] {
            pointer-events: auto !important;
            user-select: text !important;
            background-color: #ffffff !important;
            opacity: 1 !important;
            cursor: text !important;
        }
        
        /* Ensure input containers are interactive */
        .form-group {
            pointer-events: auto !important;
        }
        
        /* Style focused inputs */
        input[type="number"]:focus {
            border-color: #86b7fe !important;
            box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25) !important;
            outline: 0 !important;
        }
        
        /* Ensure input labels are properly styled */
        .form-label {
            pointer-events: none;
            user-select: none;
            cursor: default;
        }
        
        /* Enhanced styling for currency inputs */
        .currency-input input[type="number"] {
            text-align: right;
            font-weight: 500;
        }
        
        /* Remove any disabled styling */
        .disabled {
            opacity: 1 !important;
        }
        
        .disabled input {
            background-color: #ffffff !important;
            cursor: text !important;
        }
        """)
    )


@module.server
def subtab_investors_assets_server(
    input: typing.Any,
    output: typing.Any,
    session: typing.Any,
    data_utils: Dict[str, Any],
    data_inputs: Dict[str, Any],
    reactives_shiny: Dict[str, Any]
) -> None:
    """Server logic for comprehensive investor asset management and calculations.
    
    Implements reactive server-side logic for processing asset inputs, performing
    real-time calculations, and generating summary displays. The server handles
    validation, formatting, and provides immediate feedback to users as they
    input asset information.
    
    Args:
        input (typing.Any): Shiny input object containing reactive values
            from all asset input UI components.
        output (typing.Any): Shiny output object for rendering reactive
            content to summary display components.
        session (typing.Any): Shiny session object for managing
            application state and user interactions.
        data_utils (Dict[str, Any]): Utility functions and helper methods
            for calculations and data processing.
        data_inputs (Dict[str, Any]): Default values and validation rules
            for input processing and validation.
        reactives_shiny (Dict[str, Any]): Shared reactive values and state
            management objects for cross-component communication.
            
    Server Functions:
        - Real-time asset total calculations
        - Input validation and error handling
        - Summary display generation and formatting
        - Cross-component reactive updates
        
    Reactive Behavior:
        All summary outputs automatically update when any asset input value
        changes, providing immediate feedback and real-time calculations
        for enhanced user experience.
        
    Error Handling:
        Comprehensive error handling ensures graceful management of invalid
        inputs, calculation errors, and provides appropriate user feedback
        when issues occur during processing.
        
    Note:
        This function follows the project's Shiny naming conventions and
        implements proper input validation with early returns and defensive
        programming practices for robust operation.
    """
    

    # Reactive observers for currency formatting with proper input/display separation
    @reactive.effect
    @reactive.event(input.input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable, ignore_none=True)
    def observer_update_primary_taxable_assets_formatting():
        """Update currency formatting for primary taxable assets input."""
        try:
            # Get current raw value directly from input
            current_value = input.input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable()
            
            if current_value is None:
                return
            
            # Convert to string for processing
            current_str = str(current_value).strip()
            
            # Skip if empty
            if not current_str:
                return
            
            # Extract numeric value (this is the actual input value we want to preserve)
            numeric_value = extract_numeric_from_currency_string(current_str)
            
            # Validate and constrain
            constrained_value = validate_and_constrain_numeric_value(numeric_value, 0, 100000000)
            
            # Format for display (this is what the user sees)
            formatted_value = format_currency_value(constrained_value)
            
            # Only update display if different from current display
            if current_str != formatted_value:
                ui.update_text("input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable", value=formatted_value)
                
        except Exception:
            # Silently handle errors to prevent disruption
            pass


    @reactive.effect
    @reactive.event(input.input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred, ignore_none=True)
    def observer_update_primary_tax_deferred_assets_formatting():
        """Update currency formatting for primary tax deferred assets input."""
        try:
            # Get current raw value directly from input
            current_value = input.input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred()
            
            if current_value is None:
                return
            
            # Convert to string for processing
            current_str = str(current_value).strip()
            
            # Skip if empty
            if not current_str:
                return
            
            # Extract numeric value (this is the actual input value we want to preserve)
            numeric_value = extract_numeric_from_currency_string(current_str)
            
            # Validate and constrain
            constrained_value = validate_and_constrain_numeric_value(numeric_value, 0, 100000000)
            
            # Format for display (this is what the user sees)
            formatted_value = format_currency_value(constrained_value)
            
            # Only update display if different from current display
            if current_str != formatted_value:
                ui.update_text("input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred", value=formatted_value)
                
        except Exception:
            # Silently handle errors to prevent disruption
            pass


    @reactive.effect
    @reactive.event(input.input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free, ignore_none=True)
    def observer_update_primary_tax_free_assets_formatting():
        """Update currency formatting for primary tax free assets input."""
        try:
            # Get current raw value directly from input
            current_value = input.input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free()
            
            if current_value is None:
                return
            
            # Convert to string for processing
            current_str = str(current_value).strip()
            
            # Skip if empty
            if not current_str:
                return
            
            # Extract numeric value (this is the actual input value we want to preserve)
            numeric_value = extract_numeric_from_currency_string(current_str)
            
            # Validate and constrain
            constrained_value = validate_and_constrain_numeric_value(numeric_value, 0, 100000000)
            
            # Format for display (this is what the user sees)
            formatted_value = format_currency_value(constrained_value)
            
            # Only update display if different from current display
            if current_str != formatted_value:
                ui.update_text("input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free", value=formatted_value)
                
        except Exception:
            # Silently handle errors to prevent disruption
            pass


    @reactive.effect
    @reactive.event(input.input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable, ignore_none=True)
    def observer_update_partner_taxable_assets_formatting():
        """Update currency formatting for partner taxable assets input."""
        try:
            # Get current raw value directly from input
            current_value = input.input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable()
            
            if current_value is None:
                return
            
            # Convert to string for processing
            current_str = str(current_value).strip()
            
            # Skip if empty
            if not current_str:
                return
            
            # Extract numeric value (this is the actual input value we want to preserve)
            numeric_value = extract_numeric_from_currency_string(current_str)
            
            # Validate and constrain
            constrained_value = validate_and_constrain_numeric_value(numeric_value, 0, 100000000)
            
            # Format for display (this is what the user sees)
            formatted_value = format_currency_value(constrained_value)
            
            # Only update display if different from current display
            if current_str != formatted_value:
                ui.update_text("input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable", value=formatted_value)
                
        except Exception:
            # Silently handle errors to prevent disruption
            pass


    @reactive.effect
    @reactive.event(input.input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred, ignore_none=True)
    def observer_update_partner_tax_deferred_assets_formatting():
        """Update currency formatting for partner tax deferred assets input."""
        try:
            # Get current raw value directly from input
            current_value = input.input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred()
            
            if current_value is None:
                return
            
            # Convert to string for processing
            current_str = str(current_value).strip()
            
            # Skip if empty
            if not current_str:
                return
            
            # Extract numeric value (this is the actual input value we want to preserve)
            numeric_value = extract_numeric_from_currency_string(current_str)
            
            # Validate and constrain
            constrained_value = validate_and_constrain_numeric_value(numeric_value, 0, 100000000)
            
            # Format for display (this is what the user sees)
            formatted_value = format_currency_value(constrained_value)
            
            # Only update display if different from current display
            if current_str != formatted_value:
                ui.update_text("input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred", value=formatted_value)
                
        except Exception:
            # Silently handle errors to prevent disruption
            pass


    @reactive.effect
    @reactive.event(input.input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free, ignore_none=True)
    def observer_update_partner_tax_free_assets_formatting():
        """Update currency formatting for partner tax free assets input."""
        try:
            # Get current raw value directly from input
            current_value = input.input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free()
            
            if current_value is None:
                return
            
            # Convert to string for processing
            current_str = str(current_value).strip()
            
            # Skip if empty
            if not current_str:
                return
            
            # Extract numeric value (this is the actual input value we want to preserve)
            numeric_value = extract_numeric_from_currency_string(current_str)
            
            # Validate and constrain
            constrained_value = validate_and_constrain_numeric_value(numeric_value, 0, 100000000)
            
            # Format for display (this is what the user sees)
            formatted_value = format_currency_value(constrained_value)
            
            # Only update display if different from current display
            if current_str != formatted_value:
                ui.update_text("input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free", value=formatted_value)
                
        except Exception:
            # Silently handle errors to prevent disruption
            pass


    @output
    @render.text
    def output_ID_tab_investors_subtab_investors_assets_investor_primary_total():
        """Calculate and display total assets for primary investor.
        
        Returns:
            str: Formatted currency string showing total primary investor assets (dollars only)
        """
        try:
            # Get all primary investor asset values (numeric values, not display strings)
            value_Primary_Taxable_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable"])

            value_Primary_Tax_Deferred_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred"])

            value_Primary_Tax_Free_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free"])

            # Calculate total (numeric calculation)
            Primary_Total = value_Primary_Taxable_Assets + value_Primary_Tax_Deferred_Assets + value_Primary_Tax_Free_Assets

            # Format for display (dollars only, no cents)
            return format_currency_value(Primary_Total)
            
        except Exception as exc_error:
            return f"Error: {str(exc_error)}"


    @output
    @render.text
    def output_ID_tab_investors_subtab_investors_assets_investor_partner_total():
        """Calculate and display total assets for partner investor.
        
        Returns:
            str: Formatted currency string showing total partner investor assets (dollars only)
        """
        try:
            # Get all partner investor asset values (numeric values, not display strings)
            value_Partner_Taxable_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable"])

            value_Partner_Tax_Deferred_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred"])

            value_Partner_Tax_Free_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free"])

            # Calculate total (numeric calculation)
            value_Partner_Total = value_Partner_Taxable_Assets + value_Partner_Tax_Deferred_Assets + value_Partner_Tax_Free_Assets

            # Format for display (dollars only, no cents)
            return format_currency_value(value_Partner_Total)

        except Exception as exc_error:
            return f"Error: {str(exc_error)}"


    @output
    @render.text
    def output_ID_tab_investors_subtab_investors_assets_combined_total():
        """Calculate and display combined total assets for both investors.
        
        Returns:
            str: Formatted currency string showing combined total assets (dollars only)
        """
        try:
            # Get all asset values (numeric values, not display strings)
            value_Primary_Taxable_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable"])

            value_Primary_Tax_Deferred_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred"])

            value_Primary_Tax_Free_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free"])

            value_Partner_Taxable_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable"])

            value_Partner_Tax_Deferred_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred"])

            value_Partner_Tax_Free_Assets = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free"])

            # Calculate combined total (numeric calculation)
            Combined_Total = (
                value_Primary_Taxable_Assets + value_Primary_Tax_Deferred_Assets + value_Primary_Tax_Free_Assets +
                value_Partner_Taxable_Assets + value_Partner_Tax_Deferred_Assets + value_Partner_Tax_Free_Assets)

            # Format for display (dollars only, no cents)
            return format_currency_value(Combined_Total)
            
        except Exception as exc_error:
            return f"Error: {str(exc_error)}"


    @reactive.effect
    def observer_update_shared_reactives_shiny_assets():
        """Update shared reactive values for cross-module communication."""
        
        # Get all current asset values using the safe input access pattern
        primary_taxable = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable"])
        primary_tax_deferred = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred"])
        primary_tax_free = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free"])

        partner_taxable = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable"])
        partner_tax_deferred = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred"])
        partner_tax_free = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free"])

        # Update shared reactive values if available
        if reactives_shiny and isinstance(reactives_shiny, dict):
            user_inputs_category = reactives_shiny.get("User_Inputs_Shiny")
            if user_inputs_category and isinstance(user_inputs_category, dict):
                
                # Store all asset values in the shared reactive structure
                asset_mapping = {
                    "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Primary_Assets_Taxable": primary_taxable,
                    "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Primary_Assets_Tax_Deferred": primary_tax_deferred,
                    "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Primary_Assets_Tax_Free": primary_tax_free,
                    "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Partner_Assets_Taxable": partner_taxable,
                    "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Partner_Assets_Tax_Deferred": partner_tax_deferred,
                    "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Partner_Assets_Tax_Free": partner_tax_free
                }
                
                # Update each reactive value safely
                for reactive_key, current_value in asset_mapping.items():
                    if reactive_key in user_inputs_category:
                        reactive_var = user_inputs_category[reactive_key]
                        if reactive_var is not None and hasattr(reactive_var, 'set'):
                            reactive_var.set(current_value)
                

    @reactive.calc
    def calc_table_investors_assets_main():
        """Generate financial assets summary table with proper reactive dependencies.
        
        This reactive calculation automatically updates when any of the asset inputs
        change, ensuring the summary table stays synchronized with user inputs.
        
        Returns:
            pl.DataFrame: Assets data with proper reactive dependencies
            
        Reactive Dependencies:
            - input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable
            - input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred
            - input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free
            - input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable
            - input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred
            - input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free
        """
        try:
            # Input validation with early returns and explicit reactive dependencies
            # Access reactive values using proper Shiny input access patterns
            
            # Primary investor asset information with proper reactive dependencies
            # Pass the actual reactive input object to the safe function
            value_Primary_Taxable = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_taxable"])
            value_Primary_Tax_Deferred = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_deferred"])
            value_Primary_Tax_Free = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_primary_assets_tax_free"])

            # Partner investor asset information with proper reactive dependencies
            value_Partner_Taxable = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_taxable"])
            value_Partner_Tax_Deferred = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_deferred"])
            value_Partner_Tax_Free = get_value_from_shiny_input_numeric(input["input_ID_tab_investors_subtab_investors_assets_investor_partner_assets_tax_free"])

            # Configuration validation - ensure all values are non-negative
            value_Primary_Taxable = max(0.0, value_Primary_Taxable)
            value_Primary_Tax_Deferred = max(0.0, value_Primary_Tax_Deferred)
            value_Primary_Tax_Free = max(0.0, value_Primary_Tax_Free)
            value_Partner_Taxable = max(0.0, value_Partner_Taxable)
            value_Partner_Tax_Deferred = max(0.0, value_Partner_Tax_Deferred)
            value_Partner_Tax_Free = max(0.0, value_Partner_Tax_Free)

            # Business logic validation - calculate totals
            value_Primary_Total = value_Primary_Taxable + value_Primary_Tax_Deferred + value_Primary_Tax_Free
            value_Partner_Total = value_Partner_Taxable + value_Partner_Tax_Deferred + value_Partner_Tax_Free
            
            # Calculate combined totals
            value_Combined_Taxable = value_Primary_Taxable + value_Partner_Taxable
            value_Combined_Tax_Deferred = value_Primary_Tax_Deferred + value_Partner_Tax_Deferred
            value_Combined_Tax_Free = value_Primary_Tax_Free + value_Partner_Tax_Free
            value_Combined_Total = value_Primary_Total + value_Partner_Total

            # Create polars dataframe with four columns using coding standards naming
            Assets_Data = pl.DataFrame({
                "Asset_Category": [
                    "Taxable Assets", "Tax Deferred Assets", "Tax Free Assets", "Total Assets"
                ],
                "Investor_Primary": [
                    value_Primary_Taxable, value_Primary_Tax_Deferred, value_Primary_Tax_Free, value_Primary_Total
                ],
                "Investor_Partner": [
                    value_Partner_Taxable, value_Partner_Tax_Deferred, value_Partner_Tax_Free, value_Partner_Total
                ],
                "Combined_Total": [
                    value_Combined_Taxable, value_Combined_Tax_Deferred, value_Combined_Tax_Free, value_Combined_Total
                ]
            })
            
            # Configuration validation - verify dataframe was created successfully
            if Assets_Data is None or Assets_Data.height == 0:
                raise ValueError("Failed to create Assets_Data dataframe")
            
            # Return Assets_Data with proper reactive dependencies established
            return Assets_Data
            
        except Exception as exc_error:
            # Enhanced error handling with comprehensive error information
            error_message = f"Error generating assets calculation: {type(exc_error).__name__}: {str(exc_error)}"
            
            # Return fallback empty dataframe following coding standards naming
            return pl.DataFrame({
                "Asset_Category": ["Error"],
                "Investor_Primary": [0.0],
                "Investor_Partner": [0.0], 
                "Combined_Total": [0.0]
            })


    @output
    @render.ui  
    def output_ID_tab_investors_subtab_investors_assets_table_main():
        """Generate financial assets summary table using great-tables with reactive dependencies."""
        try:
            # Input validation with early returns - get reactive data from calculation
            data_Assets_DF = calc_table_investors_assets_main()
            
            # Configuration validation - ensure dataframe exists and has data
            if data_Assets_DF is None:
                raise ValueError("data_Assets_DF is None from reactive calculation")

            if data_Assets_DF.height == 0:
                raise ValueError("data_Assets_DF is empty from reactive calculation")

            # Try to create the enhanced table
            try:
                Assets_Table = create_enhanced_summary_table_multi_column(
                    dataframe_input=data_Assets_DF,
                    table_title="Financial Assets Summary",
                    table_subtitle="Current asset values organized by tax treatment and investor",
                    currency_columns=["Investor_Primary", "Investor_Partner", "Combined_Total"],
                    table_theme="professional",
                    table_width="100%"
                )
                
                # Configuration validation - verify table was created successfully
                if Assets_Table is None:
                    raise ValueError("Failed to create Assets_Table using enhanced function")
                
                # Return the GT table as HTML
                return ui.HTML(Assets_Table.as_raw_html())
                
            except Exception as table_error:
                # Fallback to simple HTML table if enhanced table creation fails
                def format_currency_fallback(amount):
                    """Format currency for fallback table."""
                    try:
                        return f"${amount:,.0f}" if amount != 0 else "$0"
                    except (ValueError, TypeError):
                        return "$0"
                
                # Extract values safely from the dataframe
                try:
                    asset_categories = data_Assets_DF.select("Asset_Category").to_series().to_list()
                    primary_values = data_Assets_DF.select("Investor_Primary").to_series().to_list()
                    partner_values = data_Assets_DF.select("Investor_Partner").to_series().to_list()
                    combined_values = data_Assets_DF.select("Combined_Total").to_series().to_list()

                    # Generate table rows
                    table_rows = []
                    for idx in range(len(asset_categories)):
                        row_class = "table-info fw-bold" if "Total" in asset_categories[idx] else ""
                        table_rows.append(f"""
                            <tr class="{row_class}">
                                <td>{asset_categories[idx]}</td>
                                <td class="text-end">{format_currency_fallback(primary_values[idx])}</td>
                                <td class="text-end">{format_currency_fallback(partner_values[idx])}</td>
                                <td class="text-end">{format_currency_fallback(combined_values[idx])}</td>
                            </tr>
                        """)
                    
                    return ui.div(
                        ui.h5("Financial Assets Summary", class_="text-center mb-3"),
                        ui.p("Current asset values organized by tax treatment and investor", 
                             class_="text-muted text-center mb-3"),
                        ui.HTML(f"""
                        <div class="table-responsive">
                            <table class="table table-striped table-hover">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Asset Category</th>
                                        <th>Investor Primary</th>
                                        <th>Investor Partner</th>
                                        <th>Combined Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {''.join(table_rows)}
                                </tbody>
                            </table>
                        </div>
                        """),
                        class_="mt-3"
                    )
                    
                except Exception as fallback_error:
                    # Ultimate fallback if even simple table generation fails
                    return ui.div(
                        ui.div(
                            ui.h5("Assets Table - Data Processing Error", class_="text-warning"),
                            ui.p(f"Enhanced table error: {str(table_error)}", class_="text-muted small"),
                            ui.p(f"Fallback error: {str(fallback_error)}", class_="text-muted small"),
                            ui.p("Please check that asset values have been entered in the Assets tab.", class_="text-info"),
                            class_="alert alert-warning"
                        ),
                        ui.HTML("""
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Asset Category</th>
                                        <th>Investor Primary</th>
                                        <th>Investor Partner</th>
                                        <th>Combined Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr><td colspan="4" class="text-center text-muted">Unable to load assets data</td></tr>
                                </tbody>
                            </table>
                        </div>
                        """)
                    )
            
        except Exception as exc_error:
            # Enhanced error handling with comprehensive error information
            error_message = f"Error generating assets table: {type(exc_error).__name__}: {str(exc_error)}"
            return ui.div(
                ui.div(
                    ui.h5("Assets Table Generation Error", class_="text-danger"),
                    ui.p(error_message, class_="text-muted"),
                    ui.p("Please check that asset values have been entered in the Assets tab.", class_="text-info"),
                    class_="alert alert-warning"
                ),
                ui.HTML("""
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead class="table-dark">
                            <tr>
                                <th>Asset Category</th>
                                <th>Investor Primary</th>
                                <th>Investor Partner</th>
                                <th>Combined Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td colspan="4" class="text-center text-muted">Error loading assets data</td></tr>
                        </tbody>
                    </table>
                </div>
                """)
            )
