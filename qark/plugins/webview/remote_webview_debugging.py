import logging

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Severity, Issue
from qark.plugins.webview.helpers import valid_set_method_bool
from qark.scanner.plugin import JavaASTPlugin

log = logging.getLogger(__name__)

JAVASCRIPT_REMOTE_DEBUGGING = (
    "Enabling webview remote debugging is insecure."
)

class RemoteDebugging(JavaASTPlugin):
    """This plugin checks if the `setWebContentsDebuggingEnabled` method is called with a value of `true`"""
    def __init__(self):
        super(RemoteDebugging, self).__init__(category="webview", name="Remote debugging enabled in Webview",
                                              description=JAVASCRIPT_REMOTE_DEBUGGING)
    def run(self):
        for _, method_invocation in self.java_ast.filter(MethodInvocation):
            if valid_set_method_bool(method_invocation, str_bool="true", method_name="setWebContentsDebuggingEnabled"):
                self.issues.append(Issue(category=self.category, name=self.name, severity=Severity.WARNING,
                                         description=self.description, line_number=method_invocation.position,
                                         file_object=self.file_path))

plugin = RemoteDebugging()
