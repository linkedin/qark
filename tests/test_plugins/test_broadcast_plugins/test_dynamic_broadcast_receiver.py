import os

import javalang

from qark.plugins.broadcast.dynamic_broadcast_receiver import DynamicBroadcastReceiver
from qark.scanner.plugin import ManifestPlugin


def test_vulnerable_dynamic_broadcast_receiver(test_java_files):
    plugin = DynamicBroadcastReceiver()
    path_to_vuln_file = os.path.join(test_java_files,
                                     "dynamic_broadcast_receiver.java")

    ManifestPlugin.min_sdk = 5
    plugin.update(file_path=path_to_vuln_file)
    plugin.run()

    assert len(plugin.issues) == 1  # vulnerable manifest
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category


def test_nonvulnerable_dynamic_broadcast_receiver(test_java_files):
    plugin = DynamicBroadcastReceiver()
    path_to_vuln_file = os.path.join(test_java_files,
                                     "dynamic_broadcast_receiver.java")
    plugin.update(file_path=path_to_vuln_file)
    ManifestPlugin.min_sdk = 14
    plugin.run()

    assert len(plugin.issues) == 0

