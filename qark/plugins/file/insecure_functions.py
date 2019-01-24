import logging

from javalang.tree import MethodDeclaration

from qark.issue import Severity, Issue
from qark.scanner.plugin import CoroutinePlugin

log = logging.getLogger(__name__)

INSECURE_FUNCTIONS_DESCRIPTION = (
    "The Content provider API provides a method call. The framework does no permission checking on this "
    "entry into the content provider besides the basic ability for the application to get access to the provider"
    " at all. Any implementation of this method must do its own permission checks on incoming calls to make sure "
    "they are allowed. Failure to do so will allow unauthorized components to interact with the content provider. "
    "Reference: https://bitbucket.org/secure-it-i/android-app-vulnerability-benchmarks/src/d5305b9481df3502e60e98fa352d5f58e4a69044/ICC/WeakChecksOnDynamicInvocation-InformationExposure/?at=master"
)

INSECURE_FUNCTIONS_NAMES = ("call",)


class InsecureFunctions(CoroutinePlugin):
    def __init__(self):
        super(InsecureFunctions, self).__init__(category="file", name="Insecure functions found",
                                                description=INSECURE_FUNCTIONS_DESCRIPTION)
        self.severity = Severity.WARNING

    def run_coroutine(self):
        while True:
            _, node = (yield)

            if isinstance(node, MethodDeclaration) and node.name in INSECURE_FUNCTIONS_NAMES:
                self.issues.append(Issue(
                    category=self.category, severity=self.severity, name=self.name,
                    description=self.description,
                    file_object=self.file_path,
                    line_number=node.position)
                )


plugin = InsecureFunctions()
