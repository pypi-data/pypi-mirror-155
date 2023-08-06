Quickstart
==========

Defining a basic plugin can be done using the following in ``mypackage/plugins/myplugin.py``::

   import ezplugins

   @ezplugins.ezplugin
   class MyPlugin:

      # Plugin objects are initialized on load
      def __init__(self):
         print("Plugin INIT")

      # Methods must be decorated so they can be run
      @ezplugins.ezplugin_method()
      def some_method(self, param1, param2):
         return f"{param1=}, {param2=}"


Loading the plugin and running the method can be done using::

   import ezplugins

   # Load plugins from mypackage.plugins
   plugin_manager = ezplugins.EZPluginManager()
   plugin_manager.load_package("mypackage.plugins")

   # Call the method some_func in each plugin
   for method, _ in plugin_manager.methods(with_name="some_func"):
      result = method.run("param1", "param2")
      print(f"RESULT: {result}")


Yes, there is a ``_`` (underscore) in the above, this is actually the plugin the method is from. In this case we don't need it.


Defining Plugins
================

Taking the quickstart example, plugins are defined by decorating them with :func:`ezplugins.decorators.ezplugin`::

   import ezplugins

   @ezplugins.ezplugin
   class MyPlugin:
      ...

The result of this would be the class is marked as being an EZPlugins class that is instantiated during plugin load.

Plugins are instantiated during load. Plugin methods are called using this instantiated object.

Multiple plugin classes can be defined in the same file. Sub-modules are transversed.

The only restriction relating to plugins is that the plugin package must be a valid Python package.

Internal plugin names are set to the path of the module it is loaded from within the ``PYTHONPATH`` and suffixed with
``#ClassName``, in this case it would be ``package.path#MyPlugin``. This can be used to call a specific plugin. On a side note,
to make things easier, plugins can also be called using ``#ClassName``, keep in mind though that one can have two classes with the
same name in different modules.

See :ref:`quickstart:Calling Plugins` for more info on using plugin names.


Plugin Aliases
--------------

Plugin aliases can be provided using the :func:`~ezplugins.decorators.ezplugin_metadata` decorator::


   import ezplugins

   @ezplugins.ezplugin_metadata(alias="CoolPlugins")
   class MyPlugin:
      ...


A plugin alias can be provided, which may better suite the needs of application. The alias can be anything, it may also match
another fully qualified plugin name, or class name. This plugin alias is looked up when a call to a specific plugin is made
(see :ref:`quickstart:Calling Plugins` for more info).

This poses an interesting scenario of being able to run a plugin method before another plugin method if the ordering is changed
(see :ref:`quickstart:Method Ordering`).


Defining Plugin Methods
=======================

Plugin methods must be decorated, this allows EZPlugins to know that this method can be called. The decorator used for methods are
:func:`~ezplugins.decorators.ezplugin_method`. The result of using this decorator is the method will get additional attributes set
which EZPlugins looks for when determining which methods can be run or not.

Here is an example::

   import ezplugins

   @ezplugins.ezplugin
   class MyPlugin:

      ...

      # Methods must be decorated in order to be called
      @ezplugins.ezplugin_method()
      def some_method(self, param1, param2):
         return f"{param1=}, {param2=}"


Method Ordering
---------------

Further to decorating a method as being runnable by EZPlugins, one can also specify the order which the method is run. This is done
using :func:`~ezplugins.decorators.ezplugin_method`.

The default plugin run order is ``5000``. By not setting the order, the result would be the methods being run in an undefined
random order when having the same run order.

Here is an example of how to specify the run order::

   import ezplugins

   @ezplugins.ezplugin
   class MyPlugin:

      ...

      # Methods must be decorated in order to be called
      @ezplugins.ezplugin_method(order=5050)
      def some_method(self, param1, param2):
         return f"{param1=}, {param2=}"


Plugin Manager
==============

The EZPlugins manager is responsible for both loading and returning plugin methods for execution.

