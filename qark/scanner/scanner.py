from __future__ import absolute_import

import logging
from os import (
    walk,
    path
)

from qark.scanner.plugin import CoroutinePlugin
from qark.scanner.plugin import JavaASTPlugin
from qark.scanner.plugin import ManifestPlugin
from qark.scanner.plugin import PluginObserver
from qark.scanner.plugin import get_plugin_source, get_plugins
from qark.utils import is_java_file

log = logging.getLogger(__name__)

PLUGIN_CATEGORIES = ("manifest", "broadcast", "file", "crypto", "intent", "cert", "webview", "generic")


class Scanner(object):

    def __init__(self, manifest_path, path_to_source):
        """
        Creates the scanner.

        :param str manifest_path: the path to the manifest file
        :param str path_to_source: the path to the source code
        """
        self.files = set()
        self.issues = []
        self.manifest_path = manifest_path

        self.path_to_source = path_to_source

        self._gather_files()

    def run(self):
        """
        Runs all the plugin checks by category.
        """
        plugins = []
        for category in PLUGIN_CATEGORIES:
            plugin_source = get_plugin_source(category=category)

            if category == "manifest":
                # Manifest plugins only need to run once, so we run them and continue
                manifest_plugins = get_plugins(category)
                ManifestPlugin.update_manifest(self.manifest_path)
                if ManifestPlugin.manifest_xml is not None:

                    for plugin in [plugin_source.load_plugin(plugin_name).plugin for plugin_name in manifest_plugins]:
                        # Give more detail to the ExportedTags manifest plugin as it is important for building the exploit
                        #   APK. Careful!
                        plugin.all_files = self.files

                        plugin.run()
                        self.issues.extend(plugin.issues)
                    continue

            for plugin_name in get_plugins(category):
                plugins.append(plugin_source.load_plugin(plugin_name).plugin)

        self._run_checks(plugins)

    def _run_checks(self, plugins):
        """Run all the plugins (besides manifest) on every file."""
        current_file_subject = Subject()
        plugins = list(observer_plugin for observer_plugin in plugins if isinstance(observer_plugin, PluginObserver))
        coroutine_plugins = list(coroutine_plugin for coroutine_plugin in plugins if isinstance(coroutine_plugin,
                                                                                                CoroutinePlugin))

        for plugin in plugins:
            current_file_subject.register(plugin)

        for filepath in self.files:
            # This call will run all non-coroutine plugins, and also update the shared class variables
            current_file_subject.notify(filepath)

            # This will efficiently run all coroutine plugins
            notify_coroutines(coroutine_plugins)

            # reset the plugin file data to None as we are done processing the file
            current_file_subject.reset()

        for plugin in plugins:
            self.issues.extend(plugin.issues)

    def _gather_files(self):
        """Walks the `path_to_source` and updates the `self.files` set with new files."""
        if is_java_file(self.path_to_source):
            self.files.add(self.path_to_source)
            log.debug("Added single java file to scanner")
            return

        log.debug("Adding files to scanner...")
        try:
            for (dir_path, _, file_names) in walk(self.path_to_source):
                for file_name in file_names:
                    self.files.add(path.join(dir_path, file_name))
        except AttributeError:
            log.debug("Decompiler does not have a build directory")


class Subject(object):
    """"""

    def __init__(self):
        self.observers = []

    def register(self, observer):
        """
        :param PluginObserver observer:
        """
        self.observers.append(observer)

    def unregister(self, observer):
        """
        :param PluginObserver observer:
        """
        self.observers.remove(observer)

    def notify(self, file_path):
        for observer in self.observers:
            observer.update(file_path, call_run=True)

    def reset(self):
        for observer in self.observers:
            observer.reset()


def notify_coroutines(coroutine_plugins):
    """Prime and run the coroutine plugins that are passed in.

    Coroutines run differently than normal plugins as they will all only iterate over the AST once. This is a much
    more efficient way of running plugins in terms of speed, and memory.
    """
    # Run all coroutine plugins
    if JavaASTPlugin.java_ast is not None:
        coroutines_to_run = []

        # Prime coroutines that can run
        for plugin in coroutine_plugins:
            if plugin.can_run_coroutine():
                coroutines_to_run.append(plugin.prime_coroutine())

        for path, node in JavaASTPlugin.java_ast:
            for coroutine in coroutines_to_run:
                coroutine.send((path, node))
