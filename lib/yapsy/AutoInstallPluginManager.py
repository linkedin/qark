# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

"""
Role
====

Defines plugin managers that can handle the installation of plugin
files into the right place. Then the end-user does not have to browse
to the plugin directory to install them.

API
===
"""

import os
import shutil
import zipfile

from yapsy.IPlugin import IPlugin
from yapsy.PluginManagerDecorator import PluginManagerDecorator
from yapsy import log
from yapsy.compat import StringIO, str


class AutoInstallPluginManager(PluginManagerDecorator):
	"""
	A plugin manager that also manages the installation of the plugin
	files into the appropriate directory.

	Ctor Arguments:
		
	    ``plugin_install_dir``
  	    The directory where new plugins to be installed will be copied.

	.. warning:: If ``plugin_install_dir`` does not correspond to
	             an element of the ``directories_list``, it is
	             appended to the later.			
	"""


	def __init__(self,
				 plugin_install_dir=None,
				 decorated_manager=None,
				 # The following args will only be used if we need to
				 # create a default PluginManager
				 categories_filter=None, 
				 directories_list=None, 
				 plugin_info_ext="yapsy-plugin"):
		if categories_filter is None:
			categories_filter = {"Default":IPlugin}
		# Create the base decorator class
		PluginManagerDecorator.__init__(self,
										decorated_manager,
										categories_filter,
										directories_list,
										plugin_info_ext)
		# set the directory for new plugins
		self.plugins_places=[]
		self.setInstallDir(plugin_install_dir)

	def setInstallDir(self,plugin_install_dir):
		"""
		Set the directory where to install new plugins.
		"""
		if not (plugin_install_dir in self.plugins_places):
			self.plugins_places.append(plugin_install_dir)
		self.install_dir = plugin_install_dir

	def getInstallDir(self):
		"""
		Return the directory where new plugins should be installed.
		"""
		return self.install_dir

	def install(self, directory, plugin_info_filename):
		"""
		Giving the plugin's info file (e.g. ``myplugin.yapsy-plugin``),
		and the directory where it is located, get all the files that
		define the plugin and copy them into the correct directory.
		
		Return ``True`` if the installation is a success, ``False`` if
		it is a failure.
		"""
		# start collecting essential info about the new plugin
		plugin_info, config_parser = self._gatherCorePluginInfo(directory, plugin_info_filename)
		# now determine the path of the file to execute,
		# depending on wether the path indicated is a
		# directory or a file
		if not (os.path.exists(plugin_info.path) or os.path.exists(plugin_info.path+".py") ):
			log.warning("Could not find the plugin's implementation for %s." % plugin_info.name)
			return False
		if os.path.isdir(plugin_info.path):
			try:
				shutil.copytree(plugin_info.path,
								os.path.join(self.install_dir,os.path.basename(plugin_info.path)))
				shutil.copy(os.path.join(directory, plugin_info_filename),
							self.install_dir)
			except:
				log.error("Could not install plugin: %s." % plugin_info.name)
				return False
			else:
				return True
		elif os.path.isfile(plugin_info.path+".py"):
			try:
				shutil.copy(plugin_info.path+".py",
							self.install_dir)
				shutil.copy(os.path.join(directory, plugin_info_filename),
						   self.install_dir)
			except:
				log.error("Could not install plugin: %s." % plugin_info.name)
				return False
			else:
				return True
		else:
			return False
		
		
	def installFromZIP(self, plugin_ZIP_filename):
		"""
		Giving the plugin's zip file (e.g. ``myplugin.zip``), check
		that their is a valid info file in it and correct all the
		plugin files into the correct directory.
		
		.. warning:: Only available for python 2.6 and later.
		
		Return ``True`` if the installation is a success, ``False`` if
		it is a failure.
		"""
		if not os.path.isfile(plugin_ZIP_filename):
			log.warning("Could not find the plugin's zip file at '%s'." % plugin_ZIP_filename)
			return False
		try:
			candidateZipFile = zipfile.ZipFile(plugin_ZIP_filename)
			first_bad_file = candidateZipFile.testzip()
			if first_bad_file:
				raise Exception("Corrupted ZIP with first bad file '%s'" % first_bad_file)
		except Exception as e:
			log.warning("Invalid zip file '%s' (error: %s)." % (plugin_ZIP_filename,e))
			return False
		zipContent = candidateZipFile.namelist()
		log.info("Investigating the content of a zip file containing: '%s'" % zipContent)
		log.info("Sanity checks on zip's contained files (looking for hazardous path symbols).")	
		# check absence of root path and ".." shortcut that would
		# send the file oustide the desired directory
		for containedFileName in zipContent:
			# WARNING: the sanity checks below are certainly not
			# exhaustive (maybe we could do something a bit smarter by
			# using os.path.expanduser, os.path.expandvars and
			# os.path.normpath)
			if containedFileName.startswith("/"):
				log.warning("Unsecure zip file, rejected because one of its file paths ('%s') starts with '/'" % containedFileName)
				return False
			if containedFileName.startswith(r"\\") or containedFileName.startswith("//"):
				log.warning(r"Unsecure zip file, rejected because one of its file paths ('%s') starts with '\\'" % containedFileName)
				return False
			if os.path.splitdrive(containedFileName)[0]:
				log.warning("Unsecure zip file, rejected because one of its file paths ('%s') starts with a drive letter" % containedFileName)
				return False
			if os.path.isabs(containedFileName):
				log.warning("Unsecure zip file, rejected because one of its file paths ('%s') is absolute" % containedFileName)
				return False
			pathComponent = os.path.split(containedFileName)
			if ".." in pathComponent:
				log.warning("Unsecure zip file, rejected because one of its file paths ('%s') contains '..'" % containedFileName)	
				return False
			if "~" in pathComponent:
				log.warning("Unsecure zip file, rejected because one of its file paths ('%s') contains '~'" % containedFileName)	
				return False
		infoFileCandidates = [filename for filename in zipContent if os.path.dirname(filename)==""]
		if not infoFileCandidates:
			log.warning("Zip file structure seems wrong in '%s', no info file found." % plugin_ZIP_filename)
			return False
		isValid = False
		log.info("Looking for the zipped plugin's info file among '%s'" % infoFileCandidates)
		for infoFileName in infoFileCandidates:
			infoFile = candidateZipFile.read(infoFileName)
			log.info("Assuming the zipped plugin info file to be '%s'" % infoFileName)
			pluginName,moduleName,_ = self._getPluginNameAndModuleFromStream(StringIO(str(infoFile,encoding="utf-8")))
			if moduleName is None:
					continue
			log.info("Checking existence of the expected module '%s' in the zip file" % moduleName)
			if moduleName in zipContent or os.path.join(moduleName,"__init__.py") in zipContent:
				isValid = True
				break
		if not isValid:
			log.warning("Zip file structure seems wrong in '%s', "
							"could not match info file with the implementation of plugin '%s'." % (plugin_ZIP_filename,pluginName))
			return False
		else:
			try:
				candidateZipFile.extractall(self.install_dir)
				return True
			except Exception as e:
				log.error("Could not install plugin '%s' from zip file '%s' (exception: '%s')." % (pluginName,plugin_ZIP_filename,e))
				return False
		
