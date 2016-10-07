# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

"""
Role
====

The ``PluginManager`` loads plugins that enforce the `Plugin
Description Policy`_, and offers the most simple methods to activate
and deactivate the plugins once they are loaded.

.. note:: It may also classify the plugins in various categories, but
          this behaviour is optional and if not specified elseway all
          plugins are stored in the same default category.

.. note:: It is often more useful to have the plugin manager behave
          like singleton, this functionality is provided by
          ``PluginManagerSingleton``


Plugin Description Policy
=========================

When creating a ``PluginManager`` instance, one should provide it with
a list of directories where plugins may be found. In each directory,
a plugin should contain the following elements:

For a  *Standard* plugin:

  ``myplugin.yapsy-plugin`` 
 
      A *plugin info file* identical to the one previously described.
 
  ``myplugin``
 
      A directory ontaining an actual Python plugin (ie with a
      ``__init__.py`` file that makes it importable). The upper
      namespace of the plugin should present a class inheriting the
      ``IPlugin`` interface (the same remarks apply here as in the
      previous case).


For a *Single file* plugin:

  ``myplugin.yapsy-plugin`` 
       
      A *plugin info file* which is identified thanks to its extension,
      see the `Plugin Info File Format`_ to see what should be in this
      file.
   
      The extension is customisable at the ``PluginManager``'s
      instanciation, since one may usually prefer the extension to bear
      the application name.
  
  ``myplugin.py``
  
      The source of the plugin. This file should at least define a class
      inheriting the ``IPlugin`` interface. This class will be
      instanciated at plugin loading and it will be notified the
      activation/deactivation events.


Plugin Info File Format
-----------------------

The plugin info file is a text file *encoded in ASCII or UTF-8* and
gathering, as its name suggests, some basic information about the
plugin.

- it gives crucial information needed to be able to load the plugin

- it provides some documentation like information like the plugin
  author's name and a short description fo the plugin functionality.

Here is an example of what such a file should contain::

      [Core]
      Name = My plugin Name
      Module = the_name_of_the_pluginto_load_with_no_py_ending
         
      [Documentation]
      Description = What my plugin broadly does
      Author = My very own name
      Version = the_version_number_of_the_plugin
      Website = My very own website
      
      
 
.. note:: From such plugin descriptions, the ``PluginManager`` will
          built its own representations of the plugins as instances of
          the :doc:`PluginInfo` class.

Changing the default behaviour
==============================

The default behaviour for locating and loading plugins can be changed
using the various options exposed on the interface via getters.

The plugin detection, in particular, can be fully customized by
settting a custom plugin locator. See ``IPluginLocator`` for more
details on this.


Extensibility
=============

Several mechanisms have been put up to help extending the basic
functionalities of the proivided classes.

A few *hints* to help you extend those classes:

If the new functionalities do not overlap the ones already
implemented, then they should be implemented as a Decorator class of the
base plugin. This should be done by inheriting the
``PluginManagerDecorator``.

If this previous way is not possible, then the functionalities should
be added as a subclass of ``PluginManager``.

.. note:: The first method is highly prefered since it makes it
          possible to have a more flexible design where one can pick
          several functionalities and litterally *add* them to get an
          object corresponding to one's precise needs.

API
===
 
"""

import sys
import os
import imp

from yapsy import log
from yapsy import NormalizePluginNameForModuleName

from yapsy.IPlugin import IPlugin
from yapsy.IPluginLocator import IPluginLocator
# The follozing two imports are used to implement the default behaviour
from yapsy.PluginFileLocator import PluginFileAnalyzerWithInfoFile
from yapsy.PluginFileLocator import PluginFileLocator
# imported for backward compatibility (this variable was defined here
# before 1.10)
from yapsy import PLUGIN_NAME_FORBIDEN_STRING
# imported for backward compatibility (this PluginInfo was imported
# here before 1.10)
from yapsy.PluginInfo import PluginInfo


