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

<h3>Configuring <code>injectorConfig.py</code></h3>

<p>
  After installation, you must configure the library to suit your project. Create a <code>injectorConfig.py</code> at the root of your project. This file should define the following variable:
</p>

<pre><code>
MODULE_APPLICATION = "your_directory_name_here"
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
