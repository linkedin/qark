import pdb
import sys
import os
sys.path.append(os.path.abspath('../modules'))
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../lib'))
import common
import mock


def mocked_getConfig():
    return './fakeConfigFile'

@mock.patch('common.getConfig', return_value=mocked_getConfig())
def test_set_environment_variables(mocked):
    common.rootDir = './'
    assert 'ANDROID_HOME' not in os.environ
    common.set_environment_variables()
    assert 'ANDROID_HOME' in os.environ

def test_dedup():
    d = common.dedup
    assert common.dedup([1,2,3]) == [1,2,3]
    assert common.dedup([1,2,3,3]) == [1,2,3]

def test_find_ext():
    pass
def test_tree():
    pass
def test_normalizeActivityNames():
    pass
def test_check_export():
    pass
def test_sink_list_check():
    pass
def test_get_entry_for_component():
    pass
def test_readLayoutFiles():
    pass
def test_fcount():
    pass
def test_getConfig():
    pass
def test_writeKey():
    pass
def test_grep():
    pass
def test_find_java():
    pass
def test_find_xml():
    pass
def test_findKeys():
    pass
def test_find_xml():
    pass
def test_read_files():
    pass
def test_print_res_list():
    pass
def test_text_scan():
    pass
def test_text_scan_single():
    pass
def test_compare():
    pass
