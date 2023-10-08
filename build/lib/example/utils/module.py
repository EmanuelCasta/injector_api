from injector_api import container
from injector_api import SINGLETON,SCOPED
import example
from iter import *
    
container.register_module(example)
container.register(IExampleService, implementation_name='ExampleServiceImpl1',override=True,lifecycle=SCOPED )
#container.register(IExampleService,implementation_name='ExampleServiceImpl2',override=True,lifecycle=SINGLETON )
#container.register(Se, implementation_name='SeA')


