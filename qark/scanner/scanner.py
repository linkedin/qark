from __future__ import absolute_import

import logging
from os import (
    walk,
    path
)

import javalang
from qark.plugins.manifest_helpers import get_min_sdk, get_target_sdk
from qark.scanner.plugin import get_plugin_source, get_plugins
from qark.scanner.plugin import ManifestPlugin
from qark.xml_helpers import get_manifest_out_of_files

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

        plugins = []
        for category in PLUGIN_CATEGORIES:
            plugin_source = get_plugin_source(category=category)

            for plugin_name in get_plugins(category):
                plugins.append(plugin_source.load_plugin(plugin_name).plugin)

        self._run_checks(plugins)

    def _run_checks(self, plugins):
        try:
            min_sdk = get_min_sdk(self.manifest_path, files=self.files)
            target_sdk = get_target_sdk(self.manifest_path, files=self.files)
        except AttributeError:
            # manifest path is not set, assume min_sdk and target_sdk
            min_sdk = target_sdk = 1

        for filepath in self.files:
            ast = None

            try:
                with open(filepath, 'r') as f:
                    file_contents = f.read()
            except Exception:
                log.exception("Unable to read file %s", filepath)
                file_contents = None

            if file_contents and filepath.lower().endswith(".java"):
                try:
                    ast = javalang.parse.parse(file_contents)
                except (javalang.parser.JavaSyntaxError, IndexError):
                    log.debug("Unable to parse AST for file %s", filepath)

            for plugin in plugins:
                log.debug("Running plugin %s", plugin)
                plugin.run(filepath, apk_constants={"min_sdk": min_sdk,
                                                    "target_sdk": target_sdk},
                           java_ast=ast,
                           file_contents=file_contents,
                           all_files=self.files)

                self.issues.extend(plugin.issues)

    def _gather_files(self):
        """
        Walks the `Decompiler.build_directory` and updates the `self.files` set with new files.
        :return:
        """
        if path.splitext(self.path_to_source.lower())[1] == ".java":
            self.files.add(self.path_to_source)
            return

        try:
            for (dir_path, _, file_names) in walk(self.build_directory):
                for file_name in file_names:
                    self.files.add(path.join(dir_path, file_name))
        except AttributeError:
            log.debug("Decompiler does not have a build directory")

        # Set the manifest path if it doesn't exist (we are walking a Java source code directory)
        if not self.manifest_path:
            self.manifest_path = get_manifest_out_of_files(self.files)
