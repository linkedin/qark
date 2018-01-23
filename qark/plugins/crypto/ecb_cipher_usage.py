import os
import logging

import re
import javalang

from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue

log = logging.getLogger(__name__)


class ECBCipherCheck(BasePlugin):
    def __init__(self):

        BasePlugin.__init__(self, category="crypto", name="ECB Cipher Usage",
                            description=("ECB mode is an insecure encryption technique and prone to data leakage"))

        self.severity = Severity.VULNERABILITY
        self.tree = None

    def _process_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                body = f.read()
        except Exception:
            log.exception("Unable to read file")
            return

        try:
            tree = javalang.parse.parse(body)
        except Exception:
            log.exception("Couldn't parse the java file: %s", filepath)

        method_invocations = tree.filter(javalang.tree.MethodInvocation)
        for node_path, method_invocation_node in method_invocations:
            try:
                method_name = method_invocation_node.member
                encryption_type = method_invocation_node.arguments[0].value
                qualifier = method_invocation_node.qualifier  # the thing that getInstance is called on
                if method_name == 'getInstance' and qualifier == 'Cipher' and re.search(r'.*/ECB/.*',
                                                                                        encryption_type):
                    description = "getInstance should not be called with ECB as the cipher mode, as it is insecure."
                    self.issues.append(
                        Issue(self.category, self.name, self.severity, description, file_object=filepath))
            except Exception:
                continue

    def run(self, files, apk_constants=None):
        relevant_files = [file_path for file_path in files if os.path.splitext(file_path)[1] == '.java']
        for file_path in relevant_files:
            self._process_file(file_path)
