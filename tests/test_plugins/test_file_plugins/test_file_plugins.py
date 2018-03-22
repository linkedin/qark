from qark.plugins.file.file_permissions import FilePermissions, WORLD_READABLE_DESCRIPTION, WORLD_WRITEABLE_DESCRIPTION
from qark.plugins.file.external_storage import ExternalStorage
from qark.plugins.file.api_keys import JavaAPIKeys
from qark.issue import Severity

import os
import tempfile


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


def test_external_storage(test_java_files):
    plugin = ExternalStorage()
    plugin.run([os.path.join(test_java_files,
                             "external_storage.java")])
    assert 4 == len(plugin.issues)

    
def test_api_keys():
    plugin = JavaAPIKeys()
    with tempfile.NamedTemporaryFile(mode="w", prefix="vuln1", suffix=".java") as vulnerable_file:
        with tempfile.NamedTemporaryFile(mode="w", prefix="vuln2", suffix=".java") as nonvulnerable_file:
            nonvulnerable_file.write("""public static final String API_TOKEN = "1234thisisaninvalidapitoken937235""")
            vulnerable_file.write("""public static final String API_TOKEN = "Nti4kWY-qRHTYq3dsbeip0P1tbGCzs2BAY163ManCAb""")
            nonvulnerable_file.seek(0)
            vulnerable_file.seek(0)

            plugin.run([nonvulnerable_file.name,
                        vulnerable_file.name])
            assert 1 == len(plugin.issues)
