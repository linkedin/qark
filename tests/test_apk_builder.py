import os
import shutil

import pytest

from qark.apk_builder import APKBuilder
from qark.plugins.manifest.exported_tags import ExportedTags

# Path to SDK is required, so these are commented out
# def test_gradle_build(build_directory, vulnerable_manifest_path):
#     if os.path.exists(build_directory):
#         shutil.rmtree(build_directory)
#
#     builder = APKBuilder(exploit_apk_path=build_directory,
#                          issues=[],
#                          apk_name="test_apk",
#                          manifest_path=vulnerable_manifest_path,
#                          sdk_path="/Users/nwalsh/IdeaProjects/qark/android-sdk_r24.0.2-macosx/android-sdk-macosx")
#     builder._build_apk()
#
#
# def test_apk_build(build_directory, vulnerable_manifest_path):
#     if os.path.exists(build_directory):
#         shutil.rmtree(build_directory)
#
#     builder = APKBuilder(exploit_apk_path=build_directory,
#                          issues=[],
#                          apk_name="test_apk",
#                          manifest_path=vulnerable_manifest_path,
#                          sdk_path="/Users/nwalsh/IdeaProjects/qark/android-sdk_r24.0.2-macosx/android-sdk-macosx")
#     builder.build()
