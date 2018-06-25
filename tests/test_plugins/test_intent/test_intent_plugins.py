import os

from qark.plugins.intent.implicit_intent_to_pending_intent import ImplicitIntentToPendingIntent


vuln_java_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_implicit_intent.java")


def test_empty_intent():
    plugin = ImplicitIntentToPendingIntent()
    plugin.update(file_path=vuln_java_file)
    plugin.run()
    assert len(plugin.issues) == 4
