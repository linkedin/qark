from qark.plugins.broadcast.send_broadcast_receiver_permission import SendBroadcastReceiverPermission

import javalang


def test_send_broadcast_receiver_permission(vulnerable_broadcast_path):
    with open(vulnerable_broadcast_path) as f:
        contents = f.read()

    ast = javalang.parse.parse(contents)

    plugin = SendBroadcastReceiverPermission()
    plugin.run(vulnerable_broadcast_path,
               java_ast=ast,
               file_contents=contents,
               apk_constants={"min_sdk": 25})
    assert 8 == len(plugin.issues)
