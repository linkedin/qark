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

from javalang.tree import MethodInvocation

from qark.issue import Severity, Issue
from qark.scanner.plugin import CoroutinePlugin

log = logging.getLogger(__name__)

ANDROID_LOGGING_DESCRIPTION = (
    "Logs are detected. This may allow potential leakage of information from Android applications. Logs should never be"
    " compiled into an application except during development. Reference: "
    "https://developer.android.com/reference/android/util/Log.html"
)

ANDROID_LOGGING_METHODS = ("v", "d", "i", "w", "e")


class AndroidLogging(CoroutinePlugin):
    def __init__(self):
        super(AndroidLogging, self).__init__(category="file", name="Logging found",
                                             description=ANDROID_LOGGING_DESCRIPTION)
        self.severity = Severity.WARNING

    def run_coroutine(self):
        while True:
            _, method_invocation = (yield)

            if not isinstance(method_invocation, MethodInvocation):
                continue

            if method_invocation.qualifier == "Log" and method_invocation.member in ANDROID_LOGGING_METHODS:
                self.issues.append(Issue(
                    category=self.category, severity=self.severity, name=self.name,
                    description=self.description,
                    file_object=self.file_path,
                    line_number=method_invocation.position)
                )


plugin = AndroidLogging()
