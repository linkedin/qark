import logging

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Issue, Severity
from qark.plugins.helpers import java_files_from_files, get_min_sdk_from_files
from qark.plugins.webview.helpers import webview_default_vulnerable, valid_set_method_bool
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

SET_ALLOW_UNIVERSAL_ACCESS_FROM_FILE_URLS_DESCRIPTION = (
    "JavaScript running in a file scheme context can access content from any origin. This is an insecure default "
    "value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions. "
    "To validate this vulnerability, load the following local file in this WebView: "
    "file://qark/poc/html/UNIV_FILE_WARNING.html"
)


class SetAllowUniversalAccessFromFileURLs(BasePlugin):
    """This plugin checks if the `setAllowUniversalAccessFromFileURLs` method is called with a value of `true`, or
    if the default is vulnerable."""
    def __init__(self):
        BasePlugin.__init__(self, category="webview", name="Webview enables universal access for JavaScript",
                            description=SET_ALLOW_UNIVERSAL_ACCESS_FROM_FILE_URLS_DESCRIPTION)
        self.severity = Severity.WARNING
        self.java_method_name = "setAllowUniversalAccessFromFileURLs"

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

        if min_sdk <= 15:
            self.issues.extend(webview_default_vulnerable(tree, method_name=self.java_method_name,
                                                          issue_name=self.name, description=self.description,
                                                          file_object=java_file, severity=self.severity))
        else:
            for _, method_invocation in tree.filter(MethodInvocation):
                if valid_set_method_bool(method_invocation, str_bool="true", method_name=self.java_method_name):
                    self.issues.append(Issue(category=self.category, name=self.name, severity=self.severity,
                                             description=self.description, line_number=method_invocation.position,
                                             file_object=java_file))

    def run(self, files, apk_constants=None):
        min_sdk = get_min_sdk_from_files(files, apk_constants)
        java_files = java_files_from_files(files)

        for java_file in java_files:
            self._process(java_file, min_sdk)


plugin = SetAllowUniversalAccessFromFileURLs()
