import os
import shutil

import pytest

from qark.decompiler import decompiler
from qark.decompiler.decompiler import Decompiler
from qark.decompiler.external_decompiler import CFR, Procyon, Fernflower


def test_unzip_file(path_to_source, build_directory):
    decompiler.unzip_file(path_to_source, destination_to_unzip=build_directory)

    with pytest.raises(SystemExit):
        decompiler.unzip_file("1")

    shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)


def test_get_java_version():
    java_version = decompiler.get_java_version()
    assert not java_version.startswith('"')
    assert not java_version.endswith('"')


def test_unpack_apk(decompiler):
    classes_dex_path = os.path.join(decompiler.build_directory, "classes.dex")
    assert classes_dex_path == decompiler._unpack_apk()
    assert os.path.isfile(classes_dex_path)

    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)

    with pytest.raises(ValueError):
        bad_decompiler = Decompiler("1")
        bad_decompiler._unpack_apk()


def test_run_apktool(decompiler):
    if os.path.exists(decompiler.build_directory):
        shutil.rmtree(decompiler.build_directory)

    decompiler.run_apktool()
    assert os.path.isdir(decompiler.build_directory)
    assert os.path.isfile(os.path.join(decompiler.build_directory, "AndroidManifest.xml"))

    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)


def test_run_dex2jar(decompiler):
    if os.path.exists(decompiler.build_directory):
        shutil.rmtree(decompiler.build_directory)

    decompiler.dex_path = decompiler._unpack_apk()
    jar_file = decompiler._run_dex2jar()
    assert os.path.isfile(jar_file)
    assert jar_file.endswith(".jar")


def test_decompile(decompiler):
    procyon_decomp_path = os.path.join(decompiler.build_directory, "procyon")
    cfr_decomp_path = os.path.join(decompiler.build_directory, "cfr")
    assert all([not os.path.exists(path) for path in (procyon_decomp_path, cfr_decomp_path)])

    decompiler.run()

    assert os.path.isdir(decompiler.build_directory)

    assert os.path.isdir(procyon_decomp_path)
    assert os.path.isdir(os.path.join(procyon_decomp_path, "org"))

    assert os.path.isdir(cfr_decomp_path)
    assert os.path.isdir(os.path.join(cfr_decomp_path, "org"))

    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)


@pytest.mark.long
@pytest.mark.parametrize("external_decompiler", [
    (),
    (CFR()),
    (Procyon()),
    (Fernflower()),
])
def test_decompiler_function(decompiler, external_decompiler):
    decompiler._decompiler_function(external_decompiler)
    decompiler_build_directory = os.path.join(decompiler.build_directory, external_decompiler.name)
    assert os.path.isdir(decompiler_build_directory)
    assert os.path.isdir(os.path.join(decompiler_build_directory, "org"))
    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)
