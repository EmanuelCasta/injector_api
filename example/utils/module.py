import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from injector_api import container,SINGLETON


import example
from example.iinterfa import IExampleService,Se
from example.iter import *
    
container.register_module(example)
container.register(IExampleService, ExampleServiceImpl1 ,override=True)
#container.register(IExampleService,ExampleServiceImpl2,override=True,lifecycle=SINGLETON )
container.register(Se, SeA)


