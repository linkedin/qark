import logging

import re
from plyj.parser import Parser
import plyj.model as m

from qark.scanner.plugin import BasePlugin
from qark.vulnerability import Severity, Vulnerability

log = logging.getLogger(__name__)

class ECBCipherCheck(BasePlugin):

    def __init__(self):

        BasePlugin.__init__(self, category="crypto", issue_name="ECB Cipher Usage",
                            description=("ECB mode is an insecure encryption technique and prone to data leakage"))

        self.severity = Severity.VULNERABILITY
        self.parser = Parser()
        self.tree = None


    def run(self, file_object):
        try:
            self.tree = self.parser.parse_file(file_object)
            if not self.tree:
                return
        except Exception:
            log.exception("Unable to create tree for %s" + str(file_object))
            return
        class_declaration_bodies = [type_decl.body for type_decl in self.tree.type_declarations if type(type_decl) is m.ClassDeclaration]
        for body in class_declaration_bodies:
            try:
                self._recursive_ecb_check_final(body, file_object)
            except:
                log.exception("Error running recursive_ecb_check in cryptoFlaws.py")


    def _ecb_method_invocation_check(self, token, filepath):
        for literal in [x for x in token.arguments if type(x) is m.Literal]:
            # sets mode to ECB
            if re.search(r'.*\/ECB\/.*', str(literal.value)):
                description = "getInstance should not be called with ECB as the cipher mode, as it is insecure."
                self.issues.append(Vulnerability(self.category, self.issue_name, self.severity, description, file_object=filepath))
            # sets mode to something other than ECB
            elif re.search(r'.*/.*/.*', str(literal.value)):
                return
            # No mode set
            elif str(literal.value) == '':
                description = "getInstance should not be called with ECB as the cipher mode, as it is insecure."
                self.issues.append(Vulnerability(self.category, self.issue_name, self.severity, description, file_object=filepath))


    def _is_target_function(self, token):
        # TODO - need to verify .getInstance is actually being invoked on a Cipher object
        is_method_invocation = type(token) is m.MethodInvocation
        is_correct_function_name = getattr(token, 'name', None) == 'getInstance'
        has_arguments = hasattr(token, 'arguments')
        return all((is_method_invocation, is_correct_function_name, has_arguments))


    def _recursive_ecb_check_final(self, token, filepath):
        if self._is_target_function(token):
            self._ecb_method_invocation_check(token, filepath)
        elif type(token) is list:
            for item in token:
                self._recursive_ecb_check_final(item, filepath)
        elif hasattr(token, 'fields'):
            for field in token.fields:
                self._recursive_ecb_check_final(getattr(token, field), filepath)
