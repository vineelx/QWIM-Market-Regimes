"""
QWIM Dashboard Main Application
===============================

![QWIM Dashboard](https://img.shields.io/badge/QWIM-Dashboard-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Shiny](https://img.shields.io/badge/shiny-for_python-orange)

## Overview

The QWIM Dashboard is a comprehensive time series analysis tool built with Python and Shiny
for visualizing and analyzing multiple time series data with focus on portfolio management
and financial analysis.

## Architecture

The dashboard follows a modular architecture with clear separation of concerns:

```mermaid
graph TD
    A[main_App.py] --> B[tab_portfolios]
    A --> C[utils_dashboard]
    B --> D[subtab_weights_distribution]
    B --> E[subtab_performance_analysis]
    C --> F[reactives_shiny]
    C --> G[utils_data]
    C --> H[utils_visuals]
```

## Features

!!! success "Core Features"
    - **Interactive Portfolio Analysis**: Real-time portfolio weight distribution visualization
    - **Time Series Analysis**: Comprehensive time series analysis with multiple visualization types
    - **Component Selection**: Dynamic ETF component selection with checkbox interface
    - **Statistical Analysis**: Advanced statistical metrics and correlation analysis
    - **Export Capabilities**: PNG export for plots and tables
    - **Responsive Design**: Mobile-friendly dashboard with Bootstrap themes

!!! info "Visualization Types"
    - Stacked Area Charts
    - Line Charts  
    - Bar Charts
    - Heatmaps
    - Pie Charts for composition analysis

## Technology Stack

=== "Frontend"
    - **Shiny for Python**: Interactive web framework
    - **Bootstrap**: Responsive CSS framework via shinyswatch
    - **Plotly**: Interactive visualizations
    - **HTML/CSS**: Custom styling

=== "Backend"  
    - **Python 3.11+**: Core programming language
    - **Polars**: High-performance DataFrame operations
    - **Pandas**: Data manipulation and analysis
    - **NumPy**: Numerical computations

=== "Data Processing"
    - **Time Series Analysis**: Custom time series utilities
    - **Statistical Computing**: NumPy-based calculations
    - **Data Validation**: Defensive programming approach

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd dashboard-QWIM

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Development mode
python src/dashboard/main_App.py

# Production mode  
QWIM_ENVIRONMENT=production python src/dashboard/main_App.py
```

### Access

- **Development**: http://127.0.0.1:8080
- **Production**: http://0.0.0.0:8000

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `QWIM_ENVIRONMENT` | `development` | Application environment (`development` or `production`) |

### File Structure

```
src/dashboard/
├── main_App.py                 # Main application entry point
├── modules_tab_portfolios/     # Portfolio analysis modules
│   ├── tab_portfolios.py       # Main portfolio tab
│   └── subtab_weights_distribution.py  # Weight distribution analysis
└── utils_dashboard/            # Utility modules
    ├── reactives_shiny.py      # Reactive value management
    ├── utils_data.py           # Data processing utilities
    └── utils_visuals.py        # Visualization utilities
```

## API Reference

### Classes

#### App
Main Shiny application instance that coordinates all dashboard functionality.

**Attributes:**
- `app_ui`: User interface definition
- `app_server`: Server-side logic

### Functions

#### get_data_inputs()
Load and prepare input data for the dashboard.

**Returns:**
- `dict`: Dictionary containing all input datasets

**Example:**
```python
data_inputs = get_data_inputs(project_dir=project_dir)
portfolio_data = data_inputs.get("Weights_My_Portfolio")
```

#### get_data_utils()  
Initialize data utility functions and configurations.

**Parameters:**
- `project_dir` (Path): Root directory of the project

**Returns:**
- `dict`: Dictionary containing utility functions and configurations

#### initialize_reactives_shiny()
Initialize reactive values for Shiny application state management.

**Parameters:**
- `data_utils` (dict): Data utility functions and configurations

**Returns:**
- `dict`: Dictionary containing initialized reactive values

**Raises:**
- `DashboardInitializationError`: If reactive initialization fails

### Server Functions

#### app_server()
Main server function that coordinates all dashboard functionality.

**Parameters:**
- `input`: Shiny input object containing user interactions
- `output`: Shiny output object for rendering results  
- `session`: Shiny session object for state management

**Features:**
- Reactive value initialization and management
- Tab navigation tracking
- Modal dialog handling
- Module coordination

## Dashboard Modules

### Portfolio Analysis Module

The portfolio analysis module provides comprehensive tools for analyzing portfolio weights
and performance over time.

**Key Features:**
- Weight distribution visualization
- Component selection interface  
- Time period filtering
- Statistical analysis
- Export capabilities

**Usage Example:**
```python
# Access portfolio module in server
portfolios_module_instance = tab_portfolios_server(
    id="ID_tab_portfolios",
    data_utils=data_utils,
    data_inputs=data_inputs, 
    reactives_shiny=reactives_shiny
)
```

### Reactive System

The dashboard uses Shiny's reactive system for real-time updates:

```python
# Reactive value initialization
reactives_shiny = initialize_reactives_shiny(data_utils=data_utils)

```

## Error Handling

The application implements comprehensive error handling following defensive programming principles:

!!! warning "Error Types"
    - `DashboardInitializationError`: Application startup failures
    - `DataLoadingError`: Data loading and processing errors
    - `ModuleInitializationError`: Module-specific initialization errors
    - `SilentInitializationException`: Non-critical initialization warnings

## Performance Considerations

!!! tip "Optimization Strategies"
    - **Data Downsampling**: Automatic downsampling for large datasets (>200 points)
    - **Lazy Loading**: Reactive calculations only when needed
    - **Efficient Data Structures**: Polars for high-performance data operations
    - **Memory Management**: Proper cleanup of temporary variables

## Development Guidelines

### Code Standards

Following the project's coding standards:

- **Naming**: `snake_case` for functions/variables, `CamelCase` for classes
- **Validation**: Input validation with early returns
- **Error Handling**: Defensive programming over try-except
- **Documentation**: Comprehensive docstrings and type hints

### Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src
```

## Deployment

### Development Deployment

```bash
# Start development server
python src/dashboard/main_App.py
```

### Production Deployment

```bash
# Set environment
export QWIM_ENVIRONMENT=production

# Start production server
python src/dashboard/main_App.py
```

!!! note "Production Notes"
    - Runs on `0.0.0.0:8000` for external access
    - Debug mode disabled
    - Reload disabled for stability

## Troubleshooting

### Common Issues

??? question "Dashboard won't start"
    - Check Python version (3.11+ required)
    - Verify all dependencies installed
    - Check project directory structure
    - Review error logs in `logs/` directory

??? question "Data not loading"
    - Verify data files exist in expected locations
    - Check file permissions
    - Review data format compatibility

??? question "Visualizations not updating"
    - Check reactive dependencies
    - Verify component selection state
    - Review browser console for JavaScript errors

## Contributing

Please follow the project's coding standards and include:

1. Comprehensive documentation
2. Input validation with early returns
3. Defensive programming practices
4. Type hints for all functions
5. Unit tests for new functionality

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-06-01 | Initial release with portfolio analysis |

## License

[Add license information here]

## Support

For support and questions:
- Check the troubleshooting section above
- Review logs in the `logs/` directory
- Contact the QWIM development team
"""

