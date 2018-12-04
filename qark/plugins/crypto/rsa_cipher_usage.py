import os
import logging

import re
import javalang

from qark.scanner.plugin import JavaASTPlugin
from qark.issue import Severity, Issue

log = logging.getLogger(__name__)


class RSACipherCheck(JavaASTPlugin):
    def __init__(self):

        super(RSACipherCheck, self).__init__(category="crypto", name="RSA Cipher Usage",
                                             description="RSA mode without padding is an insecure encryption technique and prone to data leakage")

        self.severity = Severity.VULNERABILITY

    def run(self):
        method_invocations = self.java_ast.filter(javalang.tree.MethodInvocation)
        for _, method_invocation_node in method_invocations:
            try:
                method_name = method_invocation_node.member
                encryption_type = method_invocation_node.arguments[0].value
                qualifier = method_invocation_node.qualifier  # the thing that getInstance is called on
                if method_name == 'getInstance' and qualifier == 'Cipher' and re.search(r'RSA/.+/NoPadding',
                                                                                        encryption_type):
                    description = "getInstance should not be called with RSA without padding as the cipher mode, as it is insecure."
                    self.issues.append(
                        Issue(self.category, self.name, self.severity, description, file_object=self.file_path))
            except Exception:
                continue


plugin = RSACipherCheck()
