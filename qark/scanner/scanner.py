import logging
from os import (
    walk,
    path
)

from qark.plugins.helpers import get_min_sdk, get_target_sdk
from qark.scanner.plugin import get_plugin_source, get_plugins

log = logging.getLogger(__name__)


class Scanner(object):
    __instance = None

    def __new__(cls, decompiler):
        if Scanner.__instance is None:
            Scanner.__instance = object.__new__(cls)
            Scanner.__instance.files = set()
            Scanner.__instance.issues = set()

        Scanner.__instance.decompiler = decompiler
        return Scanner.__instance

    def __init__(self, decompiler):
        """
        Creates the scanner.
        :param Decompiler decompiler: the decompiler class that contains decompiled path information
        """
        self.decompiler = decompiler
        if self.decompiler.manifest_path is None:
            self.decompiler.manifest_path = self.decompiler.run_apktool()

    def run(self):
        """
        Runs all the plugin checks by category.
        """
        self._gather_files()
        self._run_manifest_checks()

    def _run_manifest_checks(self):
        """
        Runs all plugins under `qark.plugins.manifest` and updates `self.issues` with their findings.
        """
        plugin_source = get_plugin_source(category="manifest")
        for plugin_name in get_plugins(category="manifest"):
            try:
                plugin = plugin_source.load_plugin(plugin_name).plugin
            except Exception:
                log.exception("Error loading plugin %s... continuing with next plugin", plugin_name)
                continue

            try:
                plugin.run(files=self.files, extras={"minimum_sdk": get_min_sdk(self.decompiler.manifest_path),
                                                     "target_sdk": get_target_sdk(self.decompiler.manifest_path)})
            except Exception:
                log.exception("Error running plugin %s... continuing with next plugin", plugin_name)
                continue

            self.issues.update(plugin.issues)

    def _gather_files(self):
        """
        Walks the `Decompiler.build_directory` and updates the `self.files` set with new files.
        :return:
        """
        try:
            for (dir_path, dir_names, file_names) in walk(self.decompiler.build_directory):
                for file_name in file_names:
                    self.files.add(path.join(dir_path, file_name))
        except AttributeError:
            log.debug("Decompiler does not have a build directory")
