from setuptools import setup, find_packages

setup(
    name='injector_api',
    version='0.0.21',
    packages=find_packages(),
    author='Emanuel Castañeda',
    packages=find_packages(exclude=["tests*","utils*"]),
    include_package_data=True, 
    author_email='emanuel.castaneda.cardona@gmail.com',
    description='Python dependency injection library for your projects or for dependency injection in Django!!',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/EmanuelCasta/injector_api',
)