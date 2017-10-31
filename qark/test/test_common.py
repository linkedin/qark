import sys
import os
import logging
import mock
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../modules'))
sys.path.append(os.path.abspath('../lib'))
import common
import qark.modules.common

import pytest


def mocked_getConfig():
    return './fakeConfigFile'


@mock.patch('common.getConfig', return_value=mocked_getConfig())
def test_set_environment_variables(mocked):
    common.rootDir = './'
    with mock.patch.dict('os.environ'):
        os.environ.pop('ANDROID_HOME', None)
        assert 'ANDROID_HOME' not in os.environ
        common.set_environment_variables()
        assert 'ANDROID_HOME' in os.environ


def test_dedup():
    d = common.dedup
    assert common.dedup([1,2,3]) == [1,2,3]
    assert common.dedup([1,2,3,3]) == [1,2,3]


def test_initialize_logger():
    assert logging.WARNING == qark.modules.common.logger.level
    qark.modules.common.rootDir = "."
    qark.modules.common.initialize_logger()
    assert logging.INFO == qark.modules.common.logger.level
    assert os.path.isdir("./logs")
    os.rmdir("./logs")
    assert not os.path.isdir("./logs")
    assert 2 >= len(qark.modules.common.logger.handlers)

    # this method has side effects on common.logger, the following resets the logger
    root = logging.getLogger()
    map(root.removeHandler, root.handlers[:])
    map(root.removeFilter, root.filters[:])


def test_checkJavaVersion(capsys):
    qark.modules.common.checkJavaVersion()
    out, err = capsys.readouterr()
    assert out is not None


def test_writeKey():
    if not os.path.exists("../settings.properties"):
        f = open("../settings.properties",'w')
        f.close()
    qark.modules.common.rootDir = "../"
    qark.modules.common.writeKey("test_key", "test_value")

    assert "test_value" == qark.modules.common.getConfig("test_key")
    qark.modules.common.writeKey("test_key", "new_test_value")
    assert "new_test_value" == qark.modules.common.getConfig("test_key")


def test_grep():
    test_matches = qark.modules.common.grep(".", "test")
    assert 5 <= len(test_matches)
    for match in test_matches:
        assert "test" in match


def test_find_java():
    qark.modules.common.logger = mock.MagicMock()
    javas = qark.modules.common.find_java(".")
    assert 0 < len(javas)


def test_find_xml():
    qark.modules.common.logger = mock.MagicMock()
    xmls = qark.modules.common.find_xml(".")
    assert 0 < len(xmls)


def test_read_files():
    matches = qark.modules.common.read_files("test_common.py", "MagicMock")
    assert 0 < len(matches)


def test_text_scan():
    matches = qark.modules.common.text_scan(["test_common.py", "test_api_plugin.py"], "MagicMock")
    assert 0 < len(matches)


def test_scan_single():
    matches = qark.modules.common.text_scan_single("test_common.py", "MagicMock")
    assert 1 < len(matches)


def test_normalizeActivityNames():
    activityList = qark.modules.common.normalizeActivityNames(["activity", ".activity", "something"], "package_name")
    assert 3 == len(activityList)
    assert "package_name.activity" == activityList[1]


def test_get_entry_for_component():
    assert ['onCreate', 'onStart'] == qark.modules.common.get_entry_for_component("activity")
    assert ['onCreate', 'onStart'] == qark.modules.common.get_entry_for_component("activity-alias")
    assert ['onReceive'] == qark.modules.common.get_entry_for_component("receiver")
    assert ['onCreate', 'onBind', 'onStartCommand', 'onHandleIntent'] == qark.modules.common.get_entry_for_component("service")
    assert ['onReceive'] == qark.modules.common.get_entry_for_component("provider")
