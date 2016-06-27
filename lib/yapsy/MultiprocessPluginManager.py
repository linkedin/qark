# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

"""
Role
====

Defines a plugin manager that runs all plugins in separate process
linked by pipes.


API
===
"""

import multiprocessing as mproc

from yapsy.IMultiprocessChildPlugin import IMultiprocessChildPlugin
from yapsy.MultiprocessPluginProxy import MultiprocessPluginProxy
from yapsy.PluginManager import  PluginManager


class MultiprocessPluginManager(PluginManager):
	"""
	Subclass of the PluginManager that runs each plugin in a different process
	"""

	def __init__(self,
				 categories_filter=None,
				 directories_list=None,
				 plugin_info_ext=None,
				 plugin_locator=None):
		if categories_filter is None:
			categories_filter = {"Default": IMultiprocessChildPlugin}
		PluginManager.__init__(self,
								 categories_filter=categories_filter,
								 directories_list=directories_list,
								 plugin_info_ext=plugin_info_ext,
								 plugin_locator=plugin_locator)

	def instanciateElement(self, element):
		"""
		This method instanciate each plugin in a new process and link it to
		the parent with a pipe.

		In the parent process context, the plugin's class is replaced by the ``MultiprocessPluginProxy``
		class that hold the information about the child process and the pipe to communicate with it. See
		:doc:`IMultiprocessChildPlugin`
		"""
		instanciated_element = MultiprocessPluginProxy()
		parent_pipe, child_pipe = mproc.Pipe()
		instanciated_element.proc = element(child_pipe)
		instanciated_element.child_pipe = parent_pipe
		instanciated_element.proc.start()
		return instanciated_element