Plugins are loaded from packages which are looked up within ``PYTHONPATH``.

Packages are recursed and all plugins are loaded by instantiating the classes marked as plugins. The resulting objects are used
when methods are run.


Loading Plugins
---------------

Plugins are loaded by using one of the below techniques.

Loading plugins from packages can be done as follows, these packages are recursed and all classes decorated as being EZPlugin's
are instantiated.::

   import ezplugins

   # Load plugins from mypackage.plugins and "mypackage2.plugins"
   plugin_manager = ezplugins.EZPluginManager()
   plugin_manager.load_package("mypackage.plugins")
   plugin_manager.load_package("mypackage2.plugins")

Loading plugins from modules can be done, these modules are searched in the system module list first (which includes already-loaded
modules), and falls back to attempting an import::

   import ezplugins

   # Load plugins from mypackage.plugin
   plugin_manager = ezplugins.EZPluginManager()
   plugin_manager.load_module("mypackage.plugin")

All plugin modules matching a regex can also be loaded, it is important to note that the regex must match ALL components
of the module path. Everything that matches WILL be loaded and executed. Check the below examples::

   import ezplugins

   # Load plugins from mypackage.plugin
   plugin_manager = ezplugins.EZPluginManager()
   plugin_manager.load_modules(r"^mypackage($|\.plugins($|\.))")

   # Errors during module load can be ignored using the following
   plugin_manager.load_modules(r"^mypackage2($|\.plugins($|\.))", ignore_errors=True)


Calling Plugins
---------------

Plugin methods can be called using the :meth:ezplugins.manager.EZPluginManager.methods` generator of the plugin manager.
This will return one plugin at a time in a tuple of (:class:`ezplugins.plugin_method.EZPluginMethod`,
:class:`ezplugins.plugin.EZPlugin`).

The ordering of the results will depend on :ref:`quickstart:Method Ordering`.

Taking the quickstart example, an example of running all ``some_func`` methods in all plugins can be found below::

   # Call the method some_func in each plugin
   for method, _ in plugin_manager.methods(with_name="some_func"):
      result = method.run("param1", "param2")
      print(f"RESULT: {result}")


One can also call every single method marked as an EZPlugins method in all plugins using the following::

   # Call the method some_func in each plugin
   for method, _ in plugin_manager.methods():
      result = method.run("param1", "param2")
      print(f"RESULT: {result}")


As you can see in the above examples we have a ``_`` in the ``for``, this is the EZPlugins plugin object which we didn't need::

   # Call the method some_func in each plugin
   for method, plugin in plugin_manager.methods(with_name="some_func"):
      result = method.run("param1", "param2")
      print(f"RESULT: {result} fomr {method.name}, plugin {plugin.fqn}")


By Method Name
--------------

Plugins are generally called by method name, as seen above using the ``with_name`` keyword argument.

This can be omitted but the result will be every plugin method decorated as an EZPlugins method being called.


By Method Name & Plugin Name
-----------------------------

Restricting the method being run to a specific plugin fully qualified name, class name or alias can be achieved using the below
examples...


Call the method some_func by specifying the fully qualified plugin name::

   for method, plugin in plugin_manager.methods(with_name="some_func", from_plugin="mypackage.plugins#MyPlugin"):
      result = method.run("param1", "param2")
      print(f"RESULT: {result} fomr {method.name}, plugin {plugin.fqn}")

Call the method some_func by specifying the plugin class name::

   for method, plugin in plugin_manager.methods(with_name="some_func", from_plugin="#MyPlugin"):
      result = method.run("param1", "param2")
      print(f"RESULT: {result} fomr {method.name}, plugin {plugin.fqn}")

Call the method some_func by specifying an alias::

   for method, plugin in plugin_manager.methods(with_name="some_func", from_plugin="some_alias"):
      result = method.run("param1", "param2")
      print(f"RESULT: {result} fomr {method.name}, plugin {plugin.fqn}")
