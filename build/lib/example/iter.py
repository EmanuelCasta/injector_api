class IExampleService:
    def do_something(self):
        pass

class ExampleServiceImpl1(IExampleService):
    def do_something(self):
        return "Service Implementation 1"

class ExampleServiceImpl2(IExampleService):
    def do_something(self):
        return "Service Implementation 2"
    
class Se:
     def do_something(self):
        pass
    
class SeA(Se):
    def do_something(self):
        return "Service Implementation"