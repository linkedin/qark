"""
Checks if either a method within ``ANDROID_LOGGING_METHODS`` is invoked with `Log.` before it.

For instance:
Log.d("test")
Log.e("test")

Both trigger but the following does not:
d("test")
e("test")
"""

import logging

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

ANDROID_LOGGING_DESCRIPTION = (
    "Logs are detected. This may allow potential leakage of information from Android applications. Logs should never be"
    " compiled into an application except during development. Reference: "
    "https://developer.android.com/reference/android/util/Log.html"
)

ANDROID_LOGGING_METHODS = ("v", "d", "i", "w", "e")


class AndroidLogging(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="file", name="Logging found",
                            description=ANDROID_LOGGING_DESCRIPTION)
        self.severity = Severity.WARNING

    def run(self, filepath, java_ast=None, **kwargs):
        if not java_ast:
            return

        for _, method_invocation in java_ast.filter(MethodInvocation):
            if method_invocation.qualifier == "Log" and method_invocation.member in ANDROID_LOGGING_METHODS:
                self.issues.append(Issue(
                    category=self.category, severity=self.severity, name=self.name,
                    description=self.description,
                    file_object=filepath,
                    line_number=method_invocation.position)
                )


plugin = AndroidLogging()
