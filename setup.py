from setuptools import setup, find_packages

setup(
    name='injector_api',
    version='0.0.21',
    packages=find_packages(),
    author='Emanuel Castañeda',
    author_email='emanuel.castaneda.cardona@gmail.com',
    description='python dependency injection library, BETA',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/EmanuelCasta/injector_api',
)