from test.test import IService,ServiceImpl
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from injector_api import container

container.register(IService,implementation= ServiceImpl,override=True)