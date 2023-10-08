class DependencyInjectionError(Exception):
    """Base exception for all errors in your dependency injection library."""
    pass

class ConfigurationError(DependencyInjectionError):
    """Raised when there's an error in configuration."""
    pass

class RegistrationError(DependencyInjectionError):
    """Raised when there's an error in service registration."""
    pass
