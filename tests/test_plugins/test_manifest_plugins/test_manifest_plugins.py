from qark.plugins.manifest.allow_backup import ManifestBackupAllowed
from qark.plugins.manifest.custom_permissions import CustomPermissions
from qark.plugins.manifest.debuggable import DebuggableManifest
from qark.plugins.manifest.exported_tags import ExportedTags
from qark.issue import Severity

import os
import shutil


def test_allow_backup(decompiler, build_directory, vulnerable_manifest_path):
    # set the path to manifest file
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = ManifestBackupAllowed()
    plugin.run(vulnerable_manifest_path)
    assert len(plugin.issues) == 1
    assert plugin.issues[0].issue_name == plugin.issue_name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category

    decompiler.manifest_path = decompiler.run_apktool()
    plugin = ManifestBackupAllowed()
    plugin.run(decompiler.manifest_path)
    assert len(plugin.issues) == 0  # non vulnerable manifest
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)


def test_custom_permission(decompiler, build_directory, vulnerable_manifest_path):
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = CustomPermissions()
    plugin.run(vulnerable_manifest_path)
    assert len(plugin.issues) == 1
    assert plugin.issues[0].issue_name == plugin.issue_name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category

    decompiler.manifest_path = decompiler.run_apktool()
    plugin = CustomPermissions()
    plugin.run(decompiler.manifest_path)
    assert len(plugin.issues) == 0  # non vulnerable manifest
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)


def test_debuggable(decompiler, build_directory, vulnerable_manifest_path):
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)
    # the goatdroid manifest is vulnerable. Run it on a non-vulnerable one
    plugin = DebuggableManifest()
    plugin.run(vulnerable_manifest_path)
    assert len(plugin.issues) == 0

    decompiler.manifest_path = decompiler.run_apktool()
    plugin = DebuggableManifest()
    plugin.run(decompiler.manifest_path)
    assert len(plugin.issues) == 1  # vulnerable manifest
    assert plugin.issues[0].issue_name == plugin.issue_name
    assert plugin.issues[0].severity == plugin.severity
    assert plugin.issues[0].category == plugin.category
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)


def test_exported_tags(vulnerable_manifest_path):
    plugin = ExportedTags()
    plugin.run(vulnerable_manifest_path)
    assert len(plugin.issues) == 6
    for issue in plugin.issues:
        assert Severity.WARNING == issue.severity
        assert "Manifest" == issue.category
