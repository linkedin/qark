import logging

from qark.scanner.plugin import get_plugin_source

log = logging.getLogger(__name__)


class Scanner(object):
    __instance = None

    def __new__(cls, decompiler):
        if Scanner.__instance is None:
            Scanner.__instance = object.__new__(cls)
        Scanner.__instance.decompiler = decompiler
        return Scanner.__instance

    def __init__(self, decompiler):
        """
        Creates the scanner.
        :param Decompiler decompiler: the decompiler class that contains decompiled path information
        """
        self.decompiler = decompiler
        self.issues = set()

    def run(self):
        """
        Runs all the plugin checks by category.
        :return:
        """
        self._run_manifest_checks()

    def _run_manifest_checks(self):
        """
        Runs all plugins under `qark.plugins.manifest` and updates `self.issues` with their findings.
        """
        plugin_source = get_plugin_source(category="manifest")
        if not self.decompiler.manifest_path:
            self.decompiler.manifest_path = self.decompiler.run_apktool()

        for plugin_name in plugin_source.list_plugins():
            try:
                plugin = plugin_source.load_plugin(plugin_name).plugin
            except Exception:
                log.exception("Error loading plugin %s... continuing with next plugin", plugin_name)
                continue

            plugin.run(self.decompiler.manifest_path)
            self.issues.update(plugin.issues)
