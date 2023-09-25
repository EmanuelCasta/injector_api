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

<pre><code>
pip install injector-api
</code></pre>

<h2>Usage</h2>

<h3>Configuration <code>injectorConfig.json</code></h3>

<p>
  After installation, you must configure the library to suit your project. Create a <code>injectorConfig.json</code> at the root of your project. This file should define the following variable:
</p>


<pre><code>
{
    MODULE_APPLICATION = "your_directory_name_here"
}
</code></pre>

<p>
  Replace <code>your_directory_name_here</code> with the name of the directory where your <code>module.py</code> resides.
</p>

<h3>Defining and Registering Dependencies in <code>module.py</code></h3>

<p>
  The <code>module.py</code> is a key file in the Injector API library structure. Here, you define and register the dependencies you wish to inject into your application.
</p>

<h4>Dependency Registration</h4>

<p>
  To register dependencies, you first need to import the container from the library, then use the <code>register</code> method. This method takes the interface you wish to implement and its concrete implementation as arguments.
</p>

<pre><code>
from injector_api.dependency import container

# absolute routes, DO NOT USE RELATIVE ROUTES
from aplicacion.src.interfaces import IExampleService
from aplicacion.src.interfaces import ExampleServiceImpl1
from aplicacion.src.interfaces import ExampleServiceImpl2
from aplicacion.src.interfaces import InterfaceWithoutOtherService

# Your interfaces and classes here

container.register(IExampleService, ExampleServiceImpl1, override=True)
container.register(IExampleService, ExampleServiceImpl2, override=True)
container.register(InterfaceWithoutOtherService, ImplInterface,override=True)
</code></pre>

<h4>Injecting into Functions and Methods</h4>

<p>
  Once your dependencies are registered in <code>module.py</code>, you can use the <code>@inject</code> decorator to inject these dependencies into functions or methods.
</p>

<pre><code>
from injector_api.cargaDinamica import inject

"""
  Using the decorator with () if you use only inject will throw an error, correctly use inject() in case of defining two services for an interface place {interface:0} where 0 corresponds to the first record of the injection
"""

@inject({IExampleService: 0})
def some_function(service: IExampleService):
    return service.do_something()

@inject()
def some_function_two(service: InterfaceWithoutOtherService):
    return service.do_something()
</code></pre>

<p>
  In the above example, the <code>IExampleService</code> dependency will be injected into the <code>some_function</code>, allowing you to use its methods and properties.
</p>

<h3>Location of <code>module.py</code></h3>

<p>
  Ensure that the <code>module.py</code> file is located in the directory you've specified in <code>injectorConfig.py</code>. This file will be automatically read by the library upon execution to load and manage dependencies.
</p>

<h1>Usage Guide for Injector Library in Django</h1>

<p>This guide will walk you through setting up the Injector dependency injection library in a Django project.</p>

<h2>1. Environment Setup</h2>
<p>Ensure you have Django installed and a project initialized.</p>

<h2>2. Configuring <code>injectorConfig.json</code></h2>
<p>In the root of your Django project (where <code>manage.py</code> is located), create a file named <code>injectorConfig.json</code>:</p>
<pre><code>
{
    "MODULE_APPLICATION": "myapp"
}
</code></pre>
<p>Here, <code>myapp</code> is the name of the Django application where the injector should look for the <code>module.py</code> file.</p>

<h2>3. Setting up <code>module.py</code></h2>
<p>Inside your <code>myapp</code> application, create a file named <code>module.py</code>. This file will register the dependencies.</p>
<pre><code>
from injector_api.dependency import container
# absolute routes, DO NOT USE RELATIVE ROUTES
from myapp.services import MyService

container.register(SomeInterface, MyService)
</code></pre>
<p>Make sure <code>SomeInterface</code> and <code>MyService</code> are defined in your project and import absolute routes, DO NOT USE RELATIVE ROUTES</p>

<h2>4. Using in a Django View</h2>
<p>Now, let's say you have a Django view and you want to use your injected service. You can utilize the <code>@inject</code> decorator to automatically provide the necessary service implementations to your view functions or class-based views.</p>

<h2>5. Important Notes:</h2>
<ul>
    <li>Always ensure that the <code>injectorConfig.json</code> file is placed in a secure location and cannot be accessed by unauthorized users.</li>
    <li>The <code>module.py</code> file should only contain dependency registrations. Avoid executing any business logic in this file.</li>
</ul>

<h2>Security Recommendations</h2>

<p>
  While the Injector API simplifies dependency management, there are potential security risks when using dynamic loading. We recommend the following precautions:
</p>

<ul>
  <li>Always validate dynamically loaded information or modules.</li>
  <li>Avoid loading modules from locations that can be manipulated by untrusted users.</li>
  <li>Use a secure, isolated environment for your application.</li>
  <li>Keep the library and all its dependencies up to date.</li>
</ul>

<h2>Contribute</h2>

<p>
  Contributions are welcome! Please submit pull requests or open issues on our GitHub repository.
</p>

<h2>License</h2>

<p>
  This library is licensed under the MIT License. See the <code>LICENSE</code> file for details.
</p>
