import logging
import pandas as pd
import polars as pl
from shiny import reactive


def validate_data_utils_parameter(data_utils):
    """Validate data_utils parameter using defensive programming."""
    
    # Input validation with early returns
    if data_utils is None:
        return False, "data_utils parameter cannot be None"
    
    # Configuration validation
    if not isinstance(data_utils, dict):
        return False, f"data_utils must be a dictionary, got {type(data_utils).__name__}"
    
    return True, ""


def validate_reactives_shiny_structure(reactives_shiny):
    """Validate reactives_shiny dictionary structure using defensive programming."""
    
    # Input validation with early returns
    if reactives_shiny is None:
        return False, "reactives_shiny dictionary cannot be None"
    
    if not isinstance(reactives_shiny, dict):
        return False, f"reactives_shiny must be a dictionary, got {type(reactives_shiny).__name__}"
    
    # Configuration validation - check required categories
    required_categories = [
        "User_Inputs_Shiny", 
        "Inner_Variables_Shiny", 
        "Triggers_Shiny", 
        "Visual_Objects_Shiny"
    ]
    
    for category_name in required_categories:
        if category_name not in reactives_shiny:
            available_categories = list(reactives_shiny.keys())
            return False, f"Required category '{category_name}' not found. Available: {available_categories}"
        
        # Business logic validation - ensure each category is a dictionary
        if not isinstance(reactives_shiny[category_name], dict):
            return False, f"Category '{category_name}' must be a dictionary, got {type(reactives_shiny[category_name]).__name__}"
    
    return True, ""


def validate_reactive_key_access(category_dict, key_name, category_name):
    """Validate reactive key access using defensive programming."""
    
    # Input validation with early returns
    if category_dict is None:
        return False, f"Category '{category_name}' is None"
    
    if not isinstance(category_dict, dict):
        return False, f"Category '{category_name}' is not a dictionary, got {type(category_dict).__name__}"
    
    if key_name is None:
        return False, "key_name cannot be None"
    
    if not isinstance(key_name, str):
        return False, f"key_name must be string, got {type(key_name).__name__}"
    
    # Configuration validation
    if len(key_name.strip()) == 0:
        return False, "key_name cannot be empty string"
    
    # Business logic validation
    if key_name not in category_dict:
        available_keys = list(category_dict.keys())
        return False, f"Key '{key_name}' not found in category '{category_name}'. Available keys: {available_keys}"
    
    return True, ""


def validate_category_name(category_name):
    """Validate category name using defensive programming."""
    
    # Input validation with early returns
    if category_name is None:
        return False, "category_name cannot be None"
    
    if not isinstance(category_name, str):
        return False, f"category_name must be string, got {type(category_name).__name__}"
    
    # Configuration validation
    if len(category_name.strip()) == 0:
        return False, "category_name cannot be empty string"
    
    # Business logic validation
    valid_categories = [
        "User_Inputs_Shiny", 
        "Inner_Variables_Shiny", 
        "Triggers_Shiny", 
        "Visual_Objects_Shiny"
    ]
    
    if category_name not in valid_categories:
        return False, f"Invalid category '{category_name}'. Valid categories: {valid_categories}"
    
    return True, ""


def safe_get_shiny_input_value(input_events, input_identifier):
    """Safely get value from Shiny input using defensive programming."""
    
    # Input validation with early returns
    if input_events is None:
        return None
    
    if not isinstance(input_identifier, str):
        return None
    
    if len(input_identifier.strip()) == 0:
        return None
    
    # Only use try-except for Shiny input access that might fail unpredictably
    try:
        # Check if the input identifier exists as an attribute of input_events
        if hasattr(input_events, input_identifier):
            input_reactive = getattr(input_events, input_identifier)
            
            # Call the reactive function to get the current value
            if callable(input_reactive):
                return input_reactive()
            else:
                return input_reactive
        else:
            return None
            
    except (AttributeError, KeyError, TypeError):
        return None
    except Exception:
        return None


def create_reactive_value_safely(initial_value=None):
    """Create a reactive value safely using defensive programming."""
    
    # Only use try-except for reactive.Value creation that might fail unpredictably
    try:
        return reactive.Value(initial_value)
    except Exception:
        return None


def initialize_reactives_shiny(data_utils):
    """Initialize all reactive values for the Shiny dashboard using defensive programming.
    
    Args:
        data_utils: Initial data for reactive value initialization
        
    Returns:
        dict: Dictionary containing organized reactive values by category
        
    Raises:
        ValueError: If data_utils is invalid
    """
    
    # Input validation with early returns
    validation_result, validation_message = validate_data_utils_parameter(data_utils)
    if not validation_result:
        raise ValueError(f"Data utils validation failed: {validation_message}")
    
    # Initialize each category using helper functions
    reactive_user_inputs = initialize_reactive_user_inputs(data_utils)
    reactive_inner_variables = initialize_reactive_inner_variables(data_utils)
    reactive_triggers = initialize_reactive_triggers(data_utils)
    reactive_visual_objects = initialize_reactive_visual_objects(data_utils)
    
    # Business logic validation - create organized structure
    dict_reactives_shiny = {
        "User_Inputs_Shiny": reactive_user_inputs, 
        "Inner_Variables_Shiny": reactive_inner_variables,  
        "Triggers_Shiny": reactive_triggers,  
        "Visual_Objects_Shiny": reactive_visual_objects  
    }
    
    return dict_reactives_shiny


