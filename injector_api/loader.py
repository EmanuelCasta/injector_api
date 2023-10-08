import os
import importlib.util
import json
import logging

logger = logging.getLogger(__name__)


DEFAULT_CONFIG = {
    "MODULE_APPLICATION": "apps"
}

CONFIG_FILE_NAME = "injectorConfig.json"
USE_CONFIGURE = False
LOADED_MODULES_CACHE = []
MODULE_APPLICATION = None

def load_config_from_file():
    global MODULE_APPLICATION
    if MODULE_APPLICATION is None:
        try:
            with open(CONFIG_FILE_NAME, 'r') as file:
                config_data = json.load(file)
                MODULE_APPLICATION = config_data.get("MODULE_APPLICATION", DEFAULT_CONFIG["MODULE_APPLICATION"])
        except FileNotFoundError:
            MODULE_APPLICATION = DEFAULT_CONFIG["MODULE_APPLICATION"]
            logger.warning(f"Warning: {CONFIG_FILE_NAME} not found. Using default configuration.")
        except json.JSONDecodeError:
            MODULE_APPLICATION = DEFAULT_CONFIG["MODULE_APPLICATION"]
            logger.warning(f"Warning: {CONFIG_FILE_NAME} is not well-formed. Using default configuration.")

def configure(module_application):
    global MODULE_APPLICATION
    global USE_CONFIGURE 
    USE_CONFIGURE = True
    MODULE_APPLICATION = module_application

def get_module_application():
    global MODULE_APPLICATION
    if MODULE_APPLICATION is None and not USE_CONFIGURE:
        load_config_from_file()
    return MODULE_APPLICATION

def load_modules_from_subdirectories(directory, module_name="module.py", use_cache=True):
    """
    Dynamically loads all modules with a specific name from the subdirectories of a given directory.
    """
    global LOADED_MODULES_CACHE

    if use_cache and LOADED_MODULES_CACHE:
        return LOADED_MODULES_CACHE

    loaded_modules = []

    for root, dirs, files in os.walk(directory):
        if module_name in files:
            module_path = os.path.join(root, module_name)
            try:
                # Cargar el módulo dinámicamente
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                loaded_modules.append(module)
            except Exception as e:
                raise ImportError(f"Error importing file '{module_path}'. Original error message: {str(e)}")

    LOADED_MODULES_CACHE = loaded_modules


def initializate(application):
    configure(module_application=application)
    desired_directory = os.path.join(parent_directory, get_module_application())
    load_modules_from_subdirectories(desired_directory, use_cache=True)

parent_directory = os.getcwd() 

def start():
    desired_directory = os.path.join(parent_directory, get_module_application())
    load_modules_from_subdirectories(desired_directory, use_cache=True)

def inject(interface_index_mapping=None):
    """
    A decorator that handles dependency injection for functions and class methods based on their type hints.
    """
    
    import inspect
    from functools import wraps
    
    if interface_index_mapping is None:
        interface_index_mapping = {}
    
    
        
  
    def decorator(func):
        
        params = inspect.signature(func).parameters
        param_names = list(params.keys())
        @wraps(func)
        def wrapper(*args, **kwargs):
            from .container import container
            
            # Determine if this is a class method by checking if the first argument is an instance of a class
            is_class_method = len(args) > 0 and isinstance(args[0], type(args[0]))

            args_list = list(args)

            for name, param in params.items():
                if param.annotation.__name__ in container._services:

                    index = interface_index_mapping.get(param.annotation, 0)
                    service = container.get(param.annotation, index)
                    
                    if service:
                        arg_position = param_names.index(name)
                        # Adjust for 'self' if this is a class method
                        if is_class_method:
                            arg_position += 1

                        if arg_position < len(args_list):
                            args_list[arg_position] = service
                        else:
                            kwargs[name] = service

            return func(*args_list, **kwargs)

        return wrapper

    return decorator
