from qark.plugins.generic.check_permissions import CheckPermissions

import os


def test_check_permissions(test_java_files):
    plugin = CheckPermissions()
    path = os.path.join(test_java_files,
                        "check_permissions.java")
    plugin.update(file_path=path)
    plugin.run()
    assert 2 == len(plugin.issues)