def initialize_reactive_user_inputs(data_utils):
    """Initialize values for User_Inputs_Shiny category in the reactives_shiny structures using defensive programming."""
    
    # Input validation with early returns
    validation_result, validation_message = validate_data_utils_parameter(data_utils)
    if not validation_result:
        raise ValueError(f"Data utils validation failed: {validation_message}")
    
    # Configuration validation - define reactive inputs mapping to all subtab modules
    reactive_inputs_config = {
        "Input_Tab_Portfolios_Subtab_Comparison_Time_Period": None,
        "Input_Tab_Portfolios_Subtab_Comparison_Date_Range": None,
        "Input_Tab_Portfolios_Subtab_Comparison_Viz_Type": None,
        "Input_Tab_Portfolios_Subtab_Comparison_Show_Diff": None,
        "Input_Tab_Portfolios_Subtab_Portfolios_Analysis_Time_Period": None,
        "Input_Tab_Portfolios_Subtab_Portfolios_Analysis_Date_Range": None,
        "Input_Tab_Portfolios_Subtab_Portfolios_Analysis_Type": None,
        "Input_Tab_Portfolios_Subtab_Portfolios_Analysis_Rolling_Window": None,
        "Input_Tab_Portfolios_Subtab_Portfolios_Analysis_Include_Benchmark": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_Name": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_Age_Current": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_Age_Retirement": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_Age_Income_Starting": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_Status_Marital": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_Gender": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_Tolerance_Risk": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_State": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Primary_Code_Zip": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_Name": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_Age_Current": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_Age_Retirement": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_Age_Income_Starting": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_Status_Marital": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_Gender": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_Tolerance_Risk": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_State": None,
        "Input_Tab_Investors_Subtab_Investors_Personal_Info_Investor_Partner_Code_Zip": None,
        "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Primary_Assets_Taxable": None,
        "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Primary_Assets_Tax_Deferred": None,
        "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Primary_Assets_Tax_Free": None,
        "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Partner_Assets_Taxable": None,
        "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Partner_Assets_Tax_Deferred": None,
        "Input_Tab_Investors_Subtab_Investors_Assets_Investor_Partner_Assets_Tax_Free": None,
        "Input_Tab_Investors_Subtab_Investors_Goals_Investor_Primary_Goal_Essential": None,
        "Input_Tab_Investors_Subtab_Investors_Goals_Investor_Primary_Goal_Important": None,
        "Input_Tab_Investors_Subtab_Investors_Goals_Investor_Primary_Goal_Aspirational": None,
        "Input_Tab_Investors_Subtab_Investors_Goals_Investor_Partner_Goal_Essential": None,
        "Input_Tab_Investors_Subtab_Investors_Goals_Investor_Partner_Goal_Important": None,
        "Input_Tab_Investors_Subtab_Investors_Goals_Investor_Partner_Goal_Aspirational": None,
        "Input_Tab_Investors_Subtab_Investors_Income_Investor_Primary_Income_Social_Security": None,
        "Input_Tab_Investors_Subtab_Investors_Income_Investor_Primary_Income_Pension": None,
        "Input_Tab_Investors_Subtab_Investors_Income_Investor_Primary_Income_Annuity_Existing": None,
        "Input_Tab_Investors_Subtab_Investors_Income_Investor_Primary_Income_Other": None,
        "Input_Tab_Investors_Subtab_Investors_Income_Investor_Partner_Income_Social_Security": None,
        "Input_Tab_Investors_Subtab_Investors_Income_Investor_Partner_Income_Pension": None,
        "Input_Tab_Investors_Subtab_Investors_Income_Investor_Partner_Income_Annuity_Existing": None,
        "Input_Tab_Investors_Subtab_Investors_Income_Investor_Partner_Income_Other": None
    }
    
    # Business logic validation - create reactive values safely
    reactive_user_inputs = {}
    for reactive_key_name, initial_value in reactive_inputs_config.items():
        reactive_user_inputs[reactive_key_name] = create_reactive_value_safely(initial_value)
    
    return reactive_user_inputs


def initialize_reactive_inner_variables(data_utils):
    """Initialize reactive values for Inner_Variables_Shiny category in the reactives_shiny structures using defensive programming.
    
    Args:
        data_utils: Additional data for reactive value initialization
        
    Returns:
        dict: Dictionary containing reactive values for Inner_Variables_Shiny category in the reactives_shiny structures.
        
    Raises:
        ValueError: If data_utils is invalid
    """
    
    # Input validation with early returns
    validation_result, validation_message = validate_data_utils_parameter(data_utils)
    if not validation_result:
        raise ValueError(f"Data utils validation failed: {validation_message}")
    
    # Configuration validation - define inner variables
    inner_variables_config = {
        "Data_Personal_Info_DF": None,
        "Data_Assets_DF": None,
        "Data_Goals_DF": None,
        "Data_Income_DF": None
    }
    
    # Business logic validation - create reactive values safely
    reactive_inner_variables = {}
    for variable_key_name, initial_value in inner_variables_config.items():
        reactive_inner_variables[variable_key_name] = create_reactive_value_safely(initial_value)
    
    return reactive_inner_variables


def initialize_reactive_triggers(data_utils):
    """Initialize reactive values for Triggers_Shiny category in the reactives_shiny structures using defensive programming.
    
    Args:
        data_utils: Additional data for reactive value initialization
        
    Returns:
        dict: Dictionary containing reactive values for Triggers_Shiny category in the reactives_shiny structures.
        
    Raises:
        ValueError: If data_utils is invalid
    """
    
    # Input validation with early returns
    validation_result, validation_message = validate_data_utils_parameter(data_utils)
    if not validation_result:
        raise ValueError(f"Data utils validation failed: {validation_message}")
    
    # Configuration validation - define triggers
    triggers_config = {
        "Temp_Trigger_One": None
    }
    
    # Business logic validation - create reactive values safely
    reactive_triggers = {}
    for trigger_key_name, initial_value in triggers_config.items():
        reactive_triggers[trigger_key_name] = create_reactive_value_safely(initial_value)
    
    return reactive_triggers