# =============================================================================
# Standard Library Imports
# =============================================================================

import copy  # Deep copying of objects for state management
import numpy as np  # Numerical computations and array operations
import os  # Operating system interface for environment variables
import pandas as pd  # Data manipulation and analysis library
import platform  # Access to underlying platform's identifying data
import sys  # System-specific parameters and functions
import time  # Time-related functions for performance monitoring
import traceback  # Extract, format and print stack traces
import typing  # Support for type hints and annotations
from datetime import datetime  # Date and time handling
import asyncio  # Asynchronous I/O support
from pathlib import Path  # Object-oriented filesystem paths

# =============================================================================
# Third-Party Visualization and Data Processing Imports  
# =============================================================================

import plotly.express as px  # High-level interface to plotly for quick plots
import plotly.graph_objects as go  # Low-level interface to plotly for custom plots
import polars as pl  # High-performance DataFrame library for large datasets
import shinyswatch  # Bootstrap themes for Shiny applications

# =============================================================================
# Shiny Framework Imports
# =============================================================================

from shiny import App, ui, render, reactive, Session

# =============================================================================
# Project Path Configuration
# =============================================================================

#: Root directory of the QWIM Dashboard project
#: Determined by navigating up from the current file location
project_dir = Path(__file__).parent.parent.parent

