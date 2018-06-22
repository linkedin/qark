import logging

from qark.issue import Severity
from qark.plugins.webview.helpers import webview_default_vulnerable
from qark.scanner.plugin import JavaASTPlugin

log = logging.getLogger(__name__)

SET_ALLOW_FILE_ACCESS_DESCRIPTION = (
    "File system access is enabled in this WebView. If untrusted data is used to specify the URL opened by this "
    "WebView, a malicious app or site may be able to read your app's private files, if it returns the response to "
    "them. To validate this vulnerability, load the following local file in this "
    "WebView: qark/poc/html/FILE_SYS_WARN.html"
)


class SetAllowFileAccess(JavaASTPlugin):
    """This plugin checks if the webview calls setAllowFileAccess(false), otherwise the webview is vulnerable
    (defaults to true)."""
    def __init__(self):
        super(SetAllowFileAccess, self).__init__(category="webview", name="Webview enables file access",
                                                 description=SET_ALLOW_FILE_ACCESS_DESCRIPTION)
        self.severity = Severity.WARNING

    def run(self):
        self.issues.extend(webview_default_vulnerable(self.java_ast, method_name="setAllowFileAccess", issue_name=self.name,
                                                      description=self.description, file_object=self.file_path,
                                                      severity=self.severity))


plugin = SetAllowFileAccess()
