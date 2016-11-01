# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-


"""
Role
====

The ``MultiprocessPluginProxy`` is instanciated by the MultiprocessPluginManager to replace the real implementation
that is run in a different process.

You cannot access your plugin directly from the parent process. You should use the child_pipe to communicate
with your plugin. The `MultiprocessPluginProxy`` role is to keep reference of the communication pipe to the
child process as well as the process informations.

API
===
"""

from yapsy.IPlugin import IPlugin


class MultiprocessPluginProxy(IPlugin):
	"""
	This class contains two members that are initialized by the :doc:`MultiprocessPluginManager`.

	self.proc is a reference that holds the multiprocessing.Process instance of the child process.

	self.child_pipe is a reference that holds the multiprocessing.Pipe instance to communicate with the child.
	"""
	def __init__(self):
		IPlugin.__init__(self)
		self.proc = None		# This attribute holds the multiprocessing.Process instance
		self.child_pipe = None  # This attribute holds the multiprocessing.Pipe instance