class PluginManager(object):
	"""
	Manage several plugins by ordering them in categories.
	
	The mechanism for searching and loading the plugins is already
	implemented in this class so that it can be used directly (hence
	it can be considered as a bit more than a mere interface)
	
	The file describing a plugin must be written in the syntax
	compatible with Python's ConfigParser module as in the
	`Plugin Info File Format`_

	About the __init__:

	Initialize the mapping of the categories and set the list of
	directories where plugins may be. This can also be set by
	direct call the methods: 
		
	- ``setCategoriesFilter`` for ``categories_filter``
	- ``setPluginPlaces`` for ``directories_list``
	- ``setPluginInfoExtension`` for ``plugin_info_ext``

	You may look at these function's documentation for the meaning
	of each corresponding arguments.
	"""

	def __init__(self,
				 categories_filter=None,
				 directories_list=None,
				 plugin_info_ext=None,
				 plugin_locator=None):
		# as a good practice we don't use mutable objects as default
		# values (these objects would become like static variables)
		# for function/method arguments, but rather use None.
		if categories_filter is None:
			categories_filter = {"Default":IPlugin}
		self.setCategoriesFilter(categories_filter)
		plugin_locator = self._locatorDecide(plugin_info_ext, plugin_locator)
		# plugin_locator could be either a dict defining strategies, or directly
		# an IPluginLocator object
		self.setPluginLocator(plugin_locator, directories_list)

	def _locatorDecide(self, plugin_info_ext, plugin_locator):
		"""
		For backward compatibility, we kept the *plugin_info_ext* argument.
		Thus we may use it if provided. Returns the (possibly modified)
		*plugin_locator*.
		"""
		specific_info_ext = plugin_info_ext is not None
		specific_locator = plugin_locator is not None
		if not specific_info_ext and not specific_locator:
			# use the default behavior
			res = PluginFileLocator()
		elif not specific_info_ext and specific_locator:
			# plugin_info_ext not used
			res = plugin_locator
		elif not specific_locator and specific_info_ext:
			# plugin_locator not used, and plugin_info_ext provided
			# -> compatibility mode
			res = PluginFileLocator()
			res.setAnalyzers([PluginFileAnalyzerWithInfoFile("info_ext",plugin_info_ext)])
		elif specific_info_ext and specific_locator:
			# both provided... issue a warning that tells "plugin_info_ext"
			# will be ignored
			msg = ("Two incompatible arguments (%s) provided:",
				   "'plugin_info_ext' and 'plugin_locator'). Ignoring",
				   "'plugin_info_ext'.")
			raise ValueError(" ".join(msg) % self.__class__.__name__)
		return res
	
	def setCategoriesFilter(self, categories_filter):
		"""
		Set the categories of plugins to be looked for as well as the
		way to recognise them.
		
		The ``categories_filter`` first defines the various categories
		in which the plugins will be stored via its keys and it also
		defines the interface tha has to be inherited by the actual
		plugin class belonging to each category.
		"""
		self.categories_interfaces = categories_filter.copy()
		# prepare the mapping from categories to plugin lists
		self.category_mapping = {}
		# also maps the plugin info files (useful to avoid loading
		# twice the same plugin...)
		self._category_file_mapping = {}
		for categ in categories_filter:
			self.category_mapping[categ] = []
			self._category_file_mapping[categ] = []
			

	def setPluginPlaces(self, directories_list):
		"""
		DEPRECATED(>1.9): directly configure the IPluginLocator instance instead !
		
		Convenience method (actually call the IPluginLocator method)
		"""
		self.getPluginLocator().setPluginPlaces(directories_list)

	def updatePluginPlaces(self, directories_list):
		"""
		DEPRECATED(>1.9): directly configure the IPluginLocator instance instead !

		Convenience method (actually call the IPluginLocator method)
		"""
		self.getPluginLocator().updatePluginPlaces(directories_list)

	def setPluginInfoExtension(self, ext):
		"""
		DEPRECATED(>1.9): for backward compatibility. Directly configure the
		IPluginLocator instance instead !
		
		.. warning:: This will only work if the strategy "info_ext" is
		             active for locating plugins.
		"""
		try:
			self.getPluginLocator().setPluginInfoExtension(ext)
		except KeyError:
			log.error("Current plugin locator doesn't support setting the plugin info extension.")

	def setPluginInfoClass(self, picls, strategies=None):
		"""
		DEPRECATED(>1.9): directly configure the IPluginLocator instance instead !
		
		Convenience method (actually call self.getPluginLocator().setPluginInfoClass)
		
		When using a ``PluginFileLocator`` you may restrict the
		strategies to which the change of PluginInfo class will occur
		by just giving the list of strategy names in the argument
		"strategies"
		"""
		if strategies:
			for name in strategies:
				self.getPluginLocator().setPluginInfoClass(picls, name)
		else:
			self.getPluginLocator().setPluginInfoClass(picls)

	def getPluginInfoClass(self):
		"""
		DEPRECATED(>1.9): directly control that with the IPluginLocator
		instance instead !
		
		Get the class that holds PluginInfo.
		"""
		return self.getPluginLocator().getPluginInfoClass()

	def setPluginLocator(self, plugin_locator, dir_list=None, picls=None):
		"""
		Sets the strategy used to locate the basic information.

		See ``IPluginLocator`` for the policy that plugin_locator must enforce.
		"""
		if isinstance(plugin_locator, IPluginLocator):
			self._plugin_locator = plugin_locator
			if dir_list is not None:
				self._plugin_locator.updatePluginPlaces(dir_list)
			if picls is not None:
				self.setPluginInfoClass(picls)
		else:
			raise TypeError("Unexpected format for plugin_locator ('%s' is not an instance of IPluginLocator)" % plugin_locator)
		
	def getPluginLocator(self):
		"""
		Grant direct access to the plugin locator.
		"""
		return self._plugin_locator
	
	def _gatherCorePluginInfo(self, directory, plugin_info_filename):
		"""
		DEPRECATED(>1.9): please use a specific plugin
		locator if you need such information.

		Gather the core information (name, and module to be loaded)
		about a plugin described by it's info file (found at
		'directory/filename').
		
		Return an instance of ``PluginInfo`` and the
		config_parser used to gather the core data *in a tuple*, if the
		required info could be localised, else return ``(None,None)``.

		.. note:: This is supposed to be used internally by subclasses
		and decorators.

		"""
		return self.getPluginLocator().gatherCorePluginInfo(directory,plugin_info_filename)

	def _getPluginNameAndModuleFromStream(self,infoFileObject,candidate_infofile="<buffered info>"):
		"""
		DEPRECATED(>1.9): please use a specific plugin
		locator if you need such information.
		
		Extract the name and module of a plugin from the
		content of the info file that describes it and which
		is stored in infoFileObject.
		
		.. note:: Prefer using ``_gatherCorePluginInfo``
		instead, whenever possible...
		
		.. warning:: ``infoFileObject`` must be a file-like
		object: either an opened file for instance or a string
		buffer wrapped in a StringIO instance as another
		example.

		.. note:: ``candidate_infofile`` must be provided
		whenever possible to get better error messages.
			
		Return a 3-uple with the name of the plugin, its
		module and the config_parser used to gather the core
		data *in a tuple*, if the required info could be
		localised, else return ``(None,None,None)``.

		.. note:: This is supposed to be used internally by subclasses
		and decorators.
		"""
		return self.getPluginLocator().getPluginNameAndModuleFromStream(infoFileObject, candidate_infofile)
	
	
	def getCategories(self):
		"""
		Return the list of all categories.
		"""
		return list(self.category_mapping.keys())

	def removePluginFromCategory(self, plugin,category_name):
		"""
		Remove a plugin from the category where it's assumed to belong.
		"""
		self.category_mapping[category_name].remove(plugin)


	def appendPluginToCategory(self, plugin, category_name):
		"""
		Append a new plugin to the given category.
		"""
		self.category_mapping[category_name].append(plugin)

	def getPluginsOfCategory(self, category_name):
		"""
		Return the list of all plugins belonging to a category.
		"""
		return self.category_mapping[category_name][:]

	def getAllPlugins(self):
		"""
		Return the list of all plugins (belonging to all categories).
		"""
		allPlugins = set()
		for pluginsOfOneCategory in self.category_mapping.values():
				allPlugins.update(pluginsOfOneCategory)
		return list(allPlugins)

	def getPluginCandidates(self):
		"""
		Return the list of possible plugins.

		Each possible plugin (ie a candidate) is described by a 3-uple:
		(info file path, python file path, plugin info instance)

		.. warning: locatePlugins must be called before !
		"""
		if not hasattr(self, '_candidates'):
			raise RuntimeError("locatePlugins must be called before getPluginCandidates")
		return self._candidates[:]

	def removePluginCandidate(self,candidateTuple):
		"""
		Remove a given candidate from the list of plugins that should be loaded.

		The candidate must be represented by the same tuple described
		in ``getPluginCandidates``.

		.. warning: locatePlugins must be called before !
		"""
		if not hasattr(self, '_candidates'):
			raise ValueError("locatePlugins must be called before removePluginCandidate")
		self._candidates.remove(candidateTuple)

	def appendPluginCandidate(self, candidateTuple):
		"""
		Append a new candidate to the list of plugins that should be loaded.

		The candidate must be represented by the same tuple described
		in ``getPluginCandidates``.

		.. warning: locatePlugins must be called before !
		"""
		if not hasattr(self, '_candidates'):
			raise ValueError("locatePlugins must be called before removePluginCandidate")
		self._candidates.append(candidateTuple)

	def locatePlugins(self):
		"""
		Convenience method (actually call the IPluginLocator method)
		"""
		self._candidates, npc = self.getPluginLocator().locatePlugins()
	
	def loadPlugins(self, callback=None):
		"""
		Load the candidate plugins that have been identified through a
		previous call to locatePlugins.  For each plugin candidate
		look for its category, load it and store it in the appropriate
		slot of the ``category_mapping``.

		If a callback function is specified, call it before every load
		attempt.  The ``plugin_info`` instance is passed as an argument to
		the callback.
		"""
