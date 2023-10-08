import sys
import os
from example.iinterfa import *
# Agrega el directorio padre al sys.path

class ExampleServiceImpl1(IExampleService):
    def do_something(self):
        return "Service Implementation 1"
    
class SeA(Se):
    def do_something(self):
        return "Service Implementation SeA"