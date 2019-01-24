import logging
import re

import javalang

from qark.issue import Severity, Issue
from qark.scanner.plugin import CoroutinePlugin

log = logging.getLogger(__name__)


class RSACipherCheck(CoroutinePlugin):
    def __init__(self):

        super(RSACipherCheck, self).__init__(category="crypto", name="RSA Cipher Usage",
                                             description="RSA mode without padding is an insecure encryption technique and prone to data leakage")

        self.severity = Severity.VULNERABILITY

    def run_coroutine(self):
        while True:
            _, method_invocation = (yield)

            if not isinstance(method_invocation, javalang.tree.MethodInvocation):
                continue

            try:
                method_name = method_invocation.member
                encryption_type = method_invocation.arguments[0].value
                qualifier = method_invocation.qualifier  # the thing that getInstance is called on
                if method_name == 'getInstance' and qualifier == 'Cipher' and re.search(r'RSA/.+/NoPadding',
                                                                                        encryption_type):
                    description = "getInstance should not be called with RSA without padding as the cipher mode, as it is insecure."
                    self.issues.append(
                        Issue(self.category, self.name, self.severity, description, file_object=self.file_path))
            except Exception:
                continue


plugin = RSACipherCheck()
