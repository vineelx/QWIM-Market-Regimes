
class SilentInitializationException(Exception):
    """Custom exception class for silently handling expected initialization errors.
    
    This exception is used to signal expected errors during initialization of
    reactive components, where displaying an error message would be inappropriate.
    """
    pass

class DashboardInitializationError(Exception):
    """Exception raised when dashboard initialization fails."""
    pass

class DataLoadingError(Exception):
    """Exception raised when data loading fails."""
    pass

class ModuleInitializationError(Exception):
    """Exception raised when module initialization fails."""
    pass

def is_silent_exception(exception):
    """Check if an exception should be handled silently during initialization."""
    return isinstance(exception, (SilentInitializationException, AttributeError))