def initialize_reactive_visual_objects(data_utils):
    """Initialize reactive values for Visual_Objects_Shiny category in the reactives_shiny structures using defensive programming.
    
    Args:
        data_utils: Additional data for reactive value initialization
        
    Returns:
        dict: Dictionary containing reactive values for Visual_Objects_Shiny category in the reactives_shiny structures.
        
    Raises:
        ValueError: If data_utils is invalid
    """
    
    # Input validation with early returns
    validation_result, validation_message = validate_data_utils_parameter(data_utils)
    if not validation_result:
        raise ValueError(f"Data utils validation failed: {validation_message}")
    
    # Configuration validation - define visual objects
    visual_objects_config = {
        "Table_Personal_Info": None,
        "Table_Assets": None,
        "Table_Goals": None,
        "Table_Income": None
    }
    
    # Business logic validation - create reactive values safely
    reactive_visual_objects = {}
    for visual_key_name, initial_value in visual_objects_config.items():
        reactive_visual_objects[visual_key_name] = create_reactive_value_safely(initial_value)
    
    return reactive_visual_objects


def get_value_from_reactives_shiny(
    reactives_shiny, 
    key_name, 
    key_category
):
    """Get a value from reactives dictionary using specific category with defensive programming.
    
    This function retrieves values from reactive variables with explicit error handling,
    throwing detailed errors for all failure scenarios rather than returning default values.
    Error messages include the key_name and key_category for better debugging.
    
    Args:
        reactives_shiny: Dictionary containing reactive values organized by category
        key_name: The key name to search for in the specified category
        key_category: The category to search in ("User_Inputs_Shiny", "Inner_Variables_Shiny", 
                     "Triggers_Shiny", or "Visual_Objects_Shiny")
        
    Returns:
        The value from the reactive variable (any type, including None if that's the actual stored value)
        
    Raises:
        ValueError: If reactives_shiny is None/invalid, key_category is invalid, 
                   key_name is None/empty, or reactive variable is invalid
        KeyError: If key_name is not found in the specified category or category doesn't exist
        RuntimeError: If reactive value retrieval fails unexpectedly
        TypeError: If reactive variable doesn't have required methods
    """
    
    # Input validation with early returns - validate key_name first for better error messages
    if key_name is None:
        raise ValueError("key_name cannot be None")
    
    if not isinstance(key_name, str):
        raise ValueError(f"key_name must be string, got {type(key_name).__name__}: '{key_name}'")
    
    if len(key_name.strip()) == 0:
        raise ValueError(f"key_name cannot be empty string: '{key_name}'")
    
    # Clean key_name for consistent processing
    key_name_cleaned = key_name.strip()
    
    # Validate key_category with enhanced error messages
    if key_category is None:
        raise ValueError(f"key_category cannot be None (searching for key_name: '{key_name_cleaned}')")
    
    if not isinstance(key_category, str):
        raise ValueError(f"key_category must be string, got {type(key_category).__name__}: '{key_category}' (searching for key_name: '{key_name_cleaned}')")
    
    if len(key_category.strip()) == 0:
        raise ValueError(f"key_category cannot be empty string: '{key_category}' (searching for key_name: '{key_name_cleaned}')")
    
    # Clean key_category for consistent processing
    key_category_cleaned = key_category.strip()
    
    # Validate reactives_shiny structure with enhanced error messages
    if reactives_shiny is None:
        raise ValueError(f"reactives_shiny dictionary cannot be None (searching for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}')")
    
    if not isinstance(reactives_shiny, dict):
        raise ValueError(f"reactives_shiny must be a dictionary, got {type(reactives_shiny).__name__} (searching for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}')")
    
    # Configuration validation - check required categories with enhanced error messages
    required_categories = [
        "User_Inputs_Shiny", 
        "Inner_Variables_Shiny", 
        "Triggers_Shiny", 
        "Visual_Objects_Shiny"
    ]
    
    # Validate that key_category is a valid category
    if key_category_cleaned not in required_categories:
        raise ValueError(f"Invalid key_category: '{key_category_cleaned}'. Valid categories: {required_categories} (searching for key_name: '{key_name_cleaned}')")
    
    # Check that all required categories exist in reactives_shiny
    missing_categories = []
    for category_name in required_categories:
        if category_name not in reactives_shiny:
            missing_categories.append(category_name)
        elif not isinstance(reactives_shiny[category_name], dict):
            raise ValueError(f"Category '{category_name}' must be a dictionary, got {type(reactives_shiny[category_name]).__name__} (searching for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}')")
    
    if missing_categories:
        available_categories = list(reactives_shiny.keys())
        raise ValueError(f"Required categories missing from reactives_shiny: {missing_categories}. Available categories: {available_categories} (searching for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}')")
    
    # Business logic validation - get the specific category
    category_dict = reactives_shiny.get(key_category_cleaned)
    if category_dict is None:
        # This should not happen due to above validation, but defensive programming
        available_categories = list(reactives_shiny.keys())
        raise KeyError(f"Category '{key_category_cleaned}' not found in reactives_shiny. Available categories: {available_categories} (searching for key_name: '{key_name_cleaned}')")
    
    # Validate that the specific key exists in the category
    if key_name_cleaned not in category_dict:
        available_keys = list(category_dict.keys())
        if not available_keys:
            raise KeyError(f"Key '{key_name_cleaned}' not found in category '{key_category_cleaned}' - category is empty (no keys available)")
        else:
            # Provide helpful suggestions if key is similar to existing keys
            similar_keys = [key for key in available_keys if key_name_cleaned.lower() in key.lower() or key.lower() in key_name_cleaned.lower()]
            if similar_keys:
                raise KeyError(f"Key '{key_name_cleaned}' not found in category '{key_category_cleaned}'. Available keys: {available_keys}. Similar keys found: {similar_keys}")
            else:
                raise KeyError(f"Key '{key_name_cleaned}' not found in category '{key_category_cleaned}'. Available keys: {available_keys}")
    
    # Get the reactive variable safely
    reactive_variable = category_dict[key_name_cleaned]
    
    # Validate reactive variable exists and is not None
    if reactive_variable is None:
        raise ValueError(f"Reactive variable is None for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}' - reactive variable was not properly initialized")
    
    # Validate that reactive variable has the required 'get' method
    if not hasattr(reactive_variable, 'get'):
        available_methods = [method for method in dir(reactive_variable) if not method.startswith('_')]
        raise TypeError(f"Reactive variable for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}' does not have 'get' method. Object type: {type(reactive_variable).__name__}. Available methods: {available_methods}")
    
    # Validate that the 'get' method is callable
    if not callable(getattr(reactive_variable, 'get')):
        raise TypeError(f"Reactive variable 'get' attribute for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}' is not callable. Object type: {type(reactive_variable).__name__}. 'get' type: {type(getattr(reactive_variable, 'get')).__name__}")
    
    # Attempt to retrieve the value with comprehensive error handling
    try:
        retrieved_value = reactive_variable.get()
        
        # Log successful retrieval for debugging purposes
        logging.debug(f"Successfully retrieved value from reactive variable for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}'. Value type: {type(retrieved_value).__name__}")
        
        # Return the actual value (including None if that's what was stored)
        return retrieved_value
        
    except AttributeError as exc:
        # Handle cases where get() method doesn't exist or has issues
        raise RuntimeError(f"AttributeError accessing reactive value for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}'. Reactive variable type: {type(reactive_variable).__name__}. Error: {exc}") from exc
        
    except RuntimeError as exc:
        # Handle Shiny reactive runtime errors (e.g., reactive context issues)
        raise RuntimeError(f"RuntimeError accessing reactive value for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}'. This may indicate a reactive context issue. Error: {exc}") from exc
        
    except ValueError as exc:
        # Handle value-related errors during retrieval
        raise RuntimeError(f"ValueError accessing reactive value for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}'. Error: {exc}") from exc
        
    except TypeError as exc:
        # Handle type-related errors during retrieval
        raise RuntimeError(f"TypeError accessing reactive value for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}'. Reactive variable type: {type(reactive_variable).__name__}. Error: {exc}") from exc
        
    except KeyError as exc:
        # Handle key-related errors during retrieval (though this should be rare for get())
        raise RuntimeError(f"KeyError accessing reactive value for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}'. Error: {exc}") from exc
        
    except Exception as exc:
        # Handle any other unexpected errors with full context
        exc_type = type(exc).__name__
        exc_module = getattr(type(exc), '__module__', 'unknown')
        reactive_type = type(reactive_variable).__name__
        reactive_module = getattr(type(reactive_variable), '__module__', 'unknown')
        
        raise RuntimeError(f"Unexpected {exc_type} error accessing reactive value for key_name: '{key_name_cleaned}' in key_category: '{key_category_cleaned}'. Reactive variable type: {reactive_type} from {reactive_module}. Exception type: {exc_type} from {exc_module}. Error: {exc}") from exc


