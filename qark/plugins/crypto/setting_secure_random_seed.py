import logging

import javalang

from qark.issue import Severity, Issue
from qark.scanner.plugin import CoroutinePlugin

log = logging.getLogger(__name__)


class SeedWithSecureRandom(CoroutinePlugin):

    INSECURE_FUNCTIONS = ("setSeed", "generateSeed")

    def __init__(self):

        super(SeedWithSecureRandom, self).__init__(category="crypto",
                                                   name="Random number generator is seeded with SecureSeed",
                                                   description=(
                                                       "Specifying a fixed seed will cause a predictable sequence of numbers. "
                                                       "This may be useful for testing, but not for secure use"))

        self.severity = Severity.WARNING

    def _imports_secure_seed(self, tree):
        """Checks if a tree imports java.security.SecureRandom, and returns True if the import exists"""
        return any(imp.path == "java.security.SecureRandom" for imp in tree.imports)

    def can_run_coroutine(self):
        return self._imports_secure_seed(self.java_ast)

    def run_coroutine(self):
        while True:
            _, method_invocation = (yield)

            if not isinstance(method_invocation, javalang.tree.MethodInvocation):
                continue

            if method_invocation.member in SeedWithSecureRandom.INSECURE_FUNCTIONS:
                self.issues.append(Issue(self.category, self.name, self.severity, self.description,
                                         file_object=self.file_path))


plugin = SeedWithSecureRandom()
