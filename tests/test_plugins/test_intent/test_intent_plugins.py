import os
import shutil

from qark.plugins.intent.implicit_intent_to_pending_intent import ImplicitIntentToPendingIntent

import javalang

vuln_java_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_implicit_intent.java")


def test_empty_intent(build_directory):
    # set the path to manifest file
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = ImplicitIntentToPendingIntent()
    with open(vuln_java_file) as f:
        contents = f.read()

    ast = javalang.parse.parse(contents)
    plugin.run(vuln_java_file, file_contents=contents, java_ast=ast)
    assert len(plugin.issues) == 4
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)
