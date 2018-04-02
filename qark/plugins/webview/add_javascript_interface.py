import logging

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Issue, Severity
from qark.plugins.helpers import java_files_from_files, get_min_sdk_from_files, valid_method_invocation
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

ADD_JAVASCRIPT_INTERFACE_DESCRIPTION = (
    "This webview uses the addJavascriptInterface method in a pre-API 17 app, which exposes all public methods to "
    "Javascript running in the WebView. If this webview loads untrusted content or trusted content over plain-text "
    "HTTP, this represents a MAJOR issue! Reference: "
    "https://labs.mwrinfosecurity.com/blog/2013/09/24/webview-addjavascriptinterface-remote-code-execution/. "
    "To validate this vulnerability, load the following local file in this WebView: "
    "file://qark/poc/html/BAD_JS_INT.html"
)


class AddJavascriptInterface(BasePlugin):
    """This plugin checks if the `addJavaScriptInterface` method is called with a min_sdk of below 17."""
    def __init__(self):
        BasePlugin.__init__(self, category="webview", name="Webview uses addJavascriptInterface pre-API 17",
                            description=ADD_JAVASCRIPT_INTERFACE_DESCRIPTION)
        self.severity = Severity.WARNING
        self.java_method_name = "addJavascriptInterface"

    def _process(self, java_file, min_sdk):
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

        if min_sdk <= 16:
            for _, method_invocation in tree.filter(MethodInvocation):
                if valid_method_invocation(method_invocation, method_name=self.java_method_name, num_arguments=2):
                    self.issues.append(Issue(category=self.category, name=self.name, severity=self.severity,
                                             description=self.description, line_number=method_invocation.position,
                                             file_object=java_file))

    def run(self, files, apk_constants=None):
        min_sdk = get_min_sdk_from_files(files, apk_constants)
        java_files = java_files_from_files(files)

        for java_file in java_files:
            self._process(java_file, min_sdk)


plugin = AddJavascriptInterface()
