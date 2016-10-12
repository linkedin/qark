# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-


"""
Role
====

The ``PluginFileLocator`` locates plugins when they are accessible via the filesystem.

It's default behaviour is to look for text files with the
'.yapsy-plugin' extensions and to read the plugin's decription in
them.


Customization
-------------

The behaviour of a ``PluginFileLocator`` can be customized by instanciating it with a specific 'analyzer'.

Two analyzers are already implemented and provided here:

    ``PluginFileAnalyzerWithInfoFile``

        the default 'analyzer' that looks for plugin 'info files' as
        text file with a predefined extension. This implements the way
        yapsy looks for plugin since version 1.

    ``PluginFileAnalyzerMathingRegex``

        look for files matching a regex and considers them as being
        the plugin itself.

All analyzers must enforce the 

It enforces the ``plugin locator`` policy as defined by ``IPluginLocator`` and used by ``PluginManager``.

    ``info_ext``

        expects a plugin to be discovered through its *plugin info file*.
        User just needs to provide an extension (without '.') to look
        for *plugin_info_file*.

    ``regexp``

        looks for file matching the given regular pattern expression.
        User just needs to provide the regular pattern expression.

All analyzers must enforce the policy represented by the ``IPluginFileAnalyzer`` interface.


API
===

"""

import os
import re
from yapsy import log
from yapsy.compat import ConfigParser, is_py2, basestring

from yapsy.PluginInfo import PluginInfo
from yapsy import PLUGIN_NAME_FORBIDEN_STRING
from yapsy.IPluginLocator import IPluginLocator




class IPluginFileAnalyzer(object):
	"""
	Define the methods expected by PluginFileLocator for its 'analyzer'.
	"""

	def __init__(self,name):
		self.name = name
	
	def isValidPlugin(self, filename):
		"""
		Check if the resource found at filename is a valid plugin.
		"""
		raise NotImplementedError("'isValidPlugin' must be reimplemented by %s" % self)	


	def getInfosDictFromPlugin(self, dirpath, filename):
		"""
		Returns the extracted plugin informations as a dictionary.
		This function ensures that "name" and "path" are provided.

		*dirpath* is the full path to the directory where the plugin file is

		*filename* is the name (ie the basename) of the plugin file.
		
		If *callback* function has not been provided for this strategy,
		we use the filename alone to extract minimal informations.
		"""
		raise NotImplementedError("'getInfosDictFromPlugin' must be reimplemented by %s" % self)


