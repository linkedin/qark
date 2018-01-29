import os
import shutil

import pytest

from qark.apk_builder import APKBuilder


def test_gradle_build(decompiler, build_directory, vulnerable_manifest_path):
    builder = APKBuilder(exploit_apk_path=build_directory,
                         issues=[],
                         apk_name="test_apk",
                         manifest_path=vulnerable_manifest_path,
                         sdk_path="/Users/nwalsh/IdeaProjects/qark/android-sdk_r24.0.2-macosx/android-sdk-macosx")
    builder._build_apk()

