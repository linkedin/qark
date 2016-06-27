# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-


"""
Role
====

Defines the basic interfaces for a plugin. These interfaces are
inherited by the *core* class of a plugin. The *core* class of a
plugin is then the one that will be notified the
activation/deactivation of a plugin via the ``activate/deactivate``
methods.


For simple (near trivial) plugin systems, one can directly use the
following interfaces.

Extensibility
=============

In your own software, you'll probably want to build derived classes of
the ``IPlugin`` class as it is a mere interface with no specific
functionality.

Your software's plugins should then inherit your very own plugin class
(itself derived from ``IPlugin``).

Where and how to code these plugins is explained in the section about
the :doc:`PluginManager`.


API
===
"""


class IPlugin(object):
	"""
	The most simple interface to be inherited when creating a plugin.
	"""

	def __init__(self):
		self.is_activated = False

	def activate(self):
		"""
		Called at plugin activation.
		"""
		self.is_activated = True

	def deactivate(self):
		"""
		Called when the plugin is disabled.
		"""
		self.is_activated = False