def set_value_to_reactives_shiny(reactives_shiny, key_name, key_category, input_value):
    """Set value to a variable within reactives dictionary using specific category with defensive programming.
    
    Args:
        reactives_shiny: Dictionary containing reactive values organized by category
        key_name: The key name to search for in the specified category
        key_category: The category to search in ("User_Inputs_Shiny", "Inner_Variables_Shiny", 
                     "Triggers_Shiny", or "Visual_Objects_Shiny")
        input_value: The value to set in the reactive variable
        
    Returns:
        dict: Updated reactives dictionary
        
    Raises:
        KeyError: If key_name is not found in the specified category
        ValueError: If reactives_shiny is None, invalid, or key_category is invalid
    """
    
    # Input validation with early returns
    validation_result, validation_message = validate_reactives_shiny_structure(reactives_shiny)
    if not validation_result:
        error_message = f"Reactives structure validation failed: {validation_message}"
        logging.error(error_message)
        raise ValueError(error_message)
    
    validation_result, validation_message = validate_category_name(key_category)
    if not validation_result:
        error_message = f"Category validation failed: {validation_message}"
        logging.error(error_message)
        raise ValueError(error_message)
    
    # Business logic validation - get category
    category_dict = reactives_shiny.get(key_category)
    if category_dict is None:
        available_categories = list(reactives_shiny.keys())
        error_message = f"Category '{key_category}' not found. Available categories: {available_categories}"
        logging.error(error_message)
        raise KeyError(error_message)
    
    # Validate key access
    validation_result, validation_message = validate_reactive_key_access(category_dict, key_name, key_category)
    if not validation_result:
        error_message = f"Key access validation failed: {validation_message}"
        logging.error(error_message)
        raise KeyError(error_message)
    
    # Get the reactive variable safely
    reactive_variable = category_dict[key_name]
    
    # Defensive programming - safe value setting
    if reactive_variable is None:
        error_message = f"Reactive variable '{key_name}' in category '{key_category}' is None"
        logging.error(error_message)
        raise ValueError(error_message)
    
    if not hasattr(reactive_variable, 'set'):
        error_message = f"Reactive variable '{key_name}' in category '{key_category}' does not have 'set' method"
        logging.error(error_message)
        raise ValueError(error_message)
    
    # Only use try-except for reactive value setting that might fail unpredictably
    try:
        reactive_variable.set(input_value)
        logging.debug(f"Set value in {key_category} for key '{key_name}': {input_value}")
        return reactives_shiny
    except Exception as exc:
        error_message = f"Unexpected error setting reactive value for key '{key_name}' in category '{key_category}' to '{input_value}': {exc}"
        logging.error(error_message)
        raise RuntimeError(error_message) from exc
    

