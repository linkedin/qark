import logging

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

LOAD_DATA_WITH_BASE_URL_DESCRIPTION = (
    "This webView sets the BaseURL. You should verify that this is only loading content "
    "from this domain. Loading content from a domain you do not control, or using "
    "plain-text HTTP, leaves this vulnerable to injection attacks against the BaseURL "
    "domain."
)


class LoadDataWithBaseURL(BasePlugin):
    """This plugin checks if the `loadDataWithBaseURL` method is called."""
    def __init__(self):
        BasePlugin.__init__(self, category="webview", name="BaseURL set for Webview",
                            description=LOAD_DATA_WITH_BASE_URL_DESCRIPTION)

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

        for _, method_invocation in tree.filter(MethodInvocation):
            if method_invocation.member == "loadDataWithBaseURL" and len(method_invocation.arguments) == 5:
                self.issues.append(Issue(category=self.category, name=self.name, severity=Severity.WARNING,
                                         description=self.description, line_number=method_invocation.position,
                                         file_object=java_file))

    def run(self, files, apk_constants=None):
        java_files = java_files_from_files(files)
        for java_file in java_files:
            self._process(java_file)


plugin = LoadDataWithBaseURL()
