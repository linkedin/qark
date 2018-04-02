import logging

import javalang

from qark.issue import Severity
from qark.plugins.helpers import java_files_from_files
from qark.plugins.webview.helpers import webview_default_vulnerable
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

SET_ALLOW_CONTENT_ACCESS_DESCRIPTION = (
    "While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access "
    "from WebViews. If the WebViews take in untrusted input, this can allow for data theft. To validate this "
    "vulnerability, load the following local file in this WebView: "
    "file://qark/poc/html/WV_CPA_WARNING.html"
)


class SetAllowContentAccess(BasePlugin):
    """This plugin checks if the webview calls setAllowContentAccess(false), otherwise the webview is vulnerable
    (defaults to true)."""
    def __init__(self):
        BasePlugin.__init__(self, category="webview", name="Webview enables content access",
                            description=SET_ALLOW_CONTENT_ACCESS_DESCRIPTION)
        self.severity = Severity.WARNING

    def _process(self, java_file):
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

        self.issues.extend(webview_default_vulnerable(tree, method_name="setAllowContentAccess", issue_name=self.name,
                                                      description=self.description, file_object=java_file,
                                                      severity=self.severity))

    def run(self, files, apk_constants=None):
        java_files = java_files_from_files(files)
        for java_file in java_files:
            self._process(java_file)


plugin = SetAllowContentAccess()
