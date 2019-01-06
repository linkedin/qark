import abc
import logging
import os
from xml.dom import minidom

import javalang
from pluginbase import PluginBase

from qark.plugins.manifest_helpers import get_min_sdk, get_target_sdk, get_package_from_manifest
from qark.utils import is_java_file

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
    def run(self):
        """
        Method to be called for each plugin to add issues.

        :param List[str] files: a list of files gathered by `Scanner` as absolute paths
        :param dict apk_constants: dictionary containing extra information
                                    that some plugins can use (min_sdk, target_sdk)
        """
        raise NotImplementedError()


class PluginObserver(BasePlugin):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        """For plugins to implement."""

    @abc.abstractmethod
    def reset(self):
        """Clear any class attributes that were set for the file."""


class FilePathPlugin(PluginObserver):
    """Subclass this plugin if your plugin needs action based on a new file path."""
    __metaclass__ = abc.ABCMeta

    file_path = None
    has_been_set = False

    def update(self, file_path, call_run=False):
        """
        :param str file_path:
        :param bool call_run: Whether or not `self.run()` should be called. Prevents `run()` being called multiple times
        """
        if not file_path:
            FilePathPlugin.file_path = None
            return

        if not self.has_been_set:
            FilePathPlugin.file_path = file_path
            FilePathPlugin.has_been_set = True

        if call_run:
            self.run()

    @classmethod
    def reset(cls):
        FilePathPlugin.file_path = None
        FilePathPlugin.has_been_set = False


class FileContentsPlugin(FilePathPlugin):
    """Subclass this plugin if your plugin needs to operate on file contents and no other plugin type suffices."""
    __metaclass__ = abc.ABCMeta

    file_contents = None
    readable = True

    def update(self, file_path, call_run=False):
        """
        If `file_contents` is None, then the file has not been read yet, and we must set it.
        If the file is not able to be read then we set a flag telling other plugins to not try to operate on it.
        """
        if not self.readable:
            return

        if self.file_contents is None:
            # Make sure the file path has been set.
            super(FileContentsPlugin, self).update(file_path)

            try:
                with open(self.file_path, "r") as f:
                    FileContentsPlugin.file_contents = f.read()

            except IOError:
                log.debug("Unable to operate on file %s for reading", self.file_path)
                FileContentsPlugin.readable = False
                FileContentsPlugin.file_contents = None
                return

            except UnicodeDecodeError:
                # Try to read file in ISO-8859-1 encoding, used for png, xml, webp, some other resource files etc
                try:
                    with open(self.file_path, "r", encoding="ISO-8859-1") as f:
                        FileContentsPlugin.file_contents = f.read()

                except Exception:
                    # Give up on the file
                    log.debug("Unable to operate on file %s", self.file_path)
                    FileContentsPlugin.readable = False
                    FileContentsPlugin.file_contents = None
                    return

        if call_run and self.file_contents is not None:
            self.run()

    @classmethod
    def reset(cls):
        FileContentsPlugin.file_contents = None
        FileContentsPlugin.readable = True

        super(FileContentsPlugin, cls).reset()


class JavaASTPlugin(FileContentsPlugin):
    __metaclass__ = abc.ABCMeta

    java_ast = None
    parseable = True

    def update(self, file_path, call_run=False):
        if not self.parseable:
            return

        if self.java_ast is None and is_java_file(file_path):
            # Make sure the file contents have been set
            super(JavaASTPlugin, self).update(file_path, call_run=False)

            if self.file_contents:
                try:
                    JavaASTPlugin.java_ast = javalang.parse.parse(self.file_contents)
                except (javalang.parser.JavaSyntaxError, IndexError):
                    log.debug("Unable to parse AST for file %s", self.file_path)
                    JavaASTPlugin.java_ast = None
                    JavaASTPlugin.parseable = False
                    return

        if call_run and self.java_ast is not None:
            try:
                self.run()
            except Exception:
                log.exception("Unable to run plugin")

    @classmethod
    def reset(cls):
        JavaASTPlugin.java_ast = None
        JavaASTPlugin.parseable = True

        super(JavaASTPlugin, cls).reset()


class CoroutinePlugin(JavaASTPlugin):
    """A JavaASTPlugin that runs as a coroutine.

    Much more efficient than normal JavaASTPlugins.
    """

    def can_run_coroutine(self):
        """Whether or not the coroutine should run."""
        return True

    def run(self):
        """Method to run a given coroutine against the AST.

        Used for testing plugins individually and should not be run with multiple plugins (sequentially).
        Included as a backwards-compatiable way to run plugins without breaking Liskov substitution.
        """
        if self.can_run_coroutine():
            coroutine = self.prime_coroutine()
            for path, node in self.java_ast:
                coroutine.send((path, node))

    def prime_coroutine(self):
        """Return the primed coroutine if available."""
        coroutine = self.run_coroutine()
        next(coroutine)
        return coroutine

    @abc.abstractmethod
    def run_coroutine(self):
        """User should define how their plugin runs"""

    def update(self, file_path, call_run=False):
        """Updates the AST information but does not attempt to run since that is handled by the scanner."""
        super(CoroutinePlugin, self).update(file_path)


class ManifestPlugin(BasePlugin):
    __metaclass__ = abc.ABCMeta

    manifest_xml = None
    manifest_path = None
    min_sdk = -1
    target_sdk = -1
    package_name = "PACKAGE_NOT_FOUND"

    @classmethod
    def update_manifest(cls, path_to_manifest):
        """Users of this class should call this method instead of changing class attributes directly"""
        cls.manifest_path = path_to_manifest
        try:
            cls.manifest_xml = minidom.parse(path_to_manifest)
        except Exception:
            # path_to_manifest is None or has bad XML
            cls.manifest_xml = None
            log.debug("Failed to update manifest for file %s", path_to_manifest)
            return

        try:
            cls.min_sdk = get_min_sdk(cls.manifest_path)
            cls.target_sdk = get_target_sdk(cls.manifest_path)
        except AttributeError:
            # manifest path is not set, assume min_sdk and target_sdk
            cls.min_sdk = cls.target_sdk = 1

        try:
            cls.package_name = get_package_from_manifest(cls.manifest_path)
        except IOError:
            cls.package_name = "PACKAGE_NOT_FOUND"

    @abc.abstractmethod
    def run(self):
        """User should define how their plugin runs"""
