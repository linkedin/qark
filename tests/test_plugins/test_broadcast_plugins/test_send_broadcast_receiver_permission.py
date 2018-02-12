from qark.plugins.broadcast.send_broadcast_receiver_permission import SendBroadcastReceiverPermission


def test_send_broadcast_receiver_permission(vulnerable_broadcast_path):
    plugin = SendBroadcastReceiverPermission()
    plugin.run([vulnerable_broadcast_path])
    assert len(plugin.issues) == 8
