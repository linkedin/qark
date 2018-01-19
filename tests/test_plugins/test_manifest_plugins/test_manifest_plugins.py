from qark.plugins.manifest.allow_backup import ManifestBackupAllowed
from qark.plugins.manifest.custom_permissions import CustomPermissions
from qark.plugins.manifest.debuggable import DebuggableManifest
from qark.plugins.manifest.exported_tags import ExportedTags
from qark.vulnerability import Severity

import os
import shutil


def test_allow_backup(decompiler, build_directory, vulnerable_manifest_path):
    # set the path to manifest file
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = ManifestBackupAllowed()
    plugin.run([vulnerable_manifest_path], apk_constants={})
    assert len(plugin.issues) == 1
    issue = plugin.issues.pop()
    assert issue.issue_name == plugin.issue_name
    assert issue.severity == plugin.severity
    assert issue.category == plugin.category

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
    issue = plugin.issues.pop()
    assert issue.issue_name == plugin.issue_name
    assert issue.severity == plugin.severity
    assert issue.category == plugin.category

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
    issue = plugin.issues.pop()
    assert issue.issue_name == plugin.issue_name
    assert issue.severity == plugin.severity
    assert issue.category == plugin.category
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)


def test_exported_tags(vulnerable_manifest_path):
    plugin = ExportedTags()
    plugin.run([vulnerable_manifest_path], apk_constants={})
    assert len(plugin.issues) == 6
    for issue in plugin.issues:
        assert Severity.WARNING == issue.severity
        assert "Manifest" == issue.category
