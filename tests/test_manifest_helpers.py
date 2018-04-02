from qark.plugins.manifest_helpers import get_min_sdk, get_target_sdk

from xml.dom import minidom


def test_get_min_sdk(vulnerable_manifest_path):
    assert 9 == get_min_sdk(minidom.parse(vulnerable_manifest_path))


def test_get_target_sdk(vulnerable_manifest_path):
    assert 15 == get_target_sdk(minidom.parse(vulnerable_manifest_path))
