import abc
import os
import logging

from pluginbase import PluginBase

log = logging.getLogger(__name__)


plugin_base = PluginBase(package="qark.custom_plugins")


def get_plugin_source(category=None):
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plugins")

    if not category:
        try:
            return plugin_base.make_plugin_source(searchpath=[base_path])
        except Exception:
            log.exception("Failed to get all plugins. Is the file path to plugins %s correct?", base_path)
            raise SystemExit("Failed to get all plugins. Is the file path correct?")
    else:
        try:
            return plugin_base.make_plugin_source(searchpath=[os.path.join(base_path, category)])
        except Exception:
            log.exception("Failed to get all plugins. Is the file path to plugins %s correct?",
                          os.path.join(base_path, category))
            raise SystemExit("Failed to get all plugins. Is the file path correct?")


def get_plugins(category=None):
    return get_plugin_source(category=category).list_plugins()


class BasePlugin(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, category=None, issue_name=None, description=None):
        self.category = category
        self.issues = set()
        self.issue_name = issue_name
        self.description = description

    @abc.abstractmethod
    def run(self, file_object):
        pass
