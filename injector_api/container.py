import threading

SINGLETON = 'singleton'
TRANSIENT = 'transient'
SCOPED = 'scoped'

class ScopeManager:
    """
        Manages the current "scope" for services with a SCOPED lifecycle.
        
        Uses thread-specific local storage to keep track of the current scope.
    """
    
    def __init__(self):
        self._local_storage = threading.local()
    
    def set_current_scope(self, scope_id):
        """Sets the current scope."""
        self._local_storage.scope_id = scope_id
        
    def get_current_scope(self):
        """Fetches the current scope or None if there's no active scope."""
        return getattr(self._local_storage, 'scope_id', None)

scope_manager = ScopeManager()

class DependencyContainer:
    """
        The main container that handles the registration and retrieval of services.
    """
    def __init__(self) -> None:
        self._services = {}
        self.__instances = {}
        self.__scoped_instances = {}


    def register(self, interface, implementation=None,implementation_name=None, lifecycle=SINGLETON, override=False):
        """
            Registers an implementation for a given interface. If an implementation is already registered,
            it can be overridden with the 'override' flag.
        """
        if not implementation and not implementation_name:
            raise ValueError("Either an implementation class or an implementation name must be provided.")
        
        if implementation_name and implementation:
            raise ValueError("Specify either an implementation class or an implementation name, not both.")
        
        if isinstance(implementation, str):
            raise TypeError("The 'implementation' argument should be a class, not a string.")
    

        
        if implementation_name:
            subclasses = self._get_all_subclasses(interface)

            # Search for classes with the desired name
            matching_classes = [cls for cls in subclasses if cls.__name__ == implementation_name]
            
            # Handle ambiguity
            if len(matching_classes) > 1:
                raise ValueError(f"Ambiguity error: Found multiple classes named '{implementation_name}' for interface '{interface.__name__}'.")
            elif len(matching_classes) == 0:
                raise ValueError(f"No subclass named '{implementation_name}' found for interface '{interface.__name__}'")
            else:
                implementation = matching_classes[0]

       
        if not issubclass(implementation, interface):
            raise TypeError(f'Dependency error: {implementation} is not a subclass of {interface}')
        
        if interface.__name__ in self._services and not override:
            raise ValueError(f"Registration error: Interface {interface} already has a registered implementation.")
        
        if interface.__name__ not in self._services:
            self._services[interface.__name__] = []
        self._services[interface.__name__].append((implementation, lifecycle))
        
    def _get_all_subclasses(self, cls):
        """
        Helper method to fetch all subclasses of a given class.
        """
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in self._get_all_subclasses(c)]
        )
    
    def start_scope(self):
        """Starts a new scope."""
        scope_id = id(threading.current_thread())
        self.__scoped_instances[scope_id] = {}
        scope_manager.set_current_scope(scope_id)

    def end_scope(self):
        """Ends the current scope."""
        scope_id = scope_manager.get_current_scope()
        if scope_id in self.__scoped_instances:
            del self.__scoped_instances[scope_id]
        scope_manager.set_current_scope(None)



    def get(self, interface, index=0, *args, **kwargs):
        """
        Retrieves an instance of the service registered for the provided interface.
        The lifecycle determines how the instance is created and managed.
        """
        if interface.__name__ not in self._services:
            raise ValueError(f"Dependency error: No service registered for interface {interface}")
        
        implementation, lifecycle = self._services[interface.__name__][index]

        if lifecycle == SINGLETON:
            if (interface.__name__, index) not in self.__instances:
                self.__instances[(interface.__name__, index)] = implementation(*args, **kwargs)
            return self.__instances[(interface.__name__, index)]
        
        elif lifecycle == TRANSIENT:
            return implementation(*args, **kwargs)
        
        elif lifecycle == SCOPED:
            scope_id = scope_manager.get_current_scope()
            if scope_id is None:
                raise RuntimeError("No active scope. Ensure you call start_scope() before requesting a SCOPED service.")
            
            if scope_id not in self.__scoped_instances:
                self.__scoped_instances[scope_id] = {}
            if interface.__name__ not in self.__scoped_instances[scope_id]:
                self.__scoped_instances[scope_id][interface.__name__] = implementation(*args, **kwargs)
            return self.__scoped_instances[scope_id][interface.__name__]
    
        
        else:
            raise RuntimeError("No active scope. Ensure you call start_scope() before requesting a SCOPED service.")
    
container = DependencyContainer()