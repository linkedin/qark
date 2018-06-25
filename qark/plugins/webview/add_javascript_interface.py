import logging

from javalang.tree import MethodInvocation

from qark.issue import Issue, Severity
from qark.plugins.helpers import valid_method_invocation
from qark.scanner.plugin import JavaASTPlugin, ManifestPlugin

log = logging.getLogger(__name__)

ADD_JAVASCRIPT_INTERFACE_DESCRIPTION = (
    "This webview uses the addJavascriptInterface method in a pre-API 17 app, which exposes all public methods to "
    "Javascript running in the WebView. If this webview loads untrusted content or trusted content over plain-text "
    "HTTP, this represents a MAJOR issue! Reference: "
    "https://labs.mwrinfosecurity.com/blog/2013/09/24/webview-addjavascriptinterface-remote-code-execution/. "
    "To validate this vulnerability, load the following local file in this WebView: "
    "file://qark/poc/html/BAD_JS_INT.html"
)


class AddJavascriptInterface(JavaASTPlugin, ManifestPlugin):
    """This plugin checks if the `addJavaScriptInterface` method is called with a min_sdk of below 17."""
    def __init__(self):
        super(AddJavascriptInterface, self).__init__(category="webview",
                                                     name="Webview uses addJavascriptInterface pre-API 17",
                                                     description=ADD_JAVASCRIPT_INTERFACE_DESCRIPTION)
        self.severity = Severity.WARNING
        self.java_method_name = "addJavascriptInterface"

    def run(self):
        if self.min_sdk <= 16:
            for _, method_invocation in self.java_ast.filter(MethodInvocation):
                if valid_method_invocation(method_invocation, method_name=self.java_method_name, num_arguments=2):
                    self.issues.append(Issue(category=self.category, name=self.name, severity=self.severity,
                                             description=self.description, line_number=method_invocation.position,
                                             file_object=self.file_path))


plugin = AddJavascriptInterface()
