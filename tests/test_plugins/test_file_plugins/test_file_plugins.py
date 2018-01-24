from qark.plugins.file.file_permissions import FilePermissions, WORLD_READABLE_DESCRIPTION, WORLD_WRITEABLE_DESCRIPTION
from qark.issue import Severity

import os


def test_file_permissions():
    plugin = FilePermissions()
    plugin.run([os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_file_permissions.java")],
               apk_constants={})
    assert len(plugin.issues) == 2
    assert "World readable file" == plugin.issues[0].name
    assert Severity.WARNING == plugin.issues[0].severity
    assert WORLD_READABLE_DESCRIPTION == plugin.issues[0].description
    assert "World writeable file" == plugin.issues[1].name
    assert Severity.WARNING == plugin.issues[1].severity
    assert WORLD_WRITEABLE_DESCRIPTION == plugin.issues[1].description

