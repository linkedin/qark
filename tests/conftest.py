from __future__ import absolute_import

import pytest

import os

from qark.decompiler.decompiler import Decompiler
from qark.scanner.scanner import Scanner
from qark.scanner.plugin import JavaASTPlugin, ManifestPlugin


DECOMPILER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "qark", "lib", "decompilers")


@pytest.fixture(scope="session")
def path_to_source():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "goatdroid.apk")


@pytest.fixture(scope="session")
def build_directory():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_directory")


@pytest.fixture()
def decompiler(path_to_source, build_directory):
    return Decompiler(path_to_source=path_to_source, build_directory=build_directory)


@pytest.fixture(scope="module")
def module_decompiler(path_to_source, build_directory):
    return Decompiler(path_to_source=path_to_source, build_directory=build_directory)



@pytest.fixture()
def scanner(decompiler):
    return Scanner(decompiler.manifest_path, decompiler.build_directory)


@pytest.fixture(scope="session")
def vulnerable_manifest_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_xml_files",
                        "test_androidmanifest.xml")


@pytest.fixture(scope="session")
def goatdroid_manifest_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_xml_files",
                        "test_goatdroid_manifest.xml")


@pytest.fixture(scope="session")
def test_java_files():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_java_files")


@pytest.fixture(scope="session")
def vulnerable_broadcast_path(test_java_files):
    return os.path.join(test_java_files,
                        "send_broadcast_receiver_permission.java")


@pytest.fixture(scope="session")
def vulnerable_receiver_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_plugins", "test_manifest_plugins",
                        "broadcastreceivers", "SendSMSNowReceiver.java")


@pytest.fixture(autouse=True)
def reset_plugins():
    """Reset all plugins in between each function. `JavaASTPlugin` currently will reset every other plugin type."""
    JavaASTPlugin.reset()

    ManifestPlugin.manifest_xml = None
    ManifestPlugin.manifest_path = None
    ManifestPlugin.min_sdk = -1
    ManifestPlugin.target_sdk = -1
    ManifestPlugin.package_name = "PACKAGE_NOT_FOUND"
