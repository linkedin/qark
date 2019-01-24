import logging

from javalang.tree import MethodInvocation

from qark.issue import Severity, Issue
from qark.scanner.plugin import CoroutinePlugin

log = logging.getLogger(__name__)

LOAD_DATA_WITH_BASE_URL_DESCRIPTION = (
    "This webView sets the BaseURL. You should verify that this is only loading content "
    "from this domain. Loading content from a domain you do not control, or using "
    "plain-text HTTP, leaves this vulnerable to injection attacks against the BaseURL "
    "domain."
)


class LoadDataWithBaseURL(CoroutinePlugin):
    """This plugin checks if the `loadDataWithBaseURL` method is called."""
    def __init__(self):
        super(LoadDataWithBaseURL, self).__init__(category="webview", name="BaseURL set for Webview",
                                                  description=LOAD_DATA_WITH_BASE_URL_DESCRIPTION)

    def run_coroutine(self):
        while True:
            _, method_invocation = (yield)
            if not isinstance(method_invocation, MethodInvocation):
                continue

            if method_invocation.member == "loadDataWithBaseURL" and len(method_invocation.arguments) == 5:
                self.issues.append(Issue(category=self.category, name=self.name, severity=Severity.WARNING,
                                         description=self.description, line_number=method_invocation.position,
                                         file_object=self.file_path))


plugin = LoadDataWithBaseURL()