# 		print "%s.loadPlugins" % self.__class__
		if not hasattr(self, '_candidates'):
			raise ValueError("locatePlugins must be called before loadPlugins")

		processed_plugins = []
		for candidate_infofile, candidate_filepath, plugin_info in self._candidates:
			# make sure to attribute a unique module name to the one
			# that is about to be loaded
			plugin_module_name_template = NormalizePluginNameForModuleName("yapsy_loaded_plugin_" + plugin_info.name) + "_%d"
			for plugin_name_suffix in range(len(sys.modules)):
				plugin_module_name =  plugin_module_name_template % plugin_name_suffix
				if plugin_module_name not in sys.modules:
					break
			
			# tolerance on the presence (or not) of the py extensions
			if candidate_filepath.endswith(".py"):
				candidate_filepath = candidate_filepath[:-3]
			# if a callback exists, call it before attempting to load
			# the plugin so that a message can be displayed to the
			# user
			if callback is not None:
				callback(plugin_info)
			# cover the case when the __init__ of a package has been
			# explicitely indicated
			if "__init__" in  os.path.basename(candidate_filepath):
				candidate_filepath = os.path.dirname(candidate_filepath)
			try:
				# use imp to correctly load the plugin as a module
				if os.path.isdir(candidate_filepath):
					candidate_module = imp.load_module(plugin_module_name,None,candidate_filepath,("py","r",imp.PKG_DIRECTORY))
				else:
					with open(candidate_filepath+".py","r") as plugin_file:
						candidate_module = imp.load_module(plugin_module_name,plugin_file,candidate_filepath+".py",("py","r",imp.PY_SOURCE))
			except Exception:
				exc_info = sys.exc_info()
				log.error("Unable to import plugin: %s" % candidate_filepath, exc_info=exc_info)
				plugin_info.error = exc_info
				processed_plugins.append(plugin_info)
				continue
			processed_plugins.append(plugin_info)
			if "__init__" in  os.path.basename(candidate_filepath):
				sys.path.remove(plugin_info.path)
			# now try to find and initialise the first subclass of the correct plugin interface
			for element in (getattr(candidate_module,name) for name in dir(candidate_module)):
				plugin_info_reference = None
				for category_name in self.categories_interfaces:
					try:
						is_correct_subclass = issubclass(element, self.categories_interfaces[category_name])
					except Exception:
						continue
					if is_correct_subclass and element is not self.categories_interfaces[category_name]:
							current_category = category_name
							if candidate_infofile not in self._category_file_mapping[current_category]:
								# we found a new plugin: initialise it and search for the next one
								if not plugin_info_reference:
									try:
										plugin_info.plugin_object = self.instanciateElement(element)
										plugin_info_reference = plugin_info
									except Exception:
										exc_info = sys.exc_info()
										log.error("Unable to create plugin object: %s" % candidate_filepath, exc_info=exc_info)
										plugin_info.error = exc_info
										break # If it didn't work once it wont again
								plugin_info.categories.append(current_category)
								self.category_mapping[current_category].append(plugin_info_reference)
								self._category_file_mapping[current_category].append(candidate_infofile)
		# Remove candidates list since we don't need them any more and
		# don't need to take up the space
		delattr(self, '_candidates')
		return processed_plugins

	def instanciateElement(self, element):
		"""
		Override this method to customize how plugins are instanciated
		"""
		return element()

	def collectPlugins(self):
		"""
		Walk through the plugins' places and look for plugins.  Then
		for each plugin candidate look for its category, load it and
		stores it in the appropriate slot of the category_mapping.
		"""
