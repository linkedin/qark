# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-



"""
Role
====

``IPluginLocator`` defines the basic interface expected by a
``PluginManager`` to be able to locate plugins and get basic info
about each discovered plugin (name, version etc).

API
===

"""


from yapsy import log

class IPluginLocator(object):
	"""
	Plugin Locator interface with some methods already implemented to
	manage the awkward backward compatible stuff.
	"""
	
	def locatePlugins(self):
		"""
		Walk through the plugins' places and look for plugins.

		Return the discovered plugins as a list of
		``(candidate_infofile_path, candidate_file_path,plugin_info_instance)``
		and their number.
		"""
		raise NotImplementedError("locatePlugins must be reimplemented by %s" % self)
	
	def gatherCorePluginInfo(self, directory, filename):
		"""
		Return a ``PluginInfo`` as well as the ``ConfigParser`` used to build it.
		
		If filename is a valid plugin discovered by any of the known
		strategy in use. Returns None,None otherwise.
		"""
		raise NotImplementedError("gatherPluginInfo must be reimplemented by %s" % self)
	
	# --------------------------------------------------------------------
	# Below are backward compatibility methods: if you inherit from
	# IPluginLocator it's ok not to reimplement them, there will only
	# be a warning message logged if they are called and not
	# reimplemented.
	# --------------------------------------------------------------------
	
	def getPluginNameAndModuleFromStream(self,fileobj):
		"""
		DEPRECATED(>1.9): kept for backward compatibility
		with existing PluginManager child classes.
		
		Return a 3-uple with the name of the plugin, its
		module and the config_parser used to gather the core
		data *in a tuple*, if the required info could be
		localised, else return ``(None,None,None)``.
		"""
		log.warn("setPluginInfoClass was called but '%s' doesn't implement it." % self)
		return None,None,None
	

	def setPluginInfoClass(self, picls, names=None):
		"""
		DEPRECATED(>1.9): kept for backward compatibility
		with existing PluginManager child classes.
		
		Set the class that holds PluginInfo. The class should inherit
		from ``PluginInfo``.
		"""
		log.warn("setPluginInfoClass was called but '%s' doesn't implement it." % self)

	def getPluginInfoClass(self):
		"""
		DEPRECATED(>1.9): kept for backward compatibility
		with existing PluginManager child classes.
		
		Get the class that holds PluginInfo.
		"""
		log.warn("getPluginInfoClass was called but '%s' doesn't implement it." % self)
		return None

	def setPluginPlaces(self, directories_list):
		"""
		DEPRECATED(>1.9): kept for backward compatibility
		with existing PluginManager child classes.
		
		Set the list of directories where to look for plugin places.
		"""
		log.warn("setPluginPlaces was called but '%s' doesn't implement it." % self)

	def updatePluginPlaces(self, directories_list):
		"""
		DEPRECATED(>1.9): kept for backward compatibility
		with existing PluginManager child classes.
		
		Updates the list of directories where to look for plugin places.
		"""
		log.warn("updatePluginPlaces was called but '%s' doesn't implement it." % self)

