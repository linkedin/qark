from __future__ import absolute_import

import logging
from os import (
    walk,
    path
)

from qark.plugins.manifest_helpers import get_min_sdk, get_target_sdk
from qark.scanner.plugin import get_plugin_source, get_plugins
from qark.scanner.plugin import ManifestPlugin

log = logging.getLogger(__name__)

PLUGIN_CATEGORIES = ("manifest", "broadcast", "file", "crypto", "intent", "cert", "webview", "generic")


class Scanner(object):

    def __init__(self, manifest_path, path_to_source, build_directory):
        """
        Creates the scanner.

        :param str manifest_path: the path to the manifest file
        :param str path_to_source: the path to the source code
        :param str build_directory: the path to the build directory
        """
        self.files = set()
        self.issues = []
        self.manifest_path = manifest_path

        # Manifest plugins should be able to retrieve the manifest xml directly
        ManifestPlugin.update_manifest(manifest_path)

        self.path_to_source = path_to_source
        self.build_directory = build_directory

    def run(self):
        """
        Runs all the plugin checks by category.
        """
        self._gather_files()
        for category in PLUGIN_CATEGORIES:
            self._run_checks(category=category)

    def _run_checks(self, category):
        """
        Runs all plugins under `qark.plugins.category` and updates `self.issues` with their findings.
        """
        plugin_source = get_plugin_source(category=category)
        try:
            min_sdk = get_min_sdk(self.manifest_path, files=self.files)
            target_sdk = get_target_sdk(self.manifest_path, files=self.files)
        except AttributeError:
            # manifest path is not set, assume min_sdk and target_sdk
            min_sdk = target_sdk = 1

        for plugin_name in get_plugins(category=category):
            try:
                plugin = plugin_source.load_plugin(plugin_name).plugin
            except Exception:
                log.exception("Error loading plugin %s... continuing with next plugin", plugin_name)
                continue

            try:
                plugin.run(files=self.files, apk_constants={"minimum_sdk": min_sdk,
                                                            "target_sdk": target_sdk})
            except Exception:
                log.exception("Error running plugin %s... continuing with next plugin", plugin_name)
                continue

            self.issues.extend(plugin.issues)

    def _gather_files(self):
        """
        Walks the `Decompiler.build_directory` and updates the `self.files` set with new files.
        :return:
        """
        if path.splitext(self.path_to_source.lower())[1] == ".java":
            self.files.add(self.path_to_source)
            return

        walk_directory = self.build_directory
        try:
            for (dir_path, _, file_names) in walk(walk_directory):
                for file_name in file_names:
                    self.files.add(path.join(dir_path, file_name))
        except AttributeError:
            log.debug("Decompiler does not have a build directory")