def safe_get_reactive_value(reactive_input, default_value=None):
    """Safely get value from reactive input with proper error handling.
    
    Args:
        reactive_input: Shiny reactive input object
        default_value: Default value to return if input is None or inaccessible
        
    Returns:
        Value from reactive input or default value
    """
    # Input validation with early returns
    if reactive_input is None:
        return default_value
    
    # Only use try-except for reactive value access that might fail unpredictably
    try:
        Reactive_Value = reactive_input()
        return Reactive_Value if Reactive_Value is not None else default_value
    except Exception:
        return default_value


   
def safe_get_value_from_shiny_input_text(
    input_reactive_object,
    default_value: str = ""
) -> str:
    """Safely retrieve and validate text input values following coding standards.
    
    Args:
        input_reactive_object: The actual reactive input object (e.g., input.input_ID_...)
        default_value: Default value if input is invalid or None
        
    Returns:
        str: Validated text value
    """
    # Input validation with early returns
    if input_reactive_object is None:
        return default_value
    
    try:
        # Get the reactive value using () to call the reactive function
        raw_value = input_reactive_object()
        
        # Configuration validation - ensure value exists
        if raw_value is None:
            return default_value
        
        # Input validation - convert to string and clean
        if isinstance(raw_value, str):
            cleaned_value = raw_value.strip()
        else:
            cleaned_value = str(raw_value).strip()
        
        # Return validated value
        return cleaned_value if cleaned_value else default_value
        
    except (AttributeError, RuntimeError, ValueError, TypeError):
        # Defensive programming - handle all expected errors
        return default_value


def safe_get_value_from_shiny_input_numeric(
    input_reactive_object,
    default_value: float = 0.0
) -> float:
    """Safely retrieve and validate numeric input values following coding standards.
    
    Args:
        input_reactive_object: The actual reactive input object (e.g., input.input_ID_...)
        default_value: Default value if input is invalid or None
        
    Returns:
        float: Validated numeric value
    """
    # Input validation with early returns
    if input_reactive_object is None:
        return default_value
    
    try:
        # Get the reactive value using () to call the reactive function
        raw_value = input_reactive_object()
        
        # Configuration validation - ensure value exists
        if raw_value is None:
            return default_value
        
        # Input validation - handle different value types
        if isinstance(raw_value, (int, float)):
            return max(0.0, float(raw_value))
        
        if isinstance(raw_value, str):
            # Extract numeric value from formatted currency string
            cleaned_value = raw_value.replace('$', '').replace(',', '').strip()
            if cleaned_value:
                try:
                    numeric_value = float(cleaned_value)
                    return max(0.0, numeric_value)
                except (ValueError, TypeError):
                    return default_value
            else:
                return default_value
        
        # Business logic validation - default for unexpected types
        return default_value
        
    except (AttributeError, RuntimeError, ValueError, TypeError):
        # Defensive programming - handle all expected errors
        return default_value


  
