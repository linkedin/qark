import pytest

import os

from qark.decompiler.decompiler import Decompiler


@pytest.fixture(scope="session")
def path_to_apk():
    return "{}/goatdroid.apk".format(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def build_directory():
    return "{}/unzip_apk".format(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture()
def decompiler(path_to_apk, build_directory):
    return Decompiler(path_to_apk=path_to_apk, build_directory=build_directory)


@pytest.fixture(scope="session")
def bad_decompiler():
    return Decompiler("1")


@pytest.fixture(scope="session")
def cfr_path():
    return "{}/../../lib/decompilers/cfr_0_124.jar".format(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def jdcore_path():
    return "{}/../../lib/decompilers/jd-core-java-1.2.jar".format(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def procyon_path():
    return "{}/../../lib/decompilers/procyon-decompiler-0.5.30.jar".format(os.path.dirname(os.path.abspath(__file__)))
