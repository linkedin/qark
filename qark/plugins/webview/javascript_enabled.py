import logging

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files
from qark.plugins.webview.helpers import valid_set_method_bool
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

JAVASCRIPT_ENABLED_DESCRIPTION = (
    "While not a vulnerability by itself, it appears this app has JavaScript enabled in "
    "the WebView: If this is not expressly necessary, you should disable "
    "it, to prevent the possibility of XSS (cross-site scripting) attacks. More info: "
    "http://developer.android.com/guide/practices/security.html To validate this "
    "vulnerability, load the following local file in this "
    "WebView: qark/poc/html/JS_WARNING.html"
)


class JavascriptEnabled(BasePlugin):
    """This plugin checks if the `setJavaScriptEnabled` method is called with a value of `true`"""
    def __init__(self):
        BasePlugin.__init__(self, category="webview", name="Javascript enabled in Webview",
                            description=JAVASCRIPT_ENABLED_DESCRIPTION)

    def run(self, java_file, java_ast=None, **kwargs):
        if not java_ast:
            return

        for _, method_invocation in java_ast.filter(MethodInvocation):
            if valid_set_method_bool(method_invocation, str_bool="true", method_name="setJavaScriptEnabled"):
                self.issues.append(Issue(category=self.category, name=self.name, severity=Severity.WARNING,
                                         description=self.description, line_number=method_invocation.position,
                                         file_object=java_file))


plugin = JavascriptEnabled()
