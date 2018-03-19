import abc
import os
import logging
from xml.dom import minidom

from pluginbase import PluginBase

log = logging.getLogger(__name__)


plugin_base = PluginBase(package="qark.custom_plugins")


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
    Returns all plugins defined by a `category`. TODO: implement blacklisting in this method
    :param category: plugin category, subdirectory under `plugins/`
    :return: modules for that category
    :rtype: list
    """
    return get_plugin_source(category=category).list_plugins()


class Base(object):
    def __init__(self, **kwargs):
        pass


class BasePlugin(Base):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.category = kwargs.get('category')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')

        self.issues = []

        super(BasePlugin, self).__init__(**kwargs)

    @abc.abstractmethod
    def run(self, files, apk_constants=None):
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

    def __init__(self, **kwargs):
        if self.manifest_path is None:
            self.manifest_path = kwargs.get("manifest_path")

        if self.manifest_xml is None:
            try:
                # If the user passed the parsed minidom XML content then we don't have to parse anything
                self.manifest_xml = kwargs["manifest_xml"]

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
        cls.manifest_xml = minidom.parse(path_to_manifest)

    @abc.abstractmethod
    def run(self, files, apk_constants=None):
        """User should define how their plugin runs"""
