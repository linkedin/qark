import logging

import javalang
from javalang.tree import ClassDeclaration, MethodDeclaration
from qark.issue import Issue, Severity
from qark.plugins.helpers import java_files_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

DYNAMIC_BROADCAST_RECEIVER_DESCRIPTION = (
    "Application dynamically registers a broadcast receiver\nApplication that register a broadcast receiver "
    "dynamically is vulnerable to granting unrestricted access to the broadcast receiver.\nThe receiver will "
    "be called with any broadcast Intent that matches filter.\n https://developer.android.com/reference/android/"
    "content/Context.html#registerReceiver(android.content.BroadcastReceiver, android.content.IntentFilter)"
)

JAVA_DYNAMIC_BROADCAST_RECEIVER_METHOD = 'registerReceiver'


class DynamicBroadcastReceiver(BasePlugin):
    """This plugin checks if the `addJavaScriptInterface` method is called with a min_sdk of below 17."""

    def __init__(self):
        BasePlugin.__init__(self, category="broadcast", name="Dynamic broadcast receiver found",
                            description=DYNAMIC_BROADCAST_RECEIVER_DESCRIPTION)
        self.severity = Severity.VULNERABILITY

    def _process(self, java_file):
        try:
            with open(java_file, "r") as java_file_to_read:
                file_contents = java_file_to_read.read()
        except IOError:
            log.debug("File does not exist %s, continuing", java_file)
            return

        try:
            tree = javalang.parse.parse(file_contents)
        except (javalang.parser.JavaSyntaxError, IndexError):
            log.debug("Error parsing file %s, continuing", java_file)
            return

        for _, declared_class in tree.filter(ClassDeclaration):
            for _, declared_method in declared_class.filter(MethodDeclaration):
                if declared_method.name == JAVA_DYNAMIC_BROADCAST_RECEIVER_METHOD:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=DYNAMIC_BROADCAST_RECEIVER_DESCRIPTION,
                        file_object=java_file,
                        line_number=declared_method.position)
                    )

    def run(self, files, apk_constants=None):
        java_files = java_files_from_files(files)

        for java_file in java_files:
            self._process(java_file)


plugin = DynamicBroadcastReceiver()
