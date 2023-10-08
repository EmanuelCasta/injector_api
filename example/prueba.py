
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from injector_api.loader import inject
from example.iinterfa import *

class ExampleServiceImpl2(IExampleService):
    @inject()
    def __init__(self,se:Se) -> None:
        pass
    
    def do_something(self):
        return "Service Implementation 2"
    