from .container import DependencyContainer, SINGLETON, TRANSIENT, SCOPED, container
from .loader import inject, load_modules_from_subdirectories,initializate
from .scopeMiddlware import ScopeMiddleware

__version__ = '0.5.0'