# 		print "%s.collectPlugins" % self.__class__		
		self.locatePlugins()
		self.loadPlugins()


	def getPluginByName(self,name,category="Default"):
		"""
		Get the plugin correspoding to a given category and name
		"""
		if category in self.category_mapping:
			for item in self.category_mapping[category]:
				if item.name == name:
					return item
		return None

	def activatePluginByName(self,name,category="Default"):
		"""
		Activate a plugin corresponding to a given category + name.
		"""
		pta_item = self.getPluginByName(name,category)
		if pta_item is not None:
			plugin_to_activate = pta_item.plugin_object
			if plugin_to_activate is not None:
				log.debug("Activating plugin: %s.%s"% (category,name))
				plugin_to_activate.activate()
				return plugin_to_activate			
		return None


	def deactivatePluginByName(self,name,category="Default"):
		"""
		Desactivate a plugin corresponding to a given category + name.
		"""
		if category in self.category_mapping:
			plugin_to_deactivate = None
			for item in self.category_mapping[category]:
				if item.name == name:
					plugin_to_deactivate = item.plugin_object
					break
			if plugin_to_deactivate is not None:
				log.debug("Deactivating plugin: %s.%s"% (category,name))
				plugin_to_deactivate.deactivate()
				return plugin_to_deactivate			
		return None


