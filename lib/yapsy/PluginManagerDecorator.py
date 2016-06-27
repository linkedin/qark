# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-


"""
Role
====

Provide an easy way to build a chain of decorators extending the
functionalities of the default plugin manager, when it comes to
activating, deactivating or looking into loaded plugins.

The ``PluginManagerDecorator`` is the base class to be inherited by
each element of the chain of decorator.

.. warning:: If you want to customise the way the plugins are detected
             and loaded, you should not try to do it by implementing a
             new ``PluginManagerDecorator``. Instead, you'll have to
             reimplement the :doc:`PluginManager` itself. And if you
             do so by enforcing the ``PluginManager`` interface, just
             giving an instance of your new manager class to the
             ``PluginManagerDecorator`` should be transparent to the
             "stantard" decorators.

API
===
"""

import os

from yapsy.IPlugin import IPlugin
from yapsy import log


class PluginManagerDecorator(object):
	"""
	Add several responsibilities to a plugin manager object in a
	more flexible way than by mere subclassing. This is indeed an
	implementation of the Decorator Design Patterns.
        
	
	There is also an additional mechanism that allows for the
	automatic creation of the object to be decorated when this object
	is an instance of PluginManager (and not an instance of its
	subclasses). This way we can keep the plugin managers creation
	simple when the user don't want to mix a lot of 'enhancements' on
	the base class.

	
	About the __init__:

	Mimics the PluginManager's __init__ method and wraps an
	instance of this class into this decorator class.
		
	  - *If the decorated_object is not specified*, then we use the
	    PluginManager class to create the 'base' manager, and to do
	    so we will use the arguments: ``categories_filter``,
	    ``directories_list``, and ``plugin_info_ext`` or their
	    default value if they are not given.
	  - *If the decorated object is given*, these last arguments are
	    simply **ignored** !

	All classes (and especially subclasses of this one) that want
	to be a decorator must accept the decorated manager as an
	object passed to the init function under the exact keyword
	``decorated_object``.
	"""
        
	def __init__(self, decorated_object=None,
				 # The following args will only be used if we need to
				 # create a default PluginManager
				 categories_filter=None, 
				 directories_list=None, 
				 plugin_info_ext="yapsy-plugin"):
		if directories_list is None:
			directories_list = [os.path.dirname(__file__)]
		if categories_filter is None:
			categories_filter = {"Default": IPlugin}
		if decorated_object is None:
			log.debug("Creating a default PluginManager instance to be decorated.")
			from yapsy.PluginManager import PluginManager
			decorated_object = PluginManager(categories_filter, 
											 directories_list,
											 plugin_info_ext)
		self._component = decorated_object

	def __getattr__(self,name):
		"""
		Decorator trick copied from:
		http://www.pasteur.fr/formation/infobio/python/ch18s06.html
		"""
# 		print "looking for %s in %s" % (name, self.__class__)
		return getattr(self._component,name)
		
	
	def collectPlugins(self):
		"""
		This function will usually be a shortcut to successively call
		``self.locatePlugins`` and then ``self.loadPlugins`` which are
		very likely to be redefined in each new decorator.

		So in order for this to keep on being a "shortcut" and not a
		real pain, I'm redefining it here.
		"""
		self.locatePlugins()
		self.loadPlugins()
