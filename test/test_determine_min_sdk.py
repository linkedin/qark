import pdb
import sys
import os
sys.path.append(os.path.abspath('../modules'))
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../lib'))
import DetermineMinSDK
import common
import mock
import unittest
from xml.dom import minidom

def mocked_os_walk(notUsed):
    return [('./testData/testGradle', [], ['build.gradle'])]

@mock.patch('os.walk', side_effect=mocked_os_walk)
def test_find_gradle(mock_os):
    walkList = list(os.walk('.'))
    for f in walkList:
    	print f
    out = DetermineMinSDK.find_gradle() 
    assert False # pretty sure the regex for finding build.gradle is broken

def test_determine_min_sdk():
    common.xmldoc = minidom.parse('./testData/apktool/AndroidManifest.xml')
    DetermineMinSDK.determine_min_sdk()
    assert common.minSdkVersion == 9

if __name__ == '__main__':
	test_find_gradle()
	test_determine_min_sdk()
