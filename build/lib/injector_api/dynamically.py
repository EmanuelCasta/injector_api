import os
import importlib.util

import json

CONFIG_FILE_NAME = "injectorConfig.json"

# Leer la configuración desde el archivo JSON
try:
    with open(CONFIG_FILE_NAME, 'r') as file:
        config_data = json.load(file)
        MODULE_APPLICATION = config_data.get("MODULE_APPLICATION", "utils")
except FileNotFoundError:
    MODULE_APPLICATION = "utils"



LOADED_MODULES_CACHE = []

def load_modules_from_subdirectories(directory, module_name="module.py", use_cache=True):
    """
    Carga dinámicamente todos los módulos con un nombre específico desde los subdirectorios de un directorio dado.
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
                raise ImportError(f"Error al importar el archivo '{module_path}'. Mensaje de error original: {str(e)}")

    # Actualizar la caché
    LOADED_MODULES_CACHE = loaded_modules

    return loaded_modules


def inject(interface_index_mapping=None):

    import inspect
    from functools import wraps

    
    if interface_index_mapping is None:
        interface_index_mapping = {}
        
 
    # Cargar módulos 'module.py' de subdirectorios
    parent_directory = os.getcwd()
    desired_directory = os.path.join(parent_directory, MODULE_APPLICATION)
    load_modules_from_subdirectories(desired_directory, use_cache=True)

    def decorator(func):
        params = inspect.signature(func).parameters
       
        @wraps(func)
        def wrapper(*args, **kwargs):
            from .dependency import container

            # Para depuración: imprime los servicios registrados

            for name, param in params.items():
                if param.annotation in container._services:
                    index = interface_index_mapping.get(param.annotation, 0)
                    # Obtiene el servicio directamente
                    service = container.get(param.annotation, index)
                    if service:
                        # Inyecta el servicio directamente en la función
                        return func(service, *args, **kwargs)

            # Si llegamos aquí, significa que no se pudo inyectar el servicio
            


        return wrapper

    return decorator



