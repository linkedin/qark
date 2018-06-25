from qark.plugins.file.file_permissions import FilePermissions, WORLD_READABLE_DESCRIPTION, WORLD_WRITEABLE_DESCRIPTION
from qark.plugins.file.phone_identifier import PhoneIdentifier
from qark.plugins.file.insecure_functions import InsecureFunctions
from qark.plugins.file.http_url_hardcoded import HardcodedHTTP
from qark.plugins.file.android_logging import AndroidLogging
from qark.plugins.file.external_storage import ExternalStorage
from qark.plugins.file.api_keys import JavaAPIKeys
from qark.issue import Severity

import javalang

import os


def test_file_permissions():
    plugin = FilePermissions()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_file_permissions.java")
    plugin.update(file_path=path)

    plugin.run()
    assert len(plugin.issues) == 2
    assert "World readable file" == plugin.issues[0].name
    assert Severity.WARNING == plugin.issues[0].severity
    assert WORLD_READABLE_DESCRIPTION == plugin.issues[0].description
    assert "World writeable file" == plugin.issues[1].name
    assert Severity.WARNING == plugin.issues[1].severity
    assert WORLD_WRITEABLE_DESCRIPTION == plugin.issues[1].description


def test_phone_identifier(test_java_files):
    plugin = PhoneIdentifier()
    path = os.path.join(test_java_files,
                        "phone_identifier.java")
    plugin.update(file_path=path)
    plugin.run()
    assert 1 == len(plugin.issues)


def test_insecure_functions(test_java_files):
    plugin = InsecureFunctions()
    path = os.path.join(test_java_files,
                        "insecure_functions.java")

    plugin.update(file_path=path)
    plugin.run()
    assert 1 == len(plugin.issues)


def test_http_url_hardcoded(test_java_files):
    plugin = HardcodedHTTP()
    path = os.path.join(test_java_files,
                        "http_url_hardcoded.java")
    plugin.update(file_path=path)
    plugin.run()

    assert 1 == len(plugin.issues)


def test_android_logging(test_java_files):
    plugin = AndroidLogging()
    path = os.path.join(test_java_files,
                        "test_android_logging.java")
    plugin.update(file_path=path)
    plugin.run()
    assert 2 == len(plugin.issues)
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category


def test_external_storage(test_java_files):
    plugin = ExternalStorage()
    path = os.path.join(test_java_files,
                        "external_storage.java")
    plugin.update(file_path=path)

    plugin.run()
    assert 4 == len(plugin.issues)


def test_api_keys():
    plugin = JavaAPIKeys()
    JavaAPIKeys.file_contents = """public static final String API_TOKEN = "1234thisisaninvalidapitoken937235"""
    JavaAPIKeys.file_path = "path"
    plugin.run()
    assert 0 == len(plugin.issues)
    plugin.reset()
    JavaAPIKeys.file_contents = """public static final String API_TOKEN = "Nti4kWY-qRHTYq3dsbeip0P1tbGCzs2BAY163ManCAb"""
    JavaAPIKeys.file_path = "path"
    plugin.run()
    assert 1 == len(plugin.issues)
