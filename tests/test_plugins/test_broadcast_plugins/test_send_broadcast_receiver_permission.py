from qark.plugins.broadcast.send_broadcast_receiver_permission import SendBroadcastReceiverPermission

import os
import shutil


def test_send_broadcast_receiver_permission(decompiler, build_directory, vulnerable_broadcast_path):
    # set the path to manifest file
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    decompiler._run_dex2jar()
    decompiler.run_apktool()
    decompiler.decompile()

    plugin = SendBroadcastReceiverPermission()
    files = []
    for (dir_path, dir_names, file_names) in os.walk(build_directory):
        for file_name in file_names:
            files.append(os.path.join(dir_path, file_name))
    plugin.run(files)

    assert len(plugin.issues) == 2  # vulnerable APK
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = SendBroadcastReceiverPermission()
    plugin.run([vulnerable_broadcast_path])
    assert len(plugin.issues) == 8