class PluginFileAnalyzerWithInfoFile(IPluginFileAnalyzer):
	"""
	Consider plugins described by a textual description file.

	A plugin is expected to be described by a text file ('ini' format) with a specific extension (.yapsy-plugin by default).

	This file must contain at least the following information::
	
	    [Core]
	    Name = name of the module
	    Module = relative_path/to/python_file_or_directory

	Optionnally the description file may also contain the following section (in addition to the above one)::

	    [Documentation]
	    Author = Author Name
	    Version = Major.minor
	    Website = url_for_plugin
	    Description = A simple one-sentence description

	Ctor Arguments:
		
		*name* name of the analyzer.

		*extensions* the expected extensions for the plugin info file. May be a string or a tuple of strings if several extensions are expected.
	"""
	
	def __init__(self, name, extensions="yapsy-plugin"):
		IPluginFileAnalyzer.__init__(self,name)
		self.setPluginInfoExtension(extensions)

	
	def setPluginInfoExtension(self,extensions):
		"""
		Set the extension that will identify a plugin info file.

		*extensions* May be a string or a tuple of strings if several extensions are expected.
		"""
		# Make sure extension is a tuple
		if not isinstance(extensions, tuple):
			extensions = (extensions, )
		self.expectedExtensions = extensions
		
	
	def isValidPlugin(self, filename):
		"""
		Check if it is a valid plugin based on the given plugin info file extension(s).
		If several extensions are provided, the first matching will cause the function
		to exit successfully.
		"""
		res = False
		for ext in self.expectedExtensions:
			if filename.endswith(".%s" % ext):
				res = True
				break
		return res
	
	def getPluginNameAndModuleFromStream(self, infoFileObject, candidate_infofile=None):
		"""
		Extract the name and module of a plugin from the
		content of the info file that describes it and which
		is stored in ``infoFileObject``.
		
		.. note:: Prefer using ``_extractCorePluginInfo``
		          instead, whenever possible...
		
		.. warning:: ``infoFileObject`` must be a file-like object:
		             either an opened file for instance or a string
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
		# parse the information buffer to get info about the plugin
		config_parser = ConfigParser()
		try:
			if is_py2:
				config_parser.readfp(infoFileObject)
			else:
				config_parser.read_file(infoFileObject)
		except Exception as e:
			log.debug("Could not parse the plugin file '%s' (exception raised was '%s')" % (candidate_infofile,e))
			return (None, None, None)
		# check if the basic info is available
		if not config_parser.has_section("Core"):
			log.debug("Plugin info file has no 'Core' section (in '%s')" % candidate_infofile)
			return (None, None, None)
		if not config_parser.has_option("Core","Name") or not config_parser.has_option("Core","Module"):
			log.debug("Plugin info file has no 'Name' or 'Module' section (in '%s')" % candidate_infofile)
			return (None, None, None)
		# check that the given name is valid
		name = config_parser.get("Core", "Name")
		name = name.strip()
		if PLUGIN_NAME_FORBIDEN_STRING in name:
			log.debug("Plugin name contains forbiden character: %s (in '%s')" % (PLUGIN_NAME_FORBIDEN_STRING,
																					candidate_infofile))
			return (None, None, None)
		return (name, config_parser.get("Core", "Module"), config_parser)
	
	def _extractCorePluginInfo(self,directory, filename):
		"""
		Gather the core information (name, and module to be loaded)
		about a plugin described by it's info file (found at
		'directory/filename').
		
		Return a dictionary with name and path of the plugin as well
		as the ConfigParser instance used to collect these info.
		
		.. note:: This is supposed to be used internally by subclasses
		          and decorators.
		"""
		# now we can consider the file as a serious candidate
		if not isinstance(filename, basestring):
			# filename is a file object: use it
			name, moduleName, config_parser = self.getPluginNameAndModuleFromStream(filename)
		else:
			candidate_infofile_path = os.path.join(directory, filename)
			# parse the information file to get info about the plugin
			with open(candidate_infofile_path) as candidate_infofile:
				name, moduleName, config_parser = self.getPluginNameAndModuleFromStream(candidate_infofile,candidate_infofile_path)
		if (name, moduleName, config_parser) == (None, None, None):
			return (None,None)
		infos = {"name":name, "path":os.path.join(directory, moduleName)}
		return infos, config_parser
	
	def _extractBasicPluginInfo(self,directory, filename):
		"""
		Gather some basic documentation about the plugin described by
		it's info file (found at 'directory/filename').
		
		Return a dictionary containing the core information (name and
		path) as well as as the 'documentation' info (version, author,
		description etc).
		
		See also:
		
		  ``self._extractCorePluginInfo``
		"""
		infos, config_parser = self._extractCorePluginInfo(directory, filename)
		# collect additional (but usually quite usefull) information
		if infos and config_parser and config_parser.has_section("Documentation"):
			if config_parser.has_option("Documentation","Author"):
				infos["author"]	= config_parser.get("Documentation", "Author")
			if config_parser.has_option("Documentation","Version"):
				infos["version"] = config_parser.get("Documentation", "Version")
			if config_parser.has_option("Documentation","Website"):
				infos["website"] = config_parser.get("Documentation", "Website")
			if config_parser.has_option("Documentation","Copyright"):
				infos["copyright"]	= config_parser.get("Documentation", "Copyright")
			if config_parser.has_option("Documentation","Description"):
				infos["description"] = config_parser.get("Documentation", "Description")
		return infos, config_parser
		
	def getInfosDictFromPlugin(self, dirpath, filename):
		"""
		Returns the extracted plugin informations as a dictionary.
		This function ensures that "name" and "path" are provided.

		If *callback* function has not been provided for this strategy,
		we use the filename alone to extract minimal informations.
		"""
		infos, config_parser = self._extractBasicPluginInfo(dirpath, filename)
		if not infos or infos.get("name", None) is None:
			raise ValueError("Missing *name* of the plugin in extracted infos.")
		if not infos or infos.get("path", None) is None:
			raise ValueError("Missing *path* of the plugin in extracted infos.")
		return infos, config_parser

	
class PluginFileAnalyzerMathingRegex(IPluginFileAnalyzer):
	"""
	An analyzer that targets plugins decribed by files whose name match a given regex.
	"""
	def __init__(self, name, regexp):
		IPluginFileAnalyzer.__init__(self,name)
		self.regexp = regexp
	
	def isValidPlugin(self, filename):
		"""
		Checks if the given filename is a valid plugin for this Strategy
		"""
		reg = re.compile(self.regexp)
		if reg.match(filename) is not None:
			return True
		return False
	
	def getInfosDictFromPlugin(self, dirpath, filename):
		"""
		Returns the extracted plugin informations as a dictionary.
		This function ensures that "name" and "path" are provided.
		"""
		# use the filename alone to extract minimal informations.
		infos = {}
		module_name = os.path.splitext(filename)[0]
		plugin_filename = os.path.join(dirpath,filename)
		if module_name == "__init__":
			module_name = os.path.basename(dirpath)
			plugin_filename = dirpath
		infos["name"] = "%s" % module_name
		infos["path"] = plugin_filename
		cf_parser = ConfigParser()
		cf_parser.add_section("Core")
		cf_parser.set("Core","Name",infos["name"])
		cf_parser.set("Core","Module",infos["path"])
		return infos,cf_parser



class PluginFileLocator(IPluginLocator):
	"""
	Locates plugins on the file system using a set of analyzers to
	determine what files actually corresponds to plugins.
	
	If more than one analyzer is being used, the first that will discover a
	new plugin will avoid other strategies to find it too.

	By default each directory set as a "plugin place" is scanned
	recursively. You can change that by a call to
	``disableRecursiveScan``.
	"""
	
	def __init__(self, analyzers=None, plugin_info_cls=PluginInfo):
		IPluginLocator.__init__(self)
		self._discovered_plugins = {}
		self.setPluginPlaces(None)
		self._analyzers = analyzers      # analyzers used to locate plugins
		if self._analyzers is None:
			self._analyzers = [PluginFileAnalyzerWithInfoFile("info_ext")]
		self._default_plugin_info_cls = PluginInfo
		self._plugin_info_cls_map = {}
		self._max_size = 1e3*1024 # in octets (by default 1 Mo)
		self.recursive = True
		
	def disableRecursiveScan(self):
		"""
		Disable recursive scan of the directories given as plugin places.
		"""
		self.recursive = False		
	
	def setAnalyzers(self, analyzers):
		"""
		Sets a new set of analyzers.

		.. warning:: the new analyzers won't be aware of the plugin
		             info class that may have been set via a previous
		             call to ``setPluginInfoClass``.
		"""
		self._analyzers = analyzers

	def removeAnalyzers(self, name):
		"""
		Removes analyzers of a given name.
		"""
		analyzersListCopy = self._analyzers[:]
		foundAndRemoved = False
		for obj in analyzersListCopy:
			if obj.name == name:
				self._analyzers.remove(obj)
				foundAndRemoved = True
		if not foundAndRemoved:
			log.debug("'%s' is not a known strategy name: can't remove it." % name)

	def removeAllAnalyzer(self):
		"""
		Remove all analyzers.
		"""
		self._analyzers = []
	
	def appendAnalyzer(self, analyzer):
		"""
		Append an analyzer to the existing list.
		"""
		self._analyzers.append(analyzer)


	def _getInfoForPluginFromAnalyzer(self,analyzer,dirpath, filename):
		"""
		Return an instance of plugin_info_cls filled with data extracted by the analyzer.

		May return None if the analyzer fails to extract any info.
		"""
		plugin_info_dict,config_parser = analyzer.getInfosDictFromPlugin(dirpath, filename)
		if plugin_info_dict is None:
			return None
		plugin_info_cls = self._plugin_info_cls_map.get(analyzer.name,self._default_plugin_info_cls)
		plugin_info = plugin_info_cls(plugin_info_dict["name"],plugin_info_dict["path"])
		plugin_info.details = config_parser
		return plugin_info
	
	def locatePlugins(self):
		"""
		Walk through the plugins' places and look for plugins.

		Return the candidates and number of plugins found.
		"""
# 		print "%s.locatePlugins" % self.__class__
		_candidates = []
		_discovered = {}
		for directory in map(os.path.abspath, self.plugins_places):
			# first of all, is it a directory :)
			if not os.path.isdir(directory):
				log.debug("%s skips %s (not a directory)" % (self.__class__.__name__, directory))
				continue
			if self.recursive:
				debug_txt_mode = "recursively"
				walk_iter = os.walk(directory, followlinks=True)
			else:
				debug_txt_mode = "non-recursively"
				walk_iter = [(directory,[],os.listdir(directory))]
			# iteratively walks through the directory
			log.debug("%s walks (%s) into directory: %s" % (self.__class__.__name__, debug_txt_mode, directory))
			for item in walk_iter:
				dirpath = item[0]
				for filename in item[2]:
					# print("testing candidate file %s" % filename)
					for analyzer in self._analyzers:
						# print("... with analyzer %s" % analyzer.name)
						# eliminate the obvious non plugin files
						if not analyzer.isValidPlugin(filename):
							log.debug("%s is not a valid plugin for strategy %s" % (filename, analyzer.name))
							continue
						candidate_infofile = os.path.join(dirpath, filename)
						if candidate_infofile in _discovered:
							log.debug("%s (with strategy %s) rejected because already discovered" % (candidate_infofile, analyzer.name))
							continue
						log.debug("%s found a candidate:\n    %s" % (self.__class__.__name__, candidate_infofile))
#						print candidate_infofile
						plugin_info = self._getInfoForPluginFromAnalyzer(analyzer, dirpath, filename)
						if plugin_info is None:
							log.warning("Plugin candidate '%s'  rejected by strategy '%s'" % (candidate_infofile, analyzer.name))
							break # we consider this was the good strategy to use for: it failed -> not a plugin -> don't try another strategy
						# now determine the path of the file to execute,
						# depending on wether the path indicated is a
						# directory or a file
#					print plugin_info.path
						# Remember all the files belonging to a discovered
						# plugin, so that strategies (if several in use) won't
						# collide
						if os.path.isdir(plugin_info.path):
							candidate_filepath = os.path.join(plugin_info.path, "__init__")
							# it is a package, adds all the files concerned
							for _file in os.listdir(plugin_info.path):
								if _file.endswith(".py"):
									self._discovered_plugins[os.path.join(plugin_info.path, _file)] = candidate_filepath
									_discovered[os.path.join(plugin_info.path, _file)] = candidate_filepath
						elif (plugin_info.path.endswith(".py") and os.path.isfile(plugin_info.path)) or os.path.isfile(plugin_info.path+".py"):
							candidate_filepath = plugin_info.path
							if candidate_filepath.endswith(".py"):
								candidate_filepath = candidate_filepath[:-3]
							# it is a file, adds it
							self._discovered_plugins[".".join((plugin_info.path, "py"))] = candidate_filepath
							_discovered[".".join((plugin_info.path, "py"))] = candidate_filepath
						else:
							log.error("Plugin candidate rejected: cannot find the file or directory module for '%s'" % (candidate_infofile))
							break
#					print candidate_filepath
						_candidates.append((candidate_infofile, candidate_filepath, plugin_info))
						# finally the candidate_infofile must not be discovered again
						_discovered[candidate_infofile] = candidate_filepath
						self._discovered_plugins[candidate_infofile] = candidate_filepath
#						print "%s found by strategy %s" % (candidate_filepath, analyzer.name)
		return _candidates, len(_candidates)

	def gatherCorePluginInfo(self, directory, filename):
		"""
		Return a ``PluginInfo`` as well as the ``ConfigParser`` used to build it.
		
		If filename is a valid plugin discovered by any of the known
		strategy in use. Returns None,None otherwise.
		"""
		for analyzer in self._analyzers:
			# eliminate the obvious non plugin files
			if not analyzer.isValidPlugin(filename):
				continue
			plugin_info = self._getInfoForPluginFromAnalyzer(analyzer,directory, filename)
			return plugin_info,plugin_info.details
		return None,None
	
	# -----------------------------------------------
	# Backward compatible methods
	# Note: their implementation must be conform to their
	# counterpart in yapsy<1.10
	# -----------------------------------------------

	def getPluginNameAndModuleFromStream(self, infoFileObject, candidate_infofile=None):
		for analyzer in self._analyzers:
			if analyzer.name == "info_ext":
				return analyzer.getPluginNameAndModuleFromStream(infoFileObject)
		else:
			raise RuntimeError("No current file analyzer is able to provide plugin information from stream")
	
	def setPluginInfoClass(self, picls, name=None):
		"""
		Set the class that holds PluginInfo. The class should inherit
		from ``PluginInfo``.

		If name is given, then the class will be used only by the corresponding analyzer.
		
		If name is None, the class will be set for all analyzers.
		"""
		if name is None:
			self._default_plugin_info_cls = picls
			self._plugin_info_cls_map = {}
		else:
			self._plugin_info_cls_map[name] = picls
			
	def setPluginPlaces(self, directories_list):
		"""
		Set the list of directories where to look for plugin places.
		"""
		if directories_list is None:
			directories_list = [os.path.dirname(__file__)]
		self.plugins_places = directories_list

	def updatePluginPlaces(self, directories_list):
		"""
		Updates the list of directories where to look for plugin places.
		"""
		self.plugins_places = list(set.union(set(directories_list), set(self.plugins_places)))

	def setPluginInfoExtension(self, ext):
		"""
		DEPRECATED(>1.9): for backward compatibility. Directly configure the
		IPluginLocator instance instead !

		This will only work if the strategy "info_ext" is active
		for locating plugins.
		"""
		for analyzer in self._analyzers:
			if analyzer.name == "info_ext":
				analyzer.setPluginInfoExtension(ext)
