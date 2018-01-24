from qark.plugins.broadcast.send_broadcast_receiver_permission import SendBroadcastReceiverPermission

import os
import shutil


def test_send_broadcast_receiver_permission(build_directory, vulnerable_broadcast_path):
    # set the path to manifest file
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = SendBroadcastReceiverPermission()
    plugin.run([vulnerable_broadcast_path])
    assert len(plugin.issues) == 8
