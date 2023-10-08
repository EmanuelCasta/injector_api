import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Agrega el directorio padre al sys.path
from injector_api import inject

#from iter import *
"""
from example.iinterfa import IExampleService,Se
#initializate("utils")
# Ahora, para inyectar la primera implementación en una función:
@inject({IExampleService: 1})
def my_function(service: IExampleService):
    return service.do_something()

# O para inyectar la segunda implementación:
@inject()
def another_function(service: IExampleService):
    return service.do_something()

# Si no especificas cuál implementación quieres, se inyectará la primera por defecto:
@inject()
def default_function(service:Se ):
    result = service.do_something()
    return result


@inject({IExampleService: 0})  # Solicitamos la segunda implementación (EveningMessageService) que es SCOPED
def handle_web_request(service: IExampleService):
    # Simulación de lógica de procesamiento
    message = service.do_something()
    print(message)

def simulate_web_request():
    # Iniciar un nuevo scope al comienzo de la solicitud
    container.start_scope()

    # Manejar la solicitud
    handle_web_request()

    # Finalizar el scope al final de la solicitud
    container.end_scope()

simulate_web_request()  # Esto imprimirá "Good evening!"

print(default_function())
print(my_function())
"""
