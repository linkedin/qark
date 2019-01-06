import logging

from javalang.tree import MethodInvocation

from qark.issue import Issue, Severity
from qark.plugins.webview.helpers import webview_default_vulnerable, valid_set_method_bool
from qark.scanner.plugin import CoroutinePlugin, ManifestPlugin

log = logging.getLogger(__name__)

SET_ALLOW_UNIVERSAL_ACCESS_FROM_FILE_URLS_DESCRIPTION = (
    "JavaScript running in a file scheme context can access content from any origin. This is an insecure default "
    "value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions. "
    "To validate this vulnerability, load the following local file in this WebView: "
    "file://qark/poc/html/UNIV_FILE_WARNING.html"
)


class SetAllowUniversalAccessFromFileURLs(CoroutinePlugin, ManifestPlugin):
    """This plugin checks if the `setAllowUniversalAccessFromFileURLs` method is called with a value of `true`, or
    if the default is vulnerable."""
    def __init__(self):
        super(SetAllowUniversalAccessFromFileURLs, self).__init__(category="webview",
                                                                  name="Webview enables universal access for JavaScript",
                                                                  description=SET_ALLOW_UNIVERSAL_ACCESS_FROM_FILE_URLS_DESCRIPTION)
        self.severity = Severity.WARNING
        self.java_method_name = "setAllowUniversalAccessFromFileURLs"

    def can_run_coroutine(self):
        if self.min_sdk <= 15:
            self.issues.extend(webview_default_vulnerable(self.java_ast, method_name=self.java_method_name,
                                                          issue_name=self.name, description=self.description,
                                                          file_object=self.file_path, severity=self.severity))
            return False

        return True

    def run_coroutine(self):
        while True:
            _, method_invocation = (yield)
            if not isinstance(method_invocation, MethodInvocation):
                continue

            if valid_set_method_bool(method_invocation, str_bool="true", method_name=self.java_method_name):
                self.issues.append(Issue(category=self.category, name=self.name, severity=self.severity,
                                         description=self.description, line_number=method_invocation.position,
                                         file_object=self.file_path))


plugin = SetAllowUniversalAccessFromFileURLs()
