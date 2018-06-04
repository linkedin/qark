import os

import javalang

from qark.plugins.broadcast.dynamic_broadcast_receiver import DynamicBroadcastReceiver


def test_vulnerable_dynamic_broadcast_receiver(test_java_files):
    plugin = DynamicBroadcastReceiver()
    path_to_vuln_file = os.path.join(test_java_files,
                                     "dynamic_broadcast_receiver.java")
    with open(path_to_vuln_file) as f:
        ast = javalang.parse.parse(f.read())

    plugin.run(path_to_vuln_file,
               java_ast=ast,
               apk_constants={"min_sdk": 5})

    assert len(plugin.issues) == 1  # vulnerable manifest
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category


def test_nonvulnerable_dynamic_broadcast_receiver(test_java_files):
    plugin = DynamicBroadcastReceiver()
    path_to_vuln_file = os.path.join(test_java_files,
                                     "dynamic_broadcast_receiver.java")
    with open(path_to_vuln_file) as f:
        ast = javalang.parse.parse(f.read())

    plugin.run(path_to_vuln_file,
               java_ast=ast,
               apk_constants={"min_sdk": 14})

    assert len(plugin.issues) == 0

