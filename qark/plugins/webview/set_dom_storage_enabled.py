import logging

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Issue, Severity
from qark.plugins.helpers import java_files_from_files
from qark.plugins.webview.helpers import valid_set_method_bool
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

SET_DOM_STORAGE_ENABLED_DESCRIPTION = (
    "DOM Storage enabled for this WebView, there is a potential for caching sensitive information."
)


class SetDomStorageEnabled(BasePlugin):
    """This plugin checks if the `setDomStorageEnabled` method is called with a value of `true`."""
    def __init__(self):
        BasePlugin.__init__(self, category="webview", name="Webview enables DOM Storage",
                            description=SET_DOM_STORAGE_ENABLED_DESCRIPTION)
        self.severity = Severity.WARNING
        self.java_method_name = "setDomStorageEnabled"

    def run(self, filepath, java_ast=None, **kwargs):
        if not java_ast:
            return

        for _, method_invocation in java_ast.filter(MethodInvocation):
            if valid_set_method_bool(method_invocation, str_bool="true", method_name=self.java_method_name):
                self.issues.append(Issue(category=self.category, name=self.name, severity=self.severity,
                                         description=self.description, line_number=method_invocation.position,
                                         file_object=filepath))


plugin = SetDomStorageEnabled()
