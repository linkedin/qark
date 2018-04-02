import os
import logging

import javalang

from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files

log = logging.getLogger(__name__)


class SeedWithSecureRandom(BasePlugin):

    INSECURE_FUNCTIONS = ("setSeed", "generateSeed")

    def __init__(self):

        BasePlugin.__init__(self, category="crypto", name="Random number generator is seeded with SecureSeed",
                            description=("Specifying a fixed seed will cause a predictable sequence of numbers. "
                                         "This may be useful for testing, but not for secure use"))

        self.severity = Severity.WARNING

    def _imports_secure_seed(self, tree):
        """Checks if a tree imports java.security.SecureRandom, and returns True if the import exists"""
        return any([imp.path == "java.security.SecureRandom" for imp in tree.imports])

    def _process_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                body = f.read()
        except Exception:
            log.exception("Unable to read file")
            return

        try:
            tree = javalang.parse.parse(body)
        except (javalang.parser.JavaSyntaxError, IndexError):
            log.debug("Couldn't parse the java file: %s", filepath)
            return

        if not self._imports_secure_seed(tree):  # doesn't import the insecure function
            return

        method_invocations = tree.filter(javalang.tree.MethodInvocation)
        for _, method_invocation_node in method_invocations:
            if method_invocation_node.member in SeedWithSecureRandom.INSECURE_FUNCTIONS:
                self.issues.append(Issue(self.category, self.name, self.severity, self.description,
                                         file_object=filepath))

    def run(self, files, apk_constants=None):
        relevant_files = java_files_from_files(files)
        for file_path in relevant_files:
            self._process_file(file_path)


plugin = SeedWithSecureRandom()
