from qark.plugins.generic.check_permissions import CheckPermissions

import os
import javalang


def test_check_permissions(test_java_files):
    plugin = CheckPermissions()
    path = os.path.join(test_java_files,
                        "check_permissions.java")
    with open(path) as f:
        contents = f.read()

    ast = javalang.parse.parse(contents)
    plugin.run(path, file_contents=contents, java_ast=ast)
    assert 2 == len(plugin.issues)
