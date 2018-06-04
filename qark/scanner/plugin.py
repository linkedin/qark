import abc
import os
import logging
from xml.dom import minidom

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
        return plugin_base.make_plugin_source(searchpath=[path], persist=True)
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

    def __init__(self, name, category, description=None, **kwargs):
        self.category = category
        self.name = name
        self.description = description

        super(BasePlugin, self).__init__(**kwargs)

        self.issues = []

    @abc.abstractmethod
    def run(self, file, **kwargs):
        """
        Method to be called for each plugin to add issues.

        :param List[str] files: a list of files gathered by `Scanner` as absolute paths
        :param dict apk_constants: dictionary containing extra information
                                    that some plugins can use (min_sdk, target_sdk)
        """
        pass


class ManifestPlugin(BasePlugin):
    manifest_xml = None
    manifest_path = None

    def __init__(self, manifest_path=None, manifest_xml=None, **kwargs):
        if self.manifest_path is None:
            self.manifest_path = manifest_path

        if self.manifest_xml is None:
            try:
                # If the user passed the parsed minidom XML content then we don't have to parse anything
                self.manifest_xml = manifest_xml

            except KeyError:

                # Otherwise we have to get the manifest path and parse it
                try:
                    self.manifest_xml = minidom.parse(self.manifest_path)

                except Exception:
                    log.debug("Failed to parse the XML file, resetting manifest_path")
                    self.manifest_path = None

        super(ManifestPlugin, self).__init__(**kwargs)

    @classmethod
    def update_manifest(cls, path_to_manifest):
        """Users of this class should call this method instead of changing class attributes directly"""
        cls.manifest_path = path_to_manifest
        try:
            cls.manifest_xml = minidom.parse(path_to_manifest)
        except Exception:
            # path_to_manifest is None or has bad XML
            cls.manifest_xml = None

    @abc.abstractmethod
    def run(self, files, apk_constants=None):
        """User should define how their plugin runs"""
