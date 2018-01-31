import pytest

import os

from qark.decompiler.decompiler import Decompiler
from qark.scanner.scanner import Scanner


@pytest.fixture(scope="session")
def path_to_apk():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "goatdroid.apk")


@pytest.fixture(scope="session")
def build_directory():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_directory")


@pytest.fixture()
def decompiler(path_to_apk, build_directory):
    return Decompiler(path_to_apk=path_to_apk, build_directory=build_directory)


@pytest.fixture()
def scanner(decompiler):
    return Scanner(decompiler=decompiler)


@pytest.fixture(scope="session")
def bad_decompiler():
    return Decompiler("1")


@pytest.fixture(scope="session")
def cfr_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib", "decompilers", "cfr_0_124.jar")


@pytest.fixture(scope="session")
def jdcore_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib",
                        "decompilers", "jd-core-java-1.2.jar")


@pytest.fixture(scope="session")
def procyon_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib",
                        "decompilers", "procyon-decompiler-0.5.30.jar")


@pytest.fixture(scope="session")
def vulnerable_manifest_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_androidmanifest.xml")


@pytest.fixture(scope="session")
def vulnerable_broadcast_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_java_files",
                        "send_broadcast_receiver_permission.java")
