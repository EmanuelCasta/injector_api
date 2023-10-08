import threading
from .dependencyError import *
import pkgutil
import importlib
import os
import sys

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
        self.__module =None


    def register_module(self,module)->None:
        self.__module = module

    def is_valid_class_or_tuple(self,item):
        """Verifica si el item es una clase o una tupla de clases."""
        if isinstance(item, type):
            return True
        if isinstance(item, tuple) and all(isinstance(i, type) for i in item):
            return True
        return False
    
    def module_contains_interface(self,module_path, interface_name):
        """Verifica si un módulo contiene una referencia al nombre de la interfaz sin importarlo."""
        with open(module_path, 'r') as f:
            content = f.read()
            return interface_name in content

    def find_classes_in_package_recursive(self,package, interface):
        matches_set = set()
        imported_modules = set()
        class_lengths = {}


        # Verificar que el argumento 'interface' es válido
        if not self.is_valid_class_or_tuple(interface):
            raise ValueError("The provided interface must be a class or a tuple of classes")
        
        def _find_classes_in_module(module, interface):
            for attr_name in dir(module):
                attr_value = getattr(module, attr_name)
                
                if self.is_valid_class_or_tuple(attr_value) and issubclass(attr_value, interface) and attr_value != interface:
                    class_key = attr_value.__name__  # Usamos solo el nombre de la clase como clave
                    
                    # Si la clase aún no está en nuestro diccionario de longitudes
                    if class_key not in class_lengths:
                        class_lengths[class_key] = (len(f"{attr_value.__module__}.{attr_value.__name__}"), attr_value)
                        matches_set.add(attr_value)
                    
                    else:
                        # Si la clase está en el diccionario, comparamos las longitudes y verificamos si son la misma clase
                        current_length, current_class = class_lengths[class_key]
                        
                        if len(f"{attr_value.__module__}.{attr_value.__name__}") > current_length:
                            # Si la nueva clase tiene una ruta más larga y es la misma clase, la reemplazamos
                            if current_class == attr_value:
                                matches_set.remove(current_class)
                                matches_set.add(attr_value)
                                class_lengths[class_key] = (len(f"{attr_value.__module__}.{attr_value.__name__}"), attr_value)
                            
                            # Si las clases no son las mismas, las tratamos como diferentes y las agregamos ambas
                            elif current_class != attr_value:
                                matches_set.add(attr_value)
        
        def _recursive_search(package, interface):
            for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):
                full_name = package.__name__ + '.' + module_name
                if full_name in imported_modules:
                    continue

                imported_modules.add(full_name)
                module_path = os.path.join(package.__path__[0], module_name + '.py')
                if is_pkg:
                    _recursive_search(importlib.import_module(full_name), interface)
                elif self.module_contains_interface(module_path, interface.__name__ if isinstance(interface, type) else interface[0].__name__):
                    current_script_name = sys.argv[0].replace("/", ".").replace("\\", ".").rstrip(".py")
                    
                    if full_name != current_script_name and full_name != package.__name__ + '.'+current_script_name:
                        module = importlib.import_module(full_name)
                        _find_classes_in_module(module, interface)
            

        _recursive_search(package, interface)
        return list(matches_set)


    def register(self,interface, implementation=None,implementation_name=None, lifecycle=SINGLETON, override=False):
        """
            Registers an implementation for a given interface. If an implementation is already registered,
            it can be overridden with the 'override' flag.
        """
        if not implementation and not implementation_name:
            raise RegistrationError("Either an implementation class or an implementation name must be provided.")
        
        if implementation_name and implementation:
            raise RegistrationError("Specify either an implementation class or an implementation name, not both.")
        
        if isinstance(implementation, str):
            raise ConfigurationError("The 'implementation' argument should be a class, not a string.")
    
        
        
        if implementation_name:
            if  self.__module is None:
                raise ConfigurationError(f"No register module for apps")
            
            
        # Aquí intentamos encontrar las clases usando la función
            matches = self.find_classes_in_package_recursive(self.__module, interface)
            if not matches:
                raise ConfigurationError(f"No class named '{implementation_name}' found.")
            elif len(matches) > 1 and not override:
                
                # Aquí puedes decidir qué hacer si hay múltiples coincidencias. Por ejemplo:
                raise ConfigurationError(f"Multiple classes named '{implementation_name,matches}' found. Please specify module.")
            else:
                if len(matches) > 1:
                    found_exact_match = False
                    for match in matches:
                        class_key = f"{match.__module__}.{match.__name__}"
                        class_key = class_key.split('.')[-1]
                        if class_key == implementation_name:
                            implementation = match
                            found_exact_match = True
                            break
                    if not found_exact_match:
                        raise ConfigurationError(f"Multiple matches found for '{implementation_name}', but no exact match for provided implementation name. Please specify a unique class name or check your imports.")
                else:
                    implementation = matches[0]
                
        

        if not issubclass(implementation, interface):
            raise ConfigurationError(f'Dependency error: {implementation} is not a subclass of {interface}')
        
        if interface.__name__ in self._services and not override:
            raise RegistrationError(f"Registration error: Interface {interface} already has a registered implementation.")
        if interface.__name__ not in self._services:
            self._services[interface.__name__] = []
        self._services[interface.__name__].append((implementation, lifecycle))
        
    
    
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
            raise ConfigurationError(f"Dependency error: No service registered for interface {interface}")
        
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