# Add project root to Python path for module imports
# This ensures all internal modules can be imported properly
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# =============================================================================
# Internal Module Imports - Utility Functions
# =============================================================================

# Reactive state management utilities
from src.dashboard.utils_dashboard.reactives_shiny import (
    initialize_reactives_shiny,  # Initialize reactive values for application state
    get_value_from_reactives_shiny)  # Retrieve values from reactive dictionary

# Data processing and utility functions
from src.dashboard.utils_dashboard.utils_data import (
    get_data_inputs,  # Load and prepare input datasets
    get_data_utils)  # Initialize data utility functions and configurations

# Error handling classes following defensive programming principles
from src.dashboard.utils_dashboard.utils_errors import (
    SilentInitializationException,  # Non-critical initialization warnings
    DashboardInitializationError,  # Critical application startup failures
    DataLoadingError,  # Data loading and processing errors
    ModuleInitializationError)  # Module-specific initialization errors

# =============================================================================
# Configuration and Environment Setup
# =============================================================================

#: Application environment type (development or production)
#: Controls server configuration, debug settings, and deployment options
#: 
#: - development: Local development with debug mode and auto-reload
#: - production: Production deployment with optimized settings
ENVIRONMENT = os.environ.get("QWIM_ENVIRONMENT", "development").lower()

# =============================================================================
# Data Initialization
# =============================================================================

#: Dictionary containing data utility functions and configurations
#: Provides access to data processing, validation, and transformation utilities
data_utils = get_data_utils(project_dir=project_dir)

#: Dictionary containing all input datasets for the dashboard
#: Includes portfolio data, benchmark data, weights, and time series information
data_inputs = get_data_inputs(project_dir=project_dir)

# Create logs directory for application logging and error tracking
# Ensures logs directory exists for runtime error reporting and debugging
(project_dir / "logs").mkdir(exist_ok=True)

# =============================================================================
# Internal Module Imports - Dashboard Components
# =============================================================================


from src.dashboard.modules_tab_portfolios.tab_portfolios import (
    tab_portfolios_ui,  # Portfolio tab user interface components
    tab_portfolios_server)  # Portfolio tab server-side logic

from src.dashboard.modules_tab_investors.tab_investors import (
    tab_investors_ui,  # Investors tab user interface components
    tab_investors_server)  # Investors tab server-side logic

# =============================================================================
# UI Component Functions
# =============================================================================


