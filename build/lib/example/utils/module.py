from injector_api import container
from injector_api import SINGLETON,SCOPED

from iter import *
    

container.register(IExampleService, implementation_name='ExampleServiceImpl1',override=True,lifecycle=SCOPED )
container.register(IExampleService, implementation_name='ExampleServiceImpl2',override=True,lifecycle=SINGLETON )
container.register(Se, SeA)


