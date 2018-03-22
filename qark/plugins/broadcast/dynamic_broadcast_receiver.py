"""This plugin detects if a method ``registerReceiver`` is being called with a min_sdk of less than 14.

ICE_CREAM_SANDWICH properly registers receivers so anything >= API level 14 is not vulnerable."""

import logging

import javalang
from javalang.tree import ClassDeclaration, MethodInvocation
from qark.issue import Issue, Severity
from qark.plugins.helpers import java_files_from_files, get_min_sdk_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

DYNAMIC_BROADCAST_RECEIVER_DESCRIPTION = (
    "Application that register a broadcast receiver dynamically is vulnerable to granting unrestricted access to the "
    "broadcast receiver. The receiver will be called with any broadcast Intent that matches filter."
    " Reference: https://developer.android.com/reference/android/"
    "content/Context.html#registerReceiver(android.content.BroadcastReceiver, android.content.IntentFilter)"
)

JAVA_DYNAMIC_BROADCAST_RECEIVER_METHOD = 'registerReceiver'


class DynamicBroadcastReceiver(BasePlugin):

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

        for _, method_invocation in tree.filter(MethodInvocation):
                if method_invocation.member == JAVA_DYNAMIC_BROADCAST_RECEIVER_METHOD and self.min_sdk < 14:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=DYNAMIC_BROADCAST_RECEIVER_DESCRIPTION,
                        file_object=java_file,
                        line_number=method_invocation.position)
                    )

    def run(self, files, apk_constants=None):
        self.min_sdk = apk_constants["min_sdk"] if "min_sdk" in apk_constants else get_min_sdk_from_files(files,
                                                                                                          apk_constants)
        java_files = java_files_from_files(files)

        for java_file in java_files:
            self._process(java_file)


plugin = DynamicBroadcastReceiver()
