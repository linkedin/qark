from __future__ import absolute_import

import logging
from os import (
    walk,
    path
)

from qark.manifest_helpers import get_min_sdk, get_target_sdk
from qark.scanner.plugin import get_plugin_source, get_plugins
from qark import manifest_helpers

log = logging.getLogger(__name__)


PLUGIN_CATEGORIES = ("manifest", "broadcast", "file", "crypto", "intent", "cert", "webview")


class Scanner(object):
    __instance = None

    def __new__(cls, decompiler):
        if Scanner.__instance is None:
            Scanner.__instance = object.__new__(cls)
            Scanner.__instance.files = set()
            Scanner.__instance.issues = []

        Scanner.__instance.decompiler = decompiler
        return Scanner.__instance

    def __init__(self, decompiler):
        """
        Creates the scanner.
        :param Decompiler decompiler: the decompiler class that contains decompiled path information
        """
        self.decompiler = decompiler

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
            min_sdk = get_min_sdk(self.decompiler.manifest_path, files=self.files)
            target_sdk = get_target_sdk(self.decompiler.manifest_path, files=self.files)
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
                plugin.run(files=self.files, apk_constants={"min_sdk": min_sdk,
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
        if path.splitext(self.decompiler.path_to_source.lower())[1] == ".java":
            self.files.add(self.decompiler.path_to_source)
            return

        try:
            for (dir_path, _, file_names) in walk(self.decompiler.build_directory):
                for file_name in file_names:
                    self.files.add(path.join(dir_path, file_name))
        except AttributeError:
            log.debug("Decompiler does not have a build directory")
