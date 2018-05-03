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
        self.min_sdk = None

    def _process(self, tree, java_file):
        for _, method_invocation in tree.filter(MethodInvocation):
                if method_invocation.member == JAVA_DYNAMIC_BROADCAST_RECEIVER_METHOD and self.min_sdk < 14:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=DYNAMIC_BROADCAST_RECEIVER_DESCRIPTION,
                        file_object=java_file,
                        line_number=method_invocation.position)
                    )

    def run(self, filepath, apk_constants=None, java_ast=None, **kwargs):
        if not java_ast:
            return

        self.min_sdk = apk_constants["min_sdk"]
        self._process(tree=java_ast, java_file=filepath)


plugin = DynamicBroadcastReceiver()
