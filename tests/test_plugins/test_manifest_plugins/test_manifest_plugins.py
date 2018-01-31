import os
import shutil

import pytest

from qark.issue import Severity
from qark.plugins.manifest.allow_backup import ManifestBackupAllowed
from qark.plugins.manifest.custom_permissions import CustomPermissions
from qark.plugins.manifest.debuggable import DebuggableManifest
from qark.plugins.manifest.exported_tags import ExportedTags
from qark.plugins.manifest.min_sdk import MinSDK, TAP_JACKING


def test_allow_backup(decompiler, build_directory, vulnerable_manifest_path):
    # set the path to manifest file
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = ManifestBackupAllowed()
    plugin.run([vulnerable_manifest_path], apk_constants={})
    assert len(plugin.issues) == 1
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category

    decompiler.manifest_path = decompiler.run_apktool()
    plugin = ManifestBackupAllowed()
    plugin.run([decompiler.manifest_path], apk_constants={})
    assert len(plugin.issues) == 0  # non vulnerable manifest
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)


def test_custom_permission(decompiler, build_directory, vulnerable_manifest_path):
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = CustomPermissions()
    plugin.run([vulnerable_manifest_path], apk_constants={})
    assert len(plugin.issues) == 1
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category

    decompiler.manifest_path = decompiler.run_apktool()
    plugin = CustomPermissions()
    plugin.run([decompiler.manifest_path], apk_constants={})
    assert len(plugin.issues) == 0  # non vulnerable manifest
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)


def test_debuggable(decompiler, build_directory, vulnerable_manifest_path):
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)
    # the goatdroid manifest is vulnerable. Run it on a non-vulnerable one
    plugin = DebuggableManifest()
    plugin.run([vulnerable_manifest_path], apk_constants={})
    assert len(plugin.issues) == 0

    decompiler.manifest_path = decompiler.run_apktool()
    plugin = DebuggableManifest()
    plugin.run([decompiler.manifest_path], apk_constants={})
    assert len(plugin.issues) == 1  # vulnerable manifest
    assert plugin.issues[0].name == plugin.name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)


def test_exported_tags(vulnerable_manifest_path):
    plugin = ExportedTags()
    plugin.run([vulnerable_manifest_path], apk_constants={})
    assert len(plugin.issues) == 6
    for issue in plugin.issues:
        assert Severity.WARNING == issue.severity
        assert "Manifest" == issue.category


@pytest.mark.parametrize("apk_constants", [
    None,
    {"min_sdk": 8},
    {},
])
def test_min_sdk(apk_constants):
    plugin = MinSDK()
    plugin.run([os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "test_min_sdk_tapjacking",
                             "androidmanifest.xml")],
               apk_constants=apk_constants)
    assert 1 == len(plugin.issues)
    for issue in plugin.issues:
        assert Severity.VULNERABILITY == issue.severity
        assert "Tap Jacking possible" == issue.name
        assert TAP_JACKING == issue.description
        assert plugin.category == issue.category
