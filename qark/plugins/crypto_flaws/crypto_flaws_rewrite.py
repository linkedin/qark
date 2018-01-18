
import logging

import re, sys
from plyj.parser import Parser
import plyj.model as m

from qark.scanner.plugin import BasePlugin
from qark.vulnerability import Severity, Vulnerability

log = logging.getLogger(__name__)


class PackagedPrivateKeys(BasePlugin):

    def __init__(self):

        BasePlugin.__init__(self, category="crypto", issue_name="Encryption keys are packaged with the application")

        self.severity = Severity.VULNERABILITY

    def run(self, file_object):
        if run_regex(file_object, r'PRIVATE\sKEY'):
            log.info("It appears there is a private key embedded in your application: %s", file_object)
            description = "It appears there is a private key embedded in your application in the following file:"
            self.issues.append(Vulnerability(self.category, self.issue_name, self.severity, description, file_object=file_object))


class SeedWithSecureRandom(BasePlugin):

    def __init__(self):

        BasePlugin.__init__(self, category="crypto", issue_name="Random number generator is seeded with SecureSeed",
                            description=("Specifying a fixed seed will cause a predictable sequence of numbers. "
                                         "This may be useful for testing, but not for secure use"))

        self.severity = Severity.WARNING
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

        for import_decl in self.tree.import_declarations:
            for setter_func in ("setSeed", "generateSeed"):
                if 'SecureRandom' in import_decl.name.value and setter_func in str(self.tree):
                    self.issues.append(Vulnerability(self.category, self.issue_name, self.severity, self.description, file_object=file_object))


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

def run_regex(filename, rex):
    """
    Read a file line by line, run a regular expression against the content and return list of things that require inspection
    """
    things_to_inspect = []
    try:
        with open(filename) as f:
            content = f.readlines()
            for y in content:
                if re.search(rex, y):
                    if re.match(r'^\s*(\/\/|\/\*)', y):  # exclude single-line or beginning comments
                        pass
                    elif re.match(r'^\s*\*', y):  # exclude lines that are comment bodies
                        pass
                    elif re.match(r'.*\*\/$', y):  # exclude lines that are closing comments
                        pass
                    elif re.match(r'^\s*Log\..\(', y):  # exclude Logging functions
                        pass
                    elif re.match(r'(.*)(public|private)\s(String|List)', y):  # exclude declarations
                        pass
                    else:
                        things_to_inspect.append(y)
    except Exception as e:
        log.error("Unable to read file: " + str(filename) + " results will be inaccurate")
    return things_to_inspect

if __name__ == '__main__':
    aoeu = PackagedPrivateKeys()
    aoeu.run('/tmp/aoeu')
    import pdb
    pdb.set_trace()
