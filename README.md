<h1>Injector API</h1>
<p>
  The Injector API is a lightweight dependency injection library designed to simplify the management of dependencies in Python projects.
</p>
<h2>Prerequisites</h2>
<ul>
  <li>Python 3.7 or higher</li>
  <li>A proper environment (virtualenv or conda recommended)</li>
</ul>
<h2>Installation</h2>
<p>
  To install the Injector API, simply run the following pip command:
</p>
<pre><code>pip install injector-api</code></pre>
<h2>Usage</h2>
<h3>Initial Configuration</h3>
<p>
  First, call <code>configure</code> in your main file app configuration to set up the Injector API:
</p>
<pre><code>
import injector_api

injector_api.initializate("your_directory_name_here")
</code></pre>
<h4>Note on Directory Structure:</h4>
<p>
  If you specify "your_directory_name_here" (or any other directory name) as the directory for the Injector API to search, make sure that your main execution file is located in the same parent directory as "your_directory_name_here".
</p>
<p>or</p>
<h3>Configuration <code>injectorConfig.json</code></h3>
<p>
  Instead of directly using the <code>initializate</code> method, you can also configure the library by creating an <code>injectorConfig.json</code> at the root of your project. This file should specify the directory name:
</p>
<pre><code>
{
    "MODULE_APPLICATION": "your_directory_name_here"
}
</code></pre>
<p>
  Replace <code>your_directory_name_here</code> with the name of the directory where your <code>module.py</code> resides.
</p>
<h3>Defining and Registering Dependencies in <code>module.py</code></h3>
<p>
  The <code>module.py</code> file plays a pivotal role in the Injector API library structure. Here, you define and register the dependencies you wish to inject into your application.
</p>
<h4>Dependency Registration</h4>
<p>
  To register dependencies, first import the container from the library. Then, use the <code>register</code> method. This method takes the interface you wish to implement and its concrete implementation as arguments.
</p>
<pre><code>
from injector_api.container import container
# absolute routes, DO NOT USE RELATIVE ROUTES
from application.src.interfaces import IExampleService,InterfaceWithoutOtherService
import application

# Your interfaces and classes here

container.register_module(application)
container.register(IExampleService, implementation_name='ExampleServiceImpl1' ,override=True)
container.register(IExampleService,implementation_name='ExampleServiceImpl2',override=True,lifecycle=SINGLETON )
container.register(InterfaceWithoutOtherService, implementation_name='WithoutOtherService')

</code></pre>
<h5>or</h5>

<pre><code>
# absolute routes, DO NOT USE RELATIVE ROUTES
from application.src.interfaces import IExampleService,InterfaceWithoutOtherService
from application.src.class import ExampleServiceImpl1,ExampleServiceImpl2,WithoutOtherService
import application


container.register_module(application)
container.register(IExampleService, ExampleServiceImpl1 ,override=True)
container.register(IExampleService,ExampleServiceImpl2,override=True,lifecycle=SINGLETON )
container.register(InterfaceWithoutOtherService, WithoutOtherService)
</code></pre>
<h4>Override Explanation</h4>
<p>
  The <code>override</code> parameter is optional and its default value is <code>False</code>. If set to <code>True</code>, it allows a new registration to replace an existing one for the specified interface. This is useful when you want to change the implementation for an interface without removing the previous registration manually.
</p>
<h4>Injecting into Functions and Methods</h4>
<p>
  With dependencies registered in <code>module.py</code>, you can utilize the <code>@inject</code> decorator to inject these dependencies into functions or methods.
</p>
<pre><code>
from injector_api.dynamically import inject

"""
  Use @inject() only when specifying the type of implementation. For correct usage, employ @inject() with the format {interface:0}, where 0 corresponds to the first registered injection. Without specifying the type of implementation, simply use @inject
"""

@inject({IExampleService: 0})
def some_function(service: IExampleService):
  return service.do_something()

@inject
def some_function_two(service: InterfaceWithoutOtherService):
  return service.do_something()
</code></pre>
<p>
  In the example above, the <code>IExampleService</code> dependency will be injected into <code>some_function</code>, granting access to its methods and properties.
</p>
<h3>Location of <code>module.py</code></h3>
<p>
  Ensure the <code>module.py</code> file is located in the directory you've specified in <code>injectorConfig.json</code>. This file will be automatically read by the library during execution to load and manage dependencies.
</p>
<h3>Usage with Django</h3>
<p>
  In Django, call <code>configure</code> in your app configuration:
</p>

# application/apps.py

<pre><code>
from django.apps import AppConfig
import injector_api

class ApplicationConfig(AppConfig):
    name = 'application'  # Ensure to use the correct name of your app here

    def ready(self):
        """
          It should be intuited that the new_src must be in the same apps.py directory, with new_src being a dywan
        """
        injector_api.initializate("application") 
</code></pre>
<p>Optinal</p>
# application/__init__.py

default_app_config = 'application.apps.ApplicationConfig'



<p>Use the common library as if it were your own project</p>

<p>If you're integrating the Injector API within a Django project, you have the option to use the <code>ScopeMiddleware</code> to manage scoped dependencies. This middleware ensures that dependencies with a "scoped" lifecycle are correctly managed within the context of a web request.</p>

<p>However, do note that using scoped dependencies requires your Django application to run in a server mode where each request is handled by a separate thread or process (e.g., using gunicorn with threaded workers). Using scoped dependencies in a single-threaded server (like Django's default development server) might lead to unexpected behaviors.</p>

<p>To use the middleware, add it to your Django project's middleware list:</p>

<pre><code>
MIDDLEWARE = [
    ...
    'path_to_your_library.ScopeMiddleware',
    ...
]
</code></pre>

<h2>Security Recommendations</h2>

<p>
  While the Injector API simplifies dependency management, there are potential security risks when using dynamic loading. We recommend the following precautions:
</p>

<ul>
  <li>Always validate dynamically loaded information or modules.</li>
  <li>Avoid loading modules from locations that can be manipulated by untrusted users.</li>
  <li>Use a secure, isolated environment for your application.</li>
  <li>Keep the library and all its dependencies up to date.</li>
  <li>If you're using the optional <code>ScopeMiddleware</code> in Django, ensure your server is configured correctly for scoped dependencies.</li>
</ul>

<h2>Contribute</h2>

<p>
  Contributions are welcome! Please submit pull requests or open issues on our GitHub repository.
</p>
<h2>License</h2>
<p>
  This library is licensed under the MIT License. See the <code>LICENSE</code> file for details.
</p>