def get_value_from_shiny_input_text(input_reactive_object) -> str:
    """Retrieve and validate string value from shiny text_input with explicit error handling.
    
    This function retrieves text values from Shiny reactive inputs and validates them,
    throwing explicit errors for invalid inputs rather than returning default values.
    The error messages include the reactive input identifier for better debugging.
    
    Args:
        input_reactive_object: The actual reactive input object (e.g., input.input_ID_...)
        
    Returns:
        str: Validated text value (guaranteed to be a valid string)
        
    Raises:
        ValueError: If input_reactive_object is None, invalid, or contains empty text
        RuntimeError: If reactive value retrieval fails
        TypeError: If retrieved value cannot be converted to string
    """
    # Input validation with early returns
    if input_reactive_object is None:
        raise ValueError("input_reactive_object cannot be None")
    
    # Configuration validation - ensure input object has callable interface
    if not callable(input_reactive_object):
        raise ValueError(f"input_reactive_object must be callable, got {type(input_reactive_object).__name__}")
    
    # Extract reactive input identifier for error reporting using simplified but effective approach
    reactive_input_identifier = "Unknown"
    try:
        # Method 1: Enhanced source code parsing - most reliable for Shiny inputs
        import inspect
        import linecache
        import re
        
        frame = inspect.currentframe()
        try:
            # Get the calling frame where this function was invoked
            caller_frame = frame.f_back
            if caller_frame:
                filename = caller_frame.f_code.co_filename
                line_number = caller_frame.f_lineno
                
                # Get the actual source code line that called this function
                source_line = linecache.getline(filename, line_number).strip()
                
                # Enhanced patterns to match various input access styles
                input_patterns = [
                    # Direct input access: input.input_ID_...
                    r'input\s*\.\s*(input_ID_[a-zA-Z0-9_]+)',
                    # Function call with input: get_value_from_shiny_input_text(input.input_ID_...)
                    r'get_value_from_shiny_input_text\s*\(\s*input\s*\.\s*(input_ID_[a-zA-Z0-9_]+)',
                    # Getattr style: getattr(input, 'input_ID_...')
                    r'getattr\s*\(\s*input\s*,\s*["\']?(input_ID_[a-zA-Z0-9_]+)["\']?\s*\)',
                    # Variable assignment: var = input.input_ID_...
                    r'=\s*input\s*\.\s*(input_ID_[a-zA-Z0-9_]+)',
                    # Function parameter: func(input.input_ID_...)
                    r'\(\s*input\s*\.\s*(input_ID_[a-zA-Z0-9_]+)',
                ]
                
                # Try each pattern to find the identifier
                for pattern in input_patterns:
                    match = re.search(pattern, source_line)
                    if match:
                        reactive_input_identifier = match.group(1)
                        break
                
                # If not found in current line, check surrounding lines
                if reactive_input_identifier == "Unknown" and line_number > 1:
                    # Check previous lines for multi-line function calls
                    for line_offset in range(1, 4):  # Check 3 lines above
                        prev_line_number = line_number - line_offset
                        if prev_line_number > 0:
                            prev_source_line = linecache.getline(filename, prev_line_number).strip()
                            for pattern in input_patterns:
                                match = re.search(pattern, prev_source_line)
                                if match:
                                    reactive_input_identifier = match.group(1)
                                    break
                            if reactive_input_identifier != "Unknown":
                                break
                
        finally:
            del frame  # Prevent reference cycles
        
        # Method 2: Frame variable inspection - backup method
        if reactive_input_identifier == "Unknown":
            frame = inspect.currentframe()
            try:
                caller_frame = frame.f_back
                max_depth = 3  # Limit depth to prevent performance issues
                current_depth = 0
                
                while caller_frame and reactive_input_identifier == "Unknown" and current_depth < max_depth:
                    current_depth += 1
                    
                    # Check local variables in the calling frame
                    if caller_frame.f_locals:
                        for var_name, var_value in caller_frame.f_locals.items():
                            # Direct match: variable is our reactive object and has input_ID_ in name
                            if var_value is input_reactive_object and 'input_ID_' in str(var_name):
                                reactive_input_identifier = str(var_name)
                                break
                            
                            # Input object inspection: look for input objects
                            elif var_name == 'input' and hasattr(var_value, '__dict__'):
                                # Check all attributes of the input object
                                try:
                                    for attr_name in dir(var_value):
                                        if (attr_name.startswith('input_ID_') and 
                                            hasattr(var_value, attr_name)):
                                            attr_obj = getattr(var_value, attr_name)
                                            if attr_obj is input_reactive_object:
                                                reactive_input_identifier = attr_name
                                                break
                                except (AttributeError, TypeError):
                                    pass
                                
                                if reactive_input_identifier != "Unknown":
                                    break
                    
                    # Move up one frame
                    caller_frame = caller_frame.f_back
                    
            finally:
                del frame  # Prevent reference cycles
        
        # Method 3: Object introspection - check common attributes
        if reactive_input_identifier == "Unknown":
            # Check standard identifier attributes
            identifier_attributes = ['__name__', '_name', 'name', '_id', 'id', '_key', 'key']
            for attr_name in identifier_attributes:
                if hasattr(input_reactive_object, attr_name):
                    try:
                        attr_value = getattr(input_reactive_object, attr_name)
                        if isinstance(attr_value, str) and 'input_ID_' in attr_value:
                            reactive_input_identifier = attr_value
                            break
                    except (AttributeError, TypeError):
                        pass
        
        # Method 4: String representation analysis
        if reactive_input_identifier == "Unknown":
            try:
                # Check object representation
                obj_repr = repr(input_reactive_object)
                obj_str = str(input_reactive_object)
                
                # Look for input_ID_ patterns in representations
                combined_text = f"{obj_repr} {obj_str}"
                match = re.search(r'input_ID_[a-zA-Z0-9_]+', combined_text)
                if match:
                    reactive_input_identifier = match.group(0)
                    
            except Exception:
                pass
        
        # Method 5: Enhanced fallback with more context
        if reactive_input_identifier == "Unknown":
            try:
                obj_type = type(input_reactive_object).__name__
                obj_module = getattr(type(input_reactive_object), '__module__', 'unknown')
                
                # Try to get a more meaningful identifier from the calling context
                frame = inspect.currentframe()
                try:
                    caller_frame = frame.f_back
                    if caller_frame and caller_frame.f_code:
                        func_name = caller_frame.f_code.co_name
                        filename = caller_frame.f_code.co_filename
                        line_number = caller_frame.f_lineno
                        
                        # Extract just the filename without path
                        import os
                        base_filename = os.path.basename(filename)
                        
                        reactive_input_identifier = f"Unknown_input_in_{func_name}_at_{base_filename}:{line_number}"
                    else:
                        reactive_input_identifier = f"Unknown_reactive_input_{obj_type}_from_{obj_module}"
                finally:
                    del frame
                    
            except Exception:
                reactive_input_identifier = "Unknown_reactive_input_object"
                
    except Exception:
        # Final fallback if all extraction methods fail
        reactive_input_identifier = "Unknown_reactive_input_object"
    
    try:
        # Get the reactive value using () to call the reactive function
        raw_value = input_reactive_object()
        
    except (AttributeError, RuntimeError) as exc:
        # Defensive programming - handle reactive access failures
        raise RuntimeError(f"Failed to retrieve value from reactive input '{reactive_input_identifier}': {exc}") from exc
    except Exception as exc:
        # Handle any other unexpected errors during reactive access
        raise RuntimeError(f"Unexpected error accessing reactive input '{reactive_input_identifier}': {exc}") from exc
    
    # Configuration validation - ensure value exists
    if raw_value is None:
        raise ValueError(f"Retrieved reactive value is None for input '{reactive_input_identifier}' - no text input provided")
    
    # Business logic validation - convert to string and clean
    try:
        if isinstance(raw_value, str):
            cleaned_value = raw_value.strip()
        else:
            cleaned_value = str(raw_value).strip()
            
    except (ValueError, TypeError) as exc:
        # Handle string conversion failures
        raise TypeError(f"Cannot convert retrieved value to string for input '{reactive_input_identifier}': {type(raw_value).__name__} - {exc}") from exc
    
    # Final validation - ensure we have a non-empty string
    if not cleaned_value:
        raise ValueError(f"Text input '{reactive_input_identifier}' is empty or contains only whitespace")
    
    # Return validated value
    return cleaned_value


def get_value_from_shiny_input_numeric(input_reactive_object) -> float:
    """Retrieve and validate numeric value from shiny numeric_input with explicit error handling.
    
    This function retrieves numeric values from Shiny reactive inputs and validates them,
    throwing explicit errors for invalid inputs rather than returning default values.
    The error messages include the reactive input identifier for better debugging.
    
    Args:
        input_reactive_object: The actual reactive input object (e.g., input.input_ID_...)
        
    Returns:
        float: Validated numeric value (guaranteed to be a valid non-negative float)
        
    Raises:
        ValueError: If input_reactive_object is None, invalid, or contains invalid numeric data
        RuntimeError: If reactive value retrieval fails
        TypeError: If retrieved value cannot be converted to float
    """
    # Input validation with early returns
    if input_reactive_object is None:
        raise ValueError("input_reactive_object cannot be None")
    
    # Configuration validation - ensure input object has callable interface
    if not callable(input_reactive_object):
        raise ValueError(f"input_reactive_object must be callable, got {type(input_reactive_object).__name__}")
    
    # Extract reactive input identifier for error reporting using simplified but effective approach
    reactive_input_identifier = "Unknown"
    try:
        # Method 1: Enhanced source code parsing - most reliable for Shiny inputs
        import inspect
        import linecache
        import re
        
        frame = inspect.currentframe()
        try:
            # Get the calling frame where this function was invoked
            caller_frame = frame.f_back
            if caller_frame:
                filename = caller_frame.f_code.co_filename
                line_number = caller_frame.f_lineno
                
                # Get the actual source code line that called this function
                source_line = linecache.getline(filename, line_number).strip()
                
                # Enhanced patterns to match various input access styles
                input_patterns = [
                    # Direct input access: input.input_ID_...
                    r'input\s*\.\s*(input_ID_[a-zA-Z0-9_]+)',
                    # Function call with input: get_value_from_shiny_input_numeric(input.input_ID_...)
                    r'get_value_from_shiny_input_numeric\s*\(\s*input\s*\.\s*(input_ID_[a-zA-Z0-9_]+)',
                    # Getattr style: getattr(input, 'input_ID_...')
                    r'getattr\s*\(\s*input\s*,\s*["\']?(input_ID_[a-zA-Z0-9_]+)["\']?\s*\)',
                    # Variable assignment: var = input.input_ID_...
                    r'=\s*input\s*\.\s*(input_ID_[a-zA-Z0-9_]+)',
                    # Function parameter: func(input.input_ID_...)
                    r'\(\s*input\s*\.\s*(input_ID_[a-zA-Z0-9_]+)',
                ]
                
                # Try each pattern to find the identifier
                for pattern in input_patterns:
                    match = re.search(pattern, source_line)
                    if match:
                        reactive_input_identifier = match.group(1)
                        break
                
                # If not found in current line, check surrounding lines
                if reactive_input_identifier == "Unknown" and line_number > 1:
                    # Check previous lines for multi-line function calls
                    for line_offset in range(1, 4):  # Check 3 lines above
                        prev_line_number = line_number - line_offset
                        if prev_line_number > 0:
                            prev_source_line = linecache.getline(filename, prev_line_number).strip()
                            for pattern in input_patterns:
                                match = re.search(pattern, prev_source_line)
                                if match:
                                    reactive_input_identifier = match.group(1)
                                    break
                            if reactive_input_identifier != "Unknown":
                                break
                
        finally:
            del frame  # Prevent reference cycles
        
        # Method 2: Frame variable inspection - backup method
        if reactive_input_identifier == "Unknown":
            frame = inspect.currentframe()
            try:
                caller_frame = frame.f_back
                max_depth = 3  # Limit depth to prevent performance issues
                current_depth = 0
                
                while caller_frame and reactive_input_identifier == "Unknown" and current_depth < max_depth:
                    current_depth += 1
                    
                    # Check local variables in the calling frame
                    if caller_frame.f_locals:
                        for var_name, var_value in caller_frame.f_locals.items():
                            # Direct match: variable is our reactive object and has input_ID_ in name
                            if var_value is input_reactive_object and 'input_ID_' in str(var_name):
                                reactive_input_identifier = str(var_name)
                                break
                            
                            # Input object inspection: look for input objects
                            elif var_name == 'input' and hasattr(var_value, '__dict__'):
                                # Check all attributes of the input object
                                try:
                                    for attr_name in dir(var_value):
                                        if (attr_name.startswith('input_ID_') and 
                                            hasattr(var_value, attr_name)):
                                            attr_obj = getattr(var_value, attr_name)
                                            if attr_obj is input_reactive_object:
                                                reactive_input_identifier = attr_name
                                                break
                                except (AttributeError, TypeError):
                                    pass
                                
                                if reactive_input_identifier != "Unknown":
                                    break
                    
                    # Move up one frame
                    caller_frame = caller_frame.f_back
                    
            finally:
                del frame  # Prevent reference cycles
        
        # Method 3: Object introspection - check common attributes
        if reactive_input_identifier == "Unknown":
            # Check standard identifier attributes
            identifier_attributes = ['__name__', '_name', 'name', '_id', 'id', '_key', 'key']
            for attr_name in identifier_attributes:
                if hasattr(input_reactive_object, attr_name):
                    try:
                        attr_value = getattr(input_reactive_object, attr_name)
                        if isinstance(attr_value, str) and 'input_ID_' in attr_value:
                            reactive_input_identifier = attr_value
                            break
                    except (AttributeError, TypeError):
                        pass
        
        # Method 4: String representation analysis
        if reactive_input_identifier == "Unknown":
            try:
                # Check object representation
                obj_repr = repr(input_reactive_object)
                obj_str = str(input_reactive_object)
                
                # Look for input_ID_ patterns in representations
                combined_text = f"{obj_repr} {obj_str}"
                match = re.search(r'input_ID_[a-zA-Z0-9_]+', combined_text)
                if match:
                    reactive_input_identifier = match.group(0)
                    
            except Exception:
                pass
        
        # Method 5: Enhanced fallback with more context
        if reactive_input_identifier == "Unknown":
            try:
                obj_type = type(input_reactive_object).__name__
                obj_module = getattr(type(input_reactive_object), '__module__', 'unknown')
                
                # Try to get a more meaningful identifier from the calling context
                frame = inspect.currentframe()
                try:
                    caller_frame = frame.f_back
                    if caller_frame and caller_frame.f_code:
                        func_name = caller_frame.f_code.co_name
                        filename = caller_frame.f_code.co_filename
                        line_number = caller_frame.f_lineno
                        
                        # Extract just the filename without path
                        import os
                        base_filename = os.path.basename(filename)
                        
                        reactive_input_identifier = f"Unknown_input_in_{func_name}_at_{base_filename}:{line_number}"
                    else:
                        reactive_input_identifier = f"Unknown_reactive_input_{obj_type}_from_{obj_module}"
                finally:
                    del frame
                    
            except Exception:
                reactive_input_identifier = "Unknown_reactive_input_object"
                
    except Exception:
        # Final fallback if all extraction methods fail
        reactive_input_identifier = "Unknown_reactive_input_object"
    
    try:
        # Get the reactive value using () to call the reactive function
        raw_value = input_reactive_object()
        
    except (AttributeError, RuntimeError) as exc:
        # Defensive programming - handle reactive access failures
        raise RuntimeError(f"Failed to retrieve value from reactive input '{reactive_input_identifier}': {exc}") from exc
    except Exception as exc:
        # Handle any other unexpected errors during reactive access
        raise RuntimeError(f"Unexpected error accessing reactive input '{reactive_input_identifier}': {exc}") from exc
    
    # Configuration validation - ensure value exists
    if raw_value is None:
        raise ValueError(f"Retrieved reactive value is None for input '{reactive_input_identifier}' - no numeric input provided")
    
    # Business logic validation - handle different value types and convert to float
    if isinstance(raw_value, (int, float)):
        try:
            numeric_value = float(raw_value)
            # Ensure non-negative value for financial data
            if numeric_value < 0:
                raise ValueError(f"Numeric input '{reactive_input_identifier}' contains negative value: {numeric_value}")
            return numeric_value
        except (ValueError, TypeError) as exc:
            raise TypeError(f"Cannot convert numeric value to float for input '{reactive_input_identifier}': {type(raw_value).__name__} - {exc}") from exc
    
    elif isinstance(raw_value, str):
        try:
            # Extract numeric value from formatted currency string
            cleaned_value = raw_value.replace('$', '').replace(',', '').strip()
            
            if not cleaned_value:
                raise ValueError(f"Numeric input '{reactive_input_identifier}' is empty or contains only formatting characters")
            
            numeric_value = float(cleaned_value)
            
            # Ensure non-negative value for financial data
            if numeric_value < 0:
                raise ValueError(f"Numeric input '{reactive_input_identifier}' contains negative value: {numeric_value}")
            
            return numeric_value
            
        except ValueError as exc:
            # Re-raise ValueError with context
            if "negative value" in str(exc):
                raise exc
            else:
                raise ValueError(f"Cannot parse numeric value from string for input '{reactive_input_identifier}': '{raw_value}' - {exc}") from exc
        except (TypeError, AttributeError) as exc:
            raise TypeError(f"Cannot process string value for input '{reactive_input_identifier}': {type(raw_value).__name__} - {exc}") from exc
    
    else:
        # Handle unexpected types
        raise TypeError(f"Numeric input '{reactive_input_identifier}' has unexpected type: {type(raw_value).__name__} (value: {raw_value})")
