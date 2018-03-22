from qark.plugins.generic.check_permissions import CheckPermissions

import os


def test_check_permissions(test_java_files):
    plugin = CheckPermissions()
    plugin.run([os.path.join(test_java_files,
                             "check_permissions.java")])
    assert 2 == len(plugin.issues)
