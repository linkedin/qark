import os
import shutil

from qark.plugins.intent.implicit_intent_to_pending_intent import ImplicitIntentToPendingIntent

vuln_java_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_implicit_intent.java")


def test_empty_intent(build_directory):
    # set the path to manifest file
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    plugin = ImplicitIntentToPendingIntent()
    plugin.run([vuln_java_file])
    assert len(plugin.issues) == 4
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)
