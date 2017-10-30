import os
import subprocess
import stat

import qark.qarkMain
import qark.modules.sdkManager

import pytest


def test_autodiscover_regression():
    qark.sdkManager.common.rootDir = '..'

    if not os.path.exists("../settings.properties"):
        f = open("../settings.properties",'w')
        f.close()

    qark.sdkManager.common.writeKey("rootDir", "..")
    qark.sdkManager.common.initialize_logger()
    qark.modules.sdkManager.download_sdk()  # first download the sdk so that we can use it
    result = subprocess.call("python ../qarkMain.py --source 2 --manifest testData/goatdroid/goatdroid/AndroidManifest.xml -a 1 --exploit 0 --install 0".split())
    assert 0 == result


@pytest.mark.parametrize("manifest_arg,expected", [
    ("", False),
    (None, False),
    ("f", False),
    ("F", False),
    ("False", False),
    ("false", False),
    ("valid", True)
])
def test_valid_manifest(manifest_arg, expected):
    assert expected == qark.qarkMain.valid_manifest_file(manifest_arg)


def test_get_manifestXML():
    qark.qarkMain.get_manifestXML("test_manifest")
    assert "test_manifest" == qark.qarkMain.common.manifest


@pytest.mark.parametrize("json_obj, expected_xml", [
    ({1:"thing"}, "<1>\n\tthing\n</1>"),
    ("thing", "thing"),
    ([{1: "thing"}], "<1>\n\tthing\n</1>"),
    ([{1: "thing"}, {1: "other"}], "<1>\n\tthing\n</1>\n<1>\n\tother\n</1>"),
])
def test_json2xml(json_obj, expected_xml):
    assert expected_xml == qark.qarkMain.json2xml(json_obj)


def test_hasmode():
    assert qark.qarkMain.hasmode("test_common.py", stat.S_IREAD)


def test_setmode():
    if not qark.qarkMain.hasmode("test_common.py", stat.S_IEXEC):
        qark.qarkMain.setmode("test_common.py", stat.S_IEXEC)
        assert qark.qarkMain.hasmode("test_common.py", stat.S_IEXEC)
