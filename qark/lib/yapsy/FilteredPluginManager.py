# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

"""
Role
====

Defines the basic mechanisms to have a plugin manager filter the
available list of plugins after locating them and before loading them.

One use fo this would be to prevent untrusted plugins from entering
the system.

To use it properly you must reimplement or monkey patch the
``IsPluginOk`` method, as in the following example::

  # define a plugin manager (with you prefered options)
  pm = PluginManager(...)
  # decorate it with the Filtering mechanics
  pm = FilteredPluginManager(pm)
  # define a custom predicate that filters out plugins without descriptions
  pm.isPluginOk = lambda x: x.description!=""


API
===
"""
 

from yapsy.IPlugin import IPlugin
from yapsy.PluginManagerDecorator import  PluginManagerDecorator


class FilteredPluginManager(PluginManagerDecorator):
	"""
	Base class for decorators which filter the plugins list
	before they are loaded.
	"""

	def __init__(self, 
				 decorated_manager=None,
				 categories_filter=None, 
				 directories_list=None, 
				 plugin_info_ext="yapsy-plugin"):
		if categories_filter is None:
			categories_filter = {"Default":IPlugin}
		# Create the base decorator class
		PluginManagerDecorator.__init__(self,decorated_manager,
										categories_filter,
										directories_list,
										plugin_info_ext)
		# prepare the mapping of the latest version of each plugin
		self.rejectedPlugins =  [ ] 



	def filterPlugins(self):
		"""
		Go through the currently available candidates, and and either
		leaves them, or moves them into the list of rejected Plugins.
		
		Can be overridden if overriding ``isPluginOk`` sentinel is not
		powerful enough.
		"""
		self.rejectedPlugins = [ ]
		for candidate_infofile, candidate_filepath, plugin_info in self._component.getPluginCandidates():
			if not self.isPluginOk( plugin_info):
				self.rejectPluginCandidate((candidate_infofile, candidate_filepath, plugin_info) )

	def rejectPluginCandidate(self,pluginTuple):
		"""
		Move a plugin from the candidates list to the rejected List.
		"""
		if pluginTuple in self.getPluginCandidates():
			self._component.removePluginCandidate(pluginTuple)
		if not pluginTuple in self.rejectedPlugins:
			self.rejectedPlugins.append(pluginTuple)

	def unrejectPluginCandidate(self,pluginTuple):
		"""
		Move a plugin from the rejected list to into the candidates
		list.
		"""
		if not pluginTuple in self.getPluginCandidates():
			self._component.appendPluginCandidate(pluginTuple)
		if pluginTuple in self.rejectedPlugins:
			self.rejectedPlugins.remove(pluginTuple)

	def removePluginCandidate(self,pluginTuple):
		"""
		Remove a plugin from the list of candidates.
		"""
		if pluginTuple in self.getPluginCandidates():
			self._component.removePluginCandidate(pluginTuple)
		if  pluginTuple in self.rejectedPlugins:
			self.rejectedPlugins.remove(pluginTuple)


	def appendPluginCandidate(self,pluginTuple):
		"""
		Add a new candidate.
		"""
		if self.isPluginOk(pluginTuple[2]):
			if pluginTuple not in self.getPluginCandidates():
				self._component.appendPluginCandidate(pluginTuple)
		else:
			if not pluginTuple in self.rejectedPlugins:
				self.rejectedPlugins.append(pluginTuple)

	def isPluginOk(self,info):
		"""
		Sentinel function to detect if a plugin should be filtered.

		``info`` is an instance of a ``PluginInfo`` and this method is
		expected to return True if the corresponding plugin can be
		accepted, and False if it must be filtered out.
		
		Subclasses should override this function and return false for
		any plugin which they do not want to be loadable.
		"""
		return True

	def locatePlugins(self):
		"""
		locate and filter plugins.
		"""
		#Reset Catalogue
		self.setCategoriesFilter(self._component.categories_interfaces)
		#Reread and filter.
		self._component.locatePlugins()
		self.filterPlugins()
		return len(self._component.getPluginCandidates()) 

	def getRejectedPlugins(self):
		"""
		Return the list of rejected plugins.
		"""
		return self.rejectedPlugins[:]
