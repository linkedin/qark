import abc
import os
import logging

from pluginbase import PluginBase

log = logging.getLogger(__name__)


plugin_base = PluginBase(package="qark.custom_plugins")

# plugin modules to blacklist, `helpers` should always be blacklisted as it is not a plugin
BLACKLISTED_PLUGIN_MODULES = {"helpers"}


def get_plugin_source(category=None):
    """
    Returns a `PluginBase.PluginSource` based on the `category`.
    :param category: plugin category, subdirectory under `plugins/`
    :return: `PluginBase.PluginSource`
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plugins")
    if category is not None:
        path = os.path.join(path, category)

    try:
        return plugin_base.make_plugin_source(searchpath=[path])
    except Exception:
        log.exception("Failed to get all plugins. Is the file path to plugins %s correct?", path)
        raise SystemExit("Failed to get all plugins. Is the file path correct?")


def get_plugins(category=None):
    """
    Returns all plugins defined by a `category` and removes plugins defined in ``BLACKLISTED_PLUGIN_MODULES``.

    :param category: plugin category, subdirectory under `plugins/`
    :return: modules for that category
    :rtype: list
    """
    plugins = get_plugin_source(category=category).list_plugins()

    return [plugin for plugin in plugins if plugin not in BLACKLISTED_PLUGIN_MODULES]


class BasePlugin(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, category=None, name=None, description=None):
        self.category = category
        self.issues = []
        self.name = name
        self.description = description

    @abc.abstractmethod
    def run(self, files, apk_constants=None):
        """
        Method to be called for each plugin to add issues.

        :param List[str] files: a list of files gathered by `Scanner` as absolute paths
        :param dict apk_constants: dictionary containing extra information
                                    that some plugins can use (min_sdk, target_sdk)
        """
        pass
