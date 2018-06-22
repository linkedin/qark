import logging

from qark.issue import Severity
from qark.plugins.webview.helpers import webview_default_vulnerable
from qark.scanner.plugin import JavaASTPlugin

log = logging.getLogger(__name__)

SET_ALLOW_CONTENT_ACCESS_DESCRIPTION = (
    "While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access "
    "from WebViews. If the WebViews take in untrusted input, this can allow for data theft. To validate this "
    "vulnerability, load the following local file in this WebView: "
    "file://qark/poc/html/WV_CPA_WARNING.html"
)


class SetAllowContentAccess(JavaASTPlugin):
    """This plugin checks if the webview calls setAllowContentAccess(false), otherwise the webview is vulnerable
    (defaults to true)."""
    def __init__(self):
        super(SetAllowContentAccess, self).__init__(category="webview", name="Webview enables content access",
                                                    description=SET_ALLOW_CONTENT_ACCESS_DESCRIPTION)
        self.severity = Severity.WARNING

    def run(self):
        self.issues.extend(webview_default_vulnerable(self.java_ast, method_name="setAllowContentAccess",
                                                      issue_name=self.name,
                                                      description=self.description, file_object=self.file_path,
                                                      severity=self.severity))


plugin = SetAllowContentAccess()
