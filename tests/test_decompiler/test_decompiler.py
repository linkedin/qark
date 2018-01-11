import os
import shutil

import pytest

from qark.decompiler import decompiler


def test_copy_apk_to_zip(path_to_apk):
    assert path_to_apk + ".zip" == decompiler.copy_apk_to_zip(path_to_apk)
    assert os.path.isfile(path_to_apk + ".zip")

    with pytest.raises(SystemExit):
        decompiler.copy_apk_to_zip("1")


def test_unzip_file(path_to_apk, build_directory):
    decompiler.unzip_file(path_to_apk + ".zip", destination_to_unzip=build_directory)

    with pytest.raises(SystemExit):
        decompiler.unzip_file("1")

    shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)


def test_get_java_version():
    java_version = decompiler.get_java_version()
    assert not java_version.startswith('"')
    assert not java_version.endswith('"')


def test_unpack_apk(decompiler, bad_decompiler, build_directory):
    classes_dex_path = os.path.join(build_directory, "classes.dex")
    assert classes_dex_path == decompiler._unpack_apk()
    assert os.path.isfile(classes_dex_path)

    shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)

    with pytest.raises(SystemExit):
        bad_decompiler._unpack_apk()


def test_run_apktool(decompiler, build_directory):
    assert not os.path.isdir(build_directory)

    decompiler.run_apktool()
    assert os.path.isdir(build_directory)
    assert os.path.isfile(os.path.join(decompiler.build_directory, "AndroidManifest.xml"))

    shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)


def test_run_dex2jar(decompiler, build_directory):
    assert not os.path.isdir(build_directory)

    decompiler.dex_path = decompiler._unpack_apk()
    jar_file = decompiler._run_dex2jar()
    assert os.path.isfile(jar_file)
    assert jar_file.endswith(".jar")

    shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)


def test_decompile(decompiler, build_directory):
    assert not os.path.isdir(build_directory)

    decompiler._run_dex2jar()
    decompiler.decompile()

    assert os.path.isdir(build_directory)

    jdcore_decomp_path = os.path.join(build_directory, "jdcore")
    assert os.path.isdir(jdcore_decomp_path)
    assert os.path.isdir(os.path.join(jdcore_decomp_path, "org"))

    procyon_decomp_path = os.path.join(build_directory, "procyon")
    assert os.path.isdir(procyon_decomp_path)
    assert os.path.isdir(os.path.join(procyon_decomp_path, "org"))

    cfr_decomp_path = os.path.join(build_directory, "cfr")
    assert os.path.isdir(cfr_decomp_path)
    assert os.path.isdir(os.path.join(cfr_decomp_path, "org"))

    shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)



@pytest.mark.parametrize("decompiler_name, path_to_decompiler", [
    ("cfr", "{}/../../lib/decompilers/cfr_0_124.jar".format(os.path.dirname(os.path.abspath(__file__)))),
    ("jdcore", "{}/../../lib/decompilers/jd-core-java-1.2.jar".format(os.path.dirname(os.path.abspath(__file__)))),
    ("procyon", "{}/../../lib/decompilers/procyon-decompiler-0.5.30.jar".format(
        os.path.dirname(os.path.abspath(__file__)))),
])
def test_decompiler_function(decompiler, build_directory, decompiler_name, path_to_decompiler):
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)

    decompiler._decompiler_function(decompiler_name, path_to_decompiler)
    decompiler_build_directory = os.path.join(build_directory, decompiler_name)
    assert os.path.isdir(decompiler_build_directory)
    assert os.path.isdir(os.path.join(decompiler_build_directory, "org"))
    shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)
