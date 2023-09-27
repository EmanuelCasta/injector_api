from test.test import IService
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from injector_api import container

container.register(IService,implementation_name='TransientService',override=True)