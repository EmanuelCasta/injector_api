class DependencyContainer:

    def __init__(self) -> None:
        self._services = {}
        self.__instances = {}

    def register(self, interface, implementation, override=False):
        # Comprobar si la implementación es una subclase de la interfaz
        if not issubclass(implementation, interface):
            raise TypeError(f'[Error de dependencia] {implementation} no es una subclase de {interface}')
        
        # Evitar sobrescribir servicios sin intención
        if interface in self._services and not override:
            raise ValueError(f"[Error de registro] La interfaz {interface} ya tiene una implementación registrada.")
        
        # Registrar la implementación
        if interface not in self._services:
            self._services[interface] = []
        self._services[interface].append(implementation)

    def get(self, interface, index=0, *args, **kwargs):
        if interface not in self._services:
            raise ValueError(f"[Error no existe dependencia] No se ha registrado ningún servicio para la interfaz {interface}")
        
        # Si no hay una instancia existente, crear una
        if (interface, index) not in self.__instances:
            self.__instances[(interface, index)] = self._services[interface][index](*args, **kwargs)
        return self.__instances[(interface, index)]
    
    
container = DependencyContainer()