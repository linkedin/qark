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
from qark.scanner.plugin import ManifestPlugin


@pytest.fixture(scope="module")
def test_android_manifest(vulnerable_manifest_path):
    return minidom.parse(vulnerable_manifest_path)


@pytest.fixture(scope="module")
def goatdroid_manifest(module_decompiler, build_directory):
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    return minidom.parse(module_decompiler.run_apktool())


def test_vulnerable_allow_backup(test_android_manifest):
    plugin = ManifestBackupAllowed(manifest_xml=test_android_manifest)
    plugin.run([], apk_constants={})
    assert len(plugin.issues) == 1
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category


def test_nonvulnerable_allow_backup(goatdroid_manifest):
    plugin = ManifestBackupAllowed(manifest_xml=goatdroid_manifest)
    plugin.run([], apk_constants={})
    assert len(plugin.issues) == 0  # non vulnerable manifest


def test_custom_permission_vulnerable(test_android_manifest):
    plugin = CustomPermissions(manifest_xml=test_android_manifest)
    plugin.run([], apk_constants={})
    assert len(plugin.issues) == 1
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity
    assert plugin.issues[0].category == plugin.category


def test_custom_permission_nonvulnerable(goatdroid_manifest):
    plugin = CustomPermissions(manifest_xml=goatdroid_manifest)
    plugin.run([], apk_constants={})
    assert len(plugin.issues) == 0


def test_debuggable_nonvulnerable(test_android_manifest):
    plugin = DebuggableManifest(manifest_xml=test_android_manifest)
    plugin.run([], apk_constants={})
    assert len(plugin.issues) == 0


def test_debuggable_vulnerable(goatdroid_manifest):
    plugin = DebuggableManifest(manifest_xml=goatdroid_manifest)
    plugin.run([], apk_constants={})
    assert len(plugin.issues) == 1  # vulnerable manifest
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category


def test_vulnerable_exported_tags(vulnerable_manifest_path, vulnerable_receiver_path):
    ManifestPlugin.update_manifest(vulnerable_manifest_path)
    plugin = ExportedTags()
    plugin.run([vulnerable_receiver_path], apk_constants={})
    assert len(plugin.issues) == 6
    for issue in plugin.issues:
        assert Severity.WARNING == issue.severity
        assert "Manifest" == issue.category


@pytest.mark.parametrize("apk_constants", [
    None,
    {"min_sdk": 8},
    {},
])
def test_vulnerable_min_sdk(apk_constants):
    ManifestPlugin.update_manifest(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "test_min_sdk_tapjacking",
                                                "androidmanifest.xml"))
    plugin = MinSDK()
    plugin.run([], apk_constants=apk_constants)
    assert 1 == len(plugin.issues)
    for issue in plugin.issues:
        assert Severity.VULNERABILITY == issue.severity
        assert "Tap Jacking possible" == issue.name
        assert TAP_JACKING == issue.description
        assert plugin.category == issue.category
