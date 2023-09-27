import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from injector_api import DependencyContainer, load_modules_from_subdirectories, inject,TRANSIENT,SCOPED

# Interfaces y clases de ejemplo para las pruebas
class IService:
    def get_data(self):
        pass

class ServiceImpl(IService):
    def get_data(self):
        return "data"

class TransientService(IService):
    def get_data(self):
        return "transient data"

class ScopedService(IService):
    def get_data(self):
        return "scoped data"
    



class DependencyTests(unittest.TestCase):
    def setUp(self):
        self.container = DependencyContainer()

    def test_register_and_get_singleton(self):
        self.container.register(IService, ServiceImpl)
        service = self.container.get(IService)
        self.assertIsInstance(service, ServiceImpl)

    def test_register_and_get_transient(self):
        self.container.register(IService, TransientService, lifecycle=TRANSIENT)
        service1 = self.container.get(IService)
        service2 = self.container.get(IService)
        self.assertNotEqual(service1, service2)

    def test_register_and_get_scoped(self):
        self.container.register(IService, ScopedService, lifecycle=SCOPED)
        self.container.start_scope()
        service1 = self.container.get(IService)
        service2 = self.container.get(IService)
        self.assertEqual(service1, service2)
        self.container.end_scope()

    def test_dynamic_loading(self):
        modules = load_modules_from_subdirectories("searchModule")
        self.assertGreater(len(modules), 0)

    def test_injection_ServiceImpl(self):

        @inject()
        def function_with_dependency(service: IService):
            return service.get_data()

        result = function_with_dependency()
        self.assertEqual(result, "data")
        
    def test_injection_TransientService(self):

        @inject({IService:1})
        def function_with_dependency(service: IService):
            return service.get_data()

        result = function_with_dependency()
        self.assertEqual(result, "transient data")

if __name__ == "__main__":
    unittest.main()