class PluginManagerSingleton(object):
	"""
	Singleton version of the most basic plugin manager.

	Being a singleton, this class should not be initialised explicitly
	and the ``get`` classmethod must be called instead.

	To call one of this class's methods you have to use the ``get``
	method in the following way:
	``PluginManagerSingleton.get().themethodname(theargs)``

	To set up the various coonfigurables variables of the
	PluginManager's behaviour please call explicitly the following
	methods:

	  - ``setCategoriesFilter`` for ``categories_filter``
	  - ``setPluginPlaces`` for ``directories_list``
	  - ``setPluginInfoExtension`` for ``plugin_info_ext``
	"""
	
	__instance = None
	
	__decoration_chain = None

	def __init__(self):
		if self.__instance is not None:
			raise Exception("Singleton can't be created twice !")
				
	def setBehaviour(self,list_of_pmd):
		"""
		Set the functionalities handled by the plugin manager by
		giving a list of ``PluginManager`` decorators.
		
		This function shouldn't be called several time in a same
		process, but if it is only the first call will have an effect.

		It also has an effect only if called before the initialisation
		of the singleton.

		In cases where the function is indeed going to change anything
		the ``True`` value is return, in all other cases, the ``False``
		value is returned.
		"""
		if self.__decoration_chain is None and self.__instance is None:
			log.debug("Setting up a specific behaviour for the PluginManagerSingleton")
			self.__decoration_chain = list_of_pmd
			return True
		else:
			log.debug("Useless call to setBehaviour: the singleton is already instanciated of already has a behaviour.")
			return False
	setBehaviour = classmethod(setBehaviour)


	def get(self):
		"""
		Actually create an instance
		"""
		if self.__instance is None:
			if self.__decoration_chain is not None:
				# Get the object to be decorated
#				print self.__decoration_chain
				pm = self.__decoration_chain[0]()
				for cls_item in self.__decoration_chain[1:]:
#					print cls_item
					pm = cls_item(decorated_manager=pm)
				# Decorate the whole object
				self.__instance = pm
			else:
				# initialise the 'inner' PluginManagerDecorator
				self.__instance = PluginManager()			
			log.debug("PluginManagerSingleton initialised")
		return self.__instance
	get = classmethod(get)


# For backward compatility import the most basic decorator (it changed
# place as of v1.8)
from yapsy.PluginManagerDecorator import PluginManagerDecorator

