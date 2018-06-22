import os
import shutil
from xml.dom import minidom

import pytest

from qark.issue import Severity
from qark.plugins.manifest.allow_backup import ManifestBackupAllowed
from qark.plugins.manifest.custom_permissions import CustomPermissions
from qark.plugins.manifest.debuggable import DebuggableManifest
from qark.plugins.manifest.exported_tags import ExportedTags
from qark.plugins.manifest.min_sdk import MinSDK, TAP_JACKING
from qark.plugins.manifest.android_path import AndroidPath
from qark.plugins.manifest.api_keys import APIKeys
from qark.plugins.manifest.single_task_launch_mode import SingleTaskLaunchMode
from qark.plugins.manifest.task_reparenting import TaskReparenting
from qark.scanner.plugin import ManifestPlugin


@pytest.fixture(autouse=True)
def reset_manifest_plugin():
    ManifestPlugin.manifest_path = None
    ManifestPlugin.manifest_xml = None
    ManifestPlugin.min_sdk = -1
    ManifestPlugin.target_sdk = -1
    ManifestPlugin.package_name = "PACKAGE_NOT_FOUND"
    ExportedTags.all_files = None


@pytest.fixture(scope="module")
def test_android_manifest(vulnerable_manifest_path):
    return minidom.parse(vulnerable_manifest_path)


@pytest.fixture(scope="module")
def goatdroid_manifest(goatdroid_manifest_path):
    return minidom.parse(goatdroid_manifest_path)


def test_vulnerable_allow_backup(test_android_manifest):
    ManifestPlugin.manifest_xml = test_android_manifest
    plugin = ManifestBackupAllowed()
    plugin.run()
    assert len(plugin.issues) == 1
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category


def test_nonvulnerable_allow_backup(goatdroid_manifest):
    ManifestPlugin.manifest_xml = goatdroid_manifest
    plugin = ManifestBackupAllowed()
    plugin.run()
    assert len(plugin.issues) == 0  # non vulnerable manifest


def test_custom_permission_vulnerable(test_android_manifest):
    ManifestPlugin.manifest_xml = test_android_manifest
    plugin = CustomPermissions()
    plugin.run()
    assert len(plugin.issues) == 2
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity
    assert plugin.issues[0].category == plugin.category

    ManifestPlugin.manifest_xml = test_android_manifest
    ManifestPlugin.min_sdk = 21
    plugin = CustomPermissions()
    plugin.run()
    assert len(plugin.issues) == 1


def test_custom_permission_nonvulnerable(goatdroid_manifest, test_android_manifest):
    ManifestPlugin.manifest_xml = goatdroid_manifest
    plugin = CustomPermissions()
    plugin.run()
    assert len(plugin.issues) == 0


def test_debuggable_nonvulnerable(test_android_manifest):
    ManifestPlugin.manifest_xml = test_android_manifest
    plugin = DebuggableManifest()
    plugin.run()
    assert len(plugin.issues) == 0


def test_debuggable_vulnerable(goatdroid_manifest):
    ManifestPlugin.manifest_xml = goatdroid_manifest
    plugin = DebuggableManifest()
    plugin.run()
    assert len(plugin.issues) == 1
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category


def test_vulnerable_exported_tags(vulnerable_manifest_path, vulnerable_receiver_path):
    ManifestPlugin.update_manifest(vulnerable_manifest_path)
    ExportedTags.all_files = [vulnerable_receiver_path]
    plugin = ExportedTags()
    plugin.run()
    assert len(plugin.issues) == 6
    for issue in plugin.issues:
        assert Severity.WARNING == issue.severity
        assert "Manifest" == issue.category


@pytest.mark.parametrize("min_sdk", [
    -1,
    8,
])
def test_vulnerable_min_sdk(min_sdk):
    ManifestPlugin.update_manifest(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "test_min_sdk_tapjacking",
                                                "androidmanifest.xml"))
    ManifestPlugin.min_sdk = min_sdk
    plugin = MinSDK()
    plugin.run()
    assert 1 == len(plugin.issues)
    for issue in plugin.issues:
        assert Severity.VULNERABILITY == issue.severity
        assert "Tap Jacking possible" == issue.name
        assert TAP_JACKING == issue.description
        assert plugin.category == issue.category


def test_android_path(vulnerable_manifest_path):
    ManifestPlugin.update_manifest(vulnerable_manifest_path)
    plugin = AndroidPath()
    plugin.run()
    assert 1 == len(plugin.issues)


def test_api_keys(vulnerable_manifest_path):
    ManifestPlugin.update_manifest(vulnerable_manifest_path)
    plugin = APIKeys()
    plugin.run()
    assert 1 == len(plugin.issues)


def test_single_task_launch_mode(vulnerable_manifest_path):
    ManifestPlugin.update_manifest(vulnerable_manifest_path)
    plugin = SingleTaskLaunchMode()
    plugin.run()
    assert 1 == len(plugin.issues)


def test_task_reparenting(vulnerable_manifest_path):
    ManifestPlugin.update_manifest(vulnerable_manifest_path)
    plugin = TaskReparenting()
    plugin.run()
    assert 1 == len(plugin.issues)
