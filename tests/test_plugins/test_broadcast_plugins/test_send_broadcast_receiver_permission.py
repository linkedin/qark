from qark.plugins.broadcast.send_broadcast_receiver_permission import SendBroadcastReceiverPermission
from qark.scanner.plugin import ManifestPlugin


def test_send_broadcast_receiver_permission(vulnerable_broadcast_path):
    ManifestPlugin.min_sdk = 25
    plugin = SendBroadcastReceiverPermission()
    plugin.update(file_path=vulnerable_broadcast_path)
    plugin.run()
    assert 8 == len(plugin.issues)
