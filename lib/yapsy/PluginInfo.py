# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-


"""
Role
====

Encapsulate a plugin instance as well as some metadata.

API
===
"""

from yapsy.compat import ConfigParser
from distutils.version import StrictVersion


class PluginInfo(object):
	"""Representation of the most basic set of information related to a
	given plugin such as its name, author, description...

	Any additional information can be stored ad retrieved in a
	PluginInfo, when this one is created with a
	``ConfigParser.ConfigParser`` instance.

	This typically means that when metadata is read from a text file
	(the original way for yapsy to describe plugins), all info that is
	not part of the basic variables (name, path, version etc), can
	still be accessed though the ``details`` member variables that
	behaves like Python's ``ConfigParser.ConfigParser``.

	Warning: the instance associated with the ``details`` member
	variable is never copied and used to store all plugin infos. If
	you set it to a custom instance, it will be modified as soon as
	another member variale of the plugin info is
	changed. Alternatively, if you change the instance "outside" the
	plugin info, it will also change the plugin info.

	Ctor Arguments:

		*plugin_name* is  a simple string describing the name of
         the plugin.

		*plugin_path* describe the location where the plugin can be
         found.
		
	.. warning:: The ``path`` attribute is the full path to the
	             plugin if it is organised as a directory or the
	             full path to a file without the ``.py`` extension
	             if the plugin is defined by a simple file. In the
	             later case, the actual plugin is reached via
	             ``plugin_info.path+'.py'``.
	"""
	
	def __init__(self, plugin_name, plugin_path):
		self.__details = ConfigParser()
		self.name = plugin_name
		self.path = plugin_path
		self._ensureDetailsDefaultsAreBackwardCompatible()
		# Storage for stuff created during the plugin lifetime
		self.plugin_object = None
		self.categories    = []
		self.error = None


	def __setDetails(self,cfDetails):
		"""
		Fill in all details by storing a ``ConfigParser`` instance.

		.. warning: The values for ``plugin_name`` and
		            ``plugin_path`` given a init time will superseed
		            any value found in ``cfDetails`` in section
		            'Core' for the options 'Name' and 'Module' (this
		            is mostly for backward compatibility).
		"""	
		bkp_name = self.name
		bkp_path = self.path
		self.__details = cfDetails
		self.name = bkp_name
		self.path = bkp_path
		self._ensureDetailsDefaultsAreBackwardCompatible()
	
	def __getDetails(self):
		return self.__details
		
	def __getName(self):
		return self.details.get("Core","Name")
	
	def __setName(self, name):
		if not self.details.has_section("Core"):
			self.details.add_section("Core")
		self.details.set("Core","Name",name)

	
	def __getPath(self):
		return self.details.get("Core","Module")
	
	def __setPath(self,path):
		if not self.details.has_section("Core"):
			self.details.add_section("Core")
		self.details.set("Core","Module",path)

	
	def __getVersion(self):
		return StrictVersion(self.details.get("Documentation","Version"))
	
	def setVersion(self, vstring):
		"""
		Set the version of the plugin.

		Used by subclasses to provide different handling of the
		version number.
		"""
		if isinstance(vstring,StrictVersion):
			vstring = str(vstring)
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		self.details.set("Documentation","Version",vstring)

	def __getAuthor(self):
		return self.details.get("Documentation","Author")
		
	def __setAuthor(self,author):
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		self.details.set("Documentation","Author",author)


	def __getCopyright(self):
		return self.details.get("Documentation","Copyright")
		
	def __setCopyright(self,copyrightTxt):
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		self.details.set("Documentation","Copyright",copyrightTxt)

	
	def __getWebsite(self):
		return self.details.get("Documentation","Website")
		
	def __setWebsite(self,website):
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		self.details.set("Documentation","Website",website)

	
	def __getDescription(self):
		return self.details.get("Documentation","Description")
	
	def __setDescription(self,description):
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		return self.details.set("Documentation","Description",description)


	def __getCategory(self):
		"""
		DEPRECATED (>1.9): Mimic former behaviour when what is
		noz the first category was considered as the only one the
		plugin belonged to.
		"""		
		if self.categories:
			return self.categories[0]
		else:
			return "UnknownCategory"
	
	def __setCategory(self,c):
		"""
		DEPRECATED (>1.9): Mimic former behaviour by making so
		that if a category is set as it it was the only category to
		which the plugin belongs, then a __getCategory will return
		this newly set category.
		"""
		self.categories = [c] + self.categories
	
	name = property(fget=__getName,fset=__setName)
	path = property(fget=__getPath,fset=__setPath)
	version = property(fget=__getVersion,fset=setVersion)
	author = property(fget=__getAuthor,fset=__setAuthor)
	copyright = property(fget=__getCopyright,fset=__setCopyright)
	website = property(fget=__getWebsite,fset=__setWebsite)
	description = property(fget=__getDescription,fset=__setDescription)
	details = property(fget=__getDetails,fset=__setDetails)
	# deprecated (>1.9): plugins are not longer associated to a
	# single category !
	category = property(fget=__getCategory,fset=__setCategory)
	
	def _getIsActivated(self):
		"""
		Return the activated state of the plugin object.
		Makes it possible to define a property.
		"""
		return self.plugin_object.is_activated
	
	is_activated = property(fget=_getIsActivated)
	
	def _ensureDetailsDefaultsAreBackwardCompatible(self):
		"""
		Internal helper function.
		"""
		if not self.details.has_option("Documentation","Author"):
			self.author		= "Unknown"
		if not self.details.has_option("Documentation","Version"):
			self.version	= "0.0"
		if not self.details.has_option("Documentation","Website"):
			self.website	= "None"
		if not self.details.has_option("Documentation","Copyright"):
			self.copyright	= "Unknown"
		if not self.details.has_option("Documentation","Description"):
			self.description = ""
