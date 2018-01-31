from click.testing import CliRunner

from qark.qark import cli

import os
import shutil


def test_full_sca(path_to_apk, build_directory):
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)
    os.environ['LC_ALL'] = 'en_US.utf-8'
    os.environ['LANG'] = 'en_US.utf-8'

    runner = CliRunner()

    # decompile and run scans on goatdroid APK putting output to build_directory
    result = runner.invoke(cli, ["--apk", path_to_apk, "--build-path", build_directory])
    assert 0 == result.exit_code


    # run scans on build directory files
    result = runner.invoke(cli, ["--java", build_directory])
    assert 0 == result.exit_code

    # scan a file that has an issue
    result = runner.invoke(cli, ["--java", "build_directory/cfr/android/support/v4/content/LocalBroadcastManager.java"])
    assert 0 == result.exit_code