def create_about_modal():
    """
    Create the About modal dialog with comprehensive application information.
    
    This modal provides users with detailed information about the dashboard
    including features, technology stack, version details, and platform information.
    
    ## Modal Content Structure
    
    The modal is organized into the following sections:
    
    1. **Features**: Core dashboard capabilities and functionality
    2. **Technology Stack**: Technical components and frameworks used
    3. **Supported Analysis**: Types of analysis available
    4. **Version Information**: Technical details about the current deployment
    
    ## Returns
    
    Returns:
        shiny.ui.modal: Configured modal dialog component with comprehensive
        application information formatted using Bootstrap styling.
        
    ## Usage Example
    
    ```python
    # Create and display the modal
    about_modal = create_about_modal()
    ui.modal_show(about_modal)
    ```
    
    ## Modal Features
    
    - **Responsive Design**: Adapts to different screen sizes
    - **Easy Close**: Can be dismissed by clicking outside or close button
    - **Rich Content**: Includes lists, formatted text, and highlighted sections
    - **Version Info**: Dynamic version and platform information
    
    ## Styling
    
    Uses Bootstrap classes for consistent appearance:
    - `bg-light`: Light background for version information section
    - `p-3`: Padding for content spacing
    - `rounded`: Rounded corners for modern appearance
    - `btn-primary`: Primary button styling for close button
    
    ## Notes
    
    !!! info "Dynamic Content"
        Version information is generated dynamically based on the current
        Python environment and platform, ensuring accuracy across deployments.
        
    !!! tip "Customization"
        The modal content can be easily modified to include additional
        sections or updated feature descriptions as the dashboard evolves.
    """
    return ui.modal(
        # Modal header with application title
        ui.h3("About QWIM Dashboard"),
        ui.p("The QWIM Dashboard is a comprehensive time series analysis tool built with Python and Shiny."),
        
        # Features section highlighting core capabilities
        ui.h5("🚀 Features:"),
        ui.tags.ul(
            ui.tags.li("Interactive time series visualization with multiple chart types"),
            ui.tags.li("Dynamic ETF component selection and filtering"),
            ui.tags.li("Statistical analysis and portfolio weight distribution"),
            ui.tags.li("Real-time reactive updates and synchronization"),
            ui.tags.li("Customizable time period selection and analysis"),
            ui.tags.li("Export capabilities for plots and statistical tables")
        ),
        
        # Technology stack section with technical details
        ui.h5("🛠️ Technology Stack:"),
        ui.tags.ul(
            ui.tags.li("Python 3.11+ for core functionality"),
            ui.tags.li("Shiny for Python for interactive dashboard framework"),
            ui.tags.li("Plotly for interactive and responsive visualizations"),
            ui.tags.li("Polars for high-performance time series processing"),
            ui.tags.li("NumPy and Pandas for numerical computations"),
            ui.tags.li("Bootstrap themes via shinyswatch for responsive design")
        ),
        
        # Analysis capabilities section
        ui.h5("📊 Supported Analysis:"),
        ui.tags.ul(
            ui.tags.li("Portfolio weight distribution over time"),
            ui.tags.li("Component-wise statistical analysis"),
            ui.tags.li("Time period filtering and comparison"),
            ui.tags.li("Multiple visualization formats (area, line, bar, heatmap)")
        ),
        
        # Dynamic version information section
        ui.h5("ℹ️ Version Information:"),
        ui.div(
            ui.p(f"**Dashboard Version:** 1.0.0"),
            ui.p(f"**Python Version:** {platform.python_version()}"),
            ui.p(f"**Platform:** {platform.system()} {platform.release()}"),
            ui.p(f"**Environment:** {ENVIRONMENT.title()}"),
            class_="bg-light p-3 rounded"  # Bootstrap styling for highlighted section
        ),
        
        # Footer with generation timestamp
        ui.hr(),
        ui.p(ui.tags.small(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")),
        
        # Modal configuration
        title="About QWIM Dashboard",
        size="l",  # Large modal size for comprehensive content
        easy_close=True,  # Allow closing by clicking outside modal
        footer=ui.modal_button("Close", class_="btn-primary")
    )


#: Pre-created About modal instance for consistent presentation
#: Avoids recreating the modal on each display request
about_modal = create_about_modal()


def create_app_ui():
    """
    Create the main application user interface.
    
    This function defines the primary UI layout using a navbar-based design
    that provides intuitive navigation and professional appearance.
    
    ## UI Architecture
    
    The interface follows a hierarchical structure:
    
    ```
    page_navbar (main container)
    ├── nav_panel (QWIM Portfolios tab)
    │   └── tab_portfolios_ui (portfolio analysis interface)
    ├── nav_spacer (flexible spacing)
    └── nav_control (About button)
    ```
    
    ## Layout Components
    
    ### Main Navigation
    - **Portfolio Tab**: Primary functionality for portfolio analysis
    - **About Button**: Access to application information and help
    
    ### Theme and Styling
    - **Flatly Theme**: Modern, professional Bootstrap theme via shinyswatch
    - **Responsive Design**: Adapts to different screen sizes and devices
    - **Fillable Layout**: Optimizes space usage for data visualization
    
    ## Returns
    
    Returns:
        shiny.ui.page_navbar: Main application UI layout configured with
        portfolio analysis functionality and navigation components.
        
    ## Configuration Details
    
    ### Navbar Settings
    - `title`: Application branding displayed in navigation bar
    - `theme`: Bootstrap theme for consistent visual appearance
    - `fillable`: Enables responsive layout optimization
    - `id`: Unique identifier for reactive navigation tracking
    
    ### Component IDs
    Following project naming conventions:
    - `ID_tab_portfolios`: Main portfolio analysis tab
    - `input_ID_show_about`: About button for modal display
    - `input_ID_navbar_main`: Navigation bar for tab tracking
    
    ## Usage Example
    
    ```python
    # Create the main UI
    app_ui = create_app_ui()
    
    # Use in Shiny app
    app = App(app_ui, app_server)
    ```
    
    ## Extensibility
    
    To add new tabs to the dashboard:
    
    ```python
    # Add additional nav_panel entries before nav_spacer
    ui.nav_panel(
        "New Tab Name",
        new_tab_ui("ID_new_tab", data_utils=data_utils, data_inputs=data_inputs)
    ),
    ```
    
    ## Notes
    
    !!! info "Theme Selection"
        The Flatly theme provides a modern, professional appearance suitable
        for financial and analytical applications.
        
    !!! tip "Navigation Pattern"
        The nav_spacer() pushes the About button to the right side of the
        navigation bar, following standard web design patterns.
        
    !!! warning "ID Conventions"
        All component IDs follow the project naming standards with descriptive
        prefixes (input_, output_, ID_) for consistency and maintainability.
    """
    return ui.page_navbar(

        ui.nav_panel(
            "Investors", 
            tab_investors_ui(
                "ID_tab_investors",  # Unique module identifier
                data_utils=data_utils,  # Utility functions and configuration
                data_inputs=data_inputs)  # Input datasets for analysis
        ),

        # portfolio analysis tab
        ui.nav_panel(
            "QWIM Portfolios",
            tab_portfolios_ui(
                "ID_tab_portfolios",  # Unique module identifier
                data_utils=data_utils,  # Utility functions and configuration
                data_inputs=data_inputs)  # Input datasets for analysis
        ),
        
        # Navigation spacer to push subsequent elements to the right
        # Creates proper visual separation between main content and utility buttons
        ui.nav_spacer(),
        
        # About button in navigation bar for application information
        # Provides users with help, features overview, and version details
        ui.nav_control(
            ui.input_action_button(
                "input_ID_show_about",  # Button identifier following naming convention
                "About",  # Button label
                class_="btn-outline-light me-2")  # Bootstrap styling classes
        ),
        
        # Application-level configuration settings
        title="QWIM Dashboard",  # Application title displayed in browser and navbar
        theme=shinyswatch.theme.flatly(),  # Modern Bootstrap theme for professional appearance
        id="input_ID_navbar_main",  # Unique identifier for reactive navigation tracking
        fillable=True  # Enable responsive fillable layout for optimal space usage
    )


#: Main application UI instance
#: Created once for use by the Shiny App constructor
app_ui = create_app_ui()


# =============================================================================
# Server Logic Functions
# =============================================================================


def app_server(input, output, session):
    """
    Main server function for the QWIM Dashboard application.
    
    This function serves as the central coordinator for all server-side functionality,
    managing reactive state, navigation tracking, modal dialogs, and module initialization.
    
    ## Server Architecture
    
    The server follows a coordinated modular pattern:
    
    ```mermaid
    graph TD
        A[app_server] --> B[Reactive Values]
        A --> C[Navigation Tracking]
        A --> D[Modal Handling]
        A --> E[Module Servers]
        B --> F[Portfolio Module]
        E --> F
    ```
    
    ## Core Responsibilities
    
    1. **Reactive State Management**: Initialize and coordinate reactive values
    2. **Navigation Tracking**: Monitor and respond to tab changes
    3. **Modal Dialog Handling**: Manage About dialog display
    4. **Module Coordination**: Initialize and coordinate specialized modules
    
    ## Parameters
    
    Args:
        input: Shiny input object containing user interface interactions.
            Provides access to reactive values from UI components.
            Access pattern: `input.component_id()` for reactive values,
            `input.component_id.get()` for current values.
            
        output: Shiny output object for rendering UI components.
            Used by modules to render plots, tables, and other outputs.
            Define outputs using `@output.component_id` decorator pattern.
            
        session: Shiny session object for session-specific functionality.
            Handles user session state, authentication, and communication.
            Provides session-level utilities and information.
    
    ## Reactive System Components
    
    ### State Management
    The server maintains centralized reactive state through:
    - `reactives_shiny`: Dictionary of application-wide reactive values
    - `current_tab`: Reactive value tracking active navigation tab
    
    ### Reactive Effects
    - `_update_reactives_shiny()`: Updates state based on input events
    - `_track_selected_tab()`: Monitors navigation tab changes
    - `_show_about_modal()`: Displays About dialog on button click
    
    ## Error Handling
    
    Implements defensive programming principles:
    - Early validation of reactive value initialization
    - Comprehensive error reporting with descriptive messages
    - Graceful degradation for non-critical functionality
    
    ## Raises
    
    DashboardInitializationError: If reactive values cannot be initialized.
        This is a critical error that prevents dashboard functionality.
        
    ## Usage Example
    
    ```python
    # This function is automatically called by Shiny framework
    app = App(app_ui, app_server)
    app.run()
    ```
    
    ## Module Integration
    
    The server initializes the portfolio analysis module:
    
    ```python
    portfolios_module_instance = tab_portfolios_server(
        id="ID_tab_portfolios",
        data_utils=data_utils,
        data_inputs=data_inputs,
        reactives_shiny=reactives_shiny
    )
    ```
    
    ## Performance Considerations
    
    - Reactive effects only trigger when relevant inputs change
    - Module initialization is performed once during startup
    - Shared data objects are passed by reference to minimize memory usage
    
    ## Notes
    
    !!! info "Reactive Programming"
        The server leverages Shiny's reactive programming model for efficient
        updates and real-time responsiveness to user interactions.
        
    !!! warning "Error Handling"
        Critical initialization errors will prevent the dashboard from starting.
        Non-critical errors are logged but don't stop application execution.
        
    !!! tip "Module Extension"
        To add new modules, initialize them after the existing portfolio module
        and pass the same data_utils, data_inputs, and reactives_shiny objects.
    """
    
    # Initialize reactive values for application state management
    # This creates the centralized state that coordinates all dashboard modules
    try:
        reactives_shiny = initialize_reactives_shiny(data_utils=data_utils)
    except Exception as exc:
        # Critical error - dashboard cannot function without reactive state
        raise DashboardInitializationError(f"Failed to initialize reactive values: {exc}") from exc
    
    # Initialize navigation tracking reactive value
    # Defaults to the first available tab for consistent user experience
    current_tab = reactive.value("QWIM Portfolios")


    @reactive.effect
    def observer_track_selected_tab():
        """
        Track and update the currently selected navigation tab.
        
        This reactive effect monitors changes to the main navigation bar
        and updates the `current_tab` reactive value accordingly.
        
        ## Functionality
        
        - Monitors navigation bar state changes
        - Updates current_tab reactive value
        - Enables tab-specific functionality and state management
        - Provides tab context for conditional logic in modules
        
        ## Implementation Details
        
        Uses `input.input_ID_navbar_main()` to get the currently selected tab
        and validates the value before updating the reactive state.
        
        ## Usage Example
        
        ```python
        # In other reactive contexts, access current tab
        active_tab = current_tab()
        if active_tab == "QWIM Portfolios":
            # Tab-specific logic
        ```
        
        ## Notes
        
        !!! info "Validation"
            Includes input validation to ensure only valid tab names
            are set in the reactive value.
            
        !!! tip "Extension"
            When adding new tabs, this function automatically tracks
            them without modification.
        """
        selected_tab = input.input_ID_navbar_main()
        # Validate that a tab was actually selected before updating
        if selected_tab:
            current_tab.set(selected_tab)


    @reactive.effect
    @reactive.event(input.input_ID_show_about)
    def observer_show_about_modal():
        """
        Display the About modal dialog when the About button is clicked.
        
        This reactive effect responds specifically to clicks on the About button
        and displays the modal containing application information.
        
        ## Event-Driven Pattern
        
        Uses `@reactive.event` decorator to respond only to specific button clicks
        rather than any input change, ensuring the modal only appears when requested.
        
        ## Modal Content
        
        Displays the pre-created `about_modal` which includes:
        - Feature overview and capabilities
        - Technology stack information
        - Version and platform details
        - Usage guidance and support information
        
        ## User Experience
        
        - Modal appears immediately upon button click
        - Can be dismissed by clicking outside or using the close button
        - Provides comprehensive application information in accessible format
        
        ## Implementation
        
        ```python
        # Button click → Event trigger → Modal display
        ui.modal_show(about_modal)
        ```
        
        ## Notes
        
        !!! info "Event Specificity"
            The @reactive.event decorator ensures this function only runs
            when the specific About button is clicked, not on other input changes.
            
        !!! tip "Modal Management"
            The modal is pre-created for performance and consistency,
            avoiding recreation on each display request.
        """
        ui.modal_show(about_modal)

    # Initialize investors module server
    investors_module_instance = tab_investors_server(
        id="ID_tab_investors",  # Unique module identifier following naming convention
        data_utils=data_utils,  # Utility functions and configuration settings
        data_inputs=data_inputs,  # Input datasets for portfolio analysis
        reactives_shiny=reactives_shiny)  # Centralized reactive state for coordination

    # Initialize portfolio analysis module server
    portfolios_module_instance = tab_portfolios_server(
        id="ID_tab_portfolios",  # Unique module identifier following naming convention
        data_utils=data_utils,  # Utility functions and configuration settings
        data_inputs=data_inputs,  # Input datasets for portfolio analysis
        reactives_shiny=reactives_shiny)  # Centralized reactive state for coordination


#: Main Shiny application instance combining UI and server functionality
#: This creates the complete application ready for deployment
app = App(app_ui, app_server)


# =============================================================================
# Application Entry Point
# =============================================================================

def main():
    """
    Main entry point for the QWIM Dashboard application.
    
    This function handles application startup with environment-specific configuration,
    providing different settings for development and production deployments.
    
    ## Environment Configuration
    
    The application supports two deployment modes:
    
    === "Development Mode (Default)"
        - **Host**: `127.0.0.1` (localhost access only)
        - **Port**: `8080`
        - **Reload**: `False` (stable operation for testing)
        - **Use Case**: Local development and testing
        
    === "Production Mode"
        - **Host**: `0.0.0.0` (external network access)
        - **Port**: `8000`
        - **Reload**: `False` (stable operation without automatic restarts)
        - **Use Case**: Production deployment and external access
    
    ## Environment Control
    
    Set the deployment mode using the `QWIM_ENVIRONMENT` environment variable:
    
    ```bash
    # Development mode (default)
    python main_App.py
    
    # Production mode
    QWIM_ENVIRONMENT=production python main_App.py
    ```
    
    ## Startup Information
    
    The function provides comprehensive startup information including:
    - Application mode and configuration
    - Python version and platform details
    - Project directory location
    - Access URLs for the dashboard
    
    ## Error Handling
    
    Implements robust error handling with:
    - Detailed error messages for debugging
    - Complete stack trace information
    - Graceful application termination on critical errors
    - System exit codes for process monitoring
    
    ## Raises
    
    SystemExit: If the application fails to start due to configuration issues,
    missing dependencies, or other critical errors.
    
    ## Startup Sequence
    
    1. **Environment Detection**: Determine deployment mode from environment variable
    2. **Information Display**: Print startup information and configuration details
    3. **Platform Validation**: Display Python and platform version information
    4. **Server Start**: Launch Shiny server with appropriate configuration
    5. **Error Handling**: Catch and report any startup failures
    
    ## Network Configuration
    
    ### Development Access
    - URL: http://127.0.0.1:8080
    - Access: Localhost only (secure for development)
    - Features: Stable operation, detailed error messages
    
    ### Production Access  
    - URL: http://0.0.0.0:8000
    - Access: External network access (configure firewall as needed)
    - Features: Optimized performance, stable operation
    
    ## Performance Considerations
    
    ### Development Mode
    - Stable operation without file monitoring
    - Detailed logging and error reporting
    
    ### Production Mode
    - No file system monitoring
    - Optimized for stability
    
    ## Example Usage
    
    ```python
    # Direct execution
    if __name__ == "__main__":
        main()
    
    # Programmatic usage
    import main_App
    main_App.main()
    ```
    
    ## Security Considerations
    
    !!! warning "Production Security"
        Production mode provides stable operation for external access.
        Ensure proper firewall configuration when using 0.0.0.0.
        
    !!! info "Development Safety"
        Development mode restricts access to localhost (127.0.0.1) for security
        during development and testing phases.
        
    ## Monitoring and Logging
    
    - Startup information is printed to console for monitoring and debugging
    - Error details are captured with full stack traces
    - Log files are created in the `logs/` directory
    - System exit codes indicate success (0) or failure (1)
    
    ## Troubleshooting
    
    Common startup issues and solutions:
    
    ??? question "Port already in use"
        Another application is using the port. Either stop the other application
        or modify the port number in the function.
        
    ??? question "Permission denied"
        Insufficient permissions to bind to the port (especially for ports < 1024).
        Use a higher port number or run with appropriate permissions.
        
    ??? question "Module import errors"
        Missing dependencies or incorrect Python path. Verify all requirements
        are installed and the project structure is correct.
    """
    try:
        # Display comprehensive startup information for monitoring and debugging
        print("🚀 Starting QWIM Dashboard...")
        print(f"📊 Environment: {ENVIRONMENT}")
        print(f"🐍 Python version: {platform.python_version()}")
        print(f"💻 Platform: {platform.system()} {platform.release()}")
        print(f"📁 Project directory: {project_dir}")
        
        # Launch application with environment-appropriate configuration
        if ENVIRONMENT == "production":
            # Production configuration optimized for stability and security
            print(f"🌐 Production mode: http://0.0.0.0:8000")
            print("⚡ Features: External access, optimized performance, stable operation")
            app.run(
                host="0.0.0.0", 
                port=8000, 
                reload=False
            )
        else:
            # Development configuration optimized for development workflow
            print(f"🔧 Development mode: http://127.0.0.1:8080")
            print("🛠️  Features: Stable operation, detailed error messages")
            app.run(
                host="127.0.0.1", 
                port=8080, 
                reload=False
            )
            
    except Exception as exc:
        # Comprehensive error handling with detailed information for troubleshooting
        print(f"❌ Failed to start QWIM Dashboard: {exc}")
        print(f"📝 Error details:\n{traceback.format_exc()}")
        print(f"💡 Check logs in: {project_dir / 'logs'}")
        print(f"🔍 Verify Python version (3.11+ required): {platform.python_version()}")
        sys.exit(1)  # Exit with error code for process monitoring


# =============================================================================
# Application Execution
# =============================================================================

# Main entry point when script is executed directly
# This enables both direct execution and programmatic usage
if __name__ == "__main__":
    main()