import logging
import os

import javalang
from javalang.tree import ClassCreator, MemberReference, MethodInvocation

from qark.issue import Issue, Severity
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)


class SSLSession(BasePlugin):
    """
    This plugin checks if:
     1. `AllowAllHostnameVerifier` is instantiated
     2. `setHostnameVerifier` is called with a value of `.ALLOW_ALL_HOSTNAME_VERIFIERS`
    """
    def __init__(self):
        BasePlugin.__init__(self, category="cert")
        self.severity = Severity.WARNING
        self.current_file = None
        self.tree = None
        self.ssl_sessions = []

    def _process_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                file_contents = f.read()
        except IOError:
            log.debug("Unable to read file")
            return

        try:
            self.tree = javalang.parse.parse(file_contents)
        except javalang.parser.JavaSyntaxError:
            log.debug("Couldn't parse the java file: %s", filepath)
            return

        self.current_file = filepath
        self._find_ssl_sessions()

    def _find_ssl_sessions(self):
        """
        Finds where a `SSLSession` is declared as a variable and returns instances found

        :return: SSLSession `VariableDeclaration`
        :rtype: list
        """
        a = 1


    def _set_hostname_verifier_allow_all(self):
        """Check for setHostnameVerifier with argument ALLOW_ALL_HOSTNAME_VERIFIER

        :param tree: javalang parsed tree
        """
        set_hostname_verifiers = (allow_all_verifier for _, allow_all_verifier in self.tree.filter(MethodInvocation)
                                  if allow_all_verifier.member == "setHostnameVerifier"
                                  and len(allow_all_verifier.arguments) == 1
                                  and type(allow_all_verifier.arguments[0]) is MemberReference
                                  and allow_all_verifier.arguments[0].member == "ALLOW_ALL_HOSTNAME_VERIFIER")
        for set_hostname_verifier in set_hostname_verifiers:
            self.issues.append(Issue(category=self.category, name="setHostnameVerifier set to ALLOW_ALL",
                                     severity=Severity.WARNING, description=ALLOW_ALL_HOSTNAME_VERIFIER_DESC,
                                     file_object=self.current_file, line_number=set_hostname_verifier.position))

    def run(self, files, apk_constants=None):
        relevant_files = (file_path for file_path in files if os.path.splitext(file_path.lower())[1] == '.java')
        for file_path in relevant_files:
            self._process_file(file_path)


plugin = SSLSession()
