import sys
import os
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../modules'))
sys.path.append(os.path.abspath('../lib'))
import common
import mock

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

