import logging

import javalang
from javalang.tree import ClassCreator, MemberReference, MethodInvocation

from qark.issue import Issue, Severity
from qark.scanner.plugin import BasePlugin
from qark.plugins.helpers import java_files_from_files

log = logging.getLogger(__name__)

ALLOW_ALL_HOSTNAME_VERIFIER_DESC = ("This can allow for impromper x.509 certificate validation wherein the DNS "
                                    "hostname does not match the Common or Subject Alternative Name(s) on the "
                                    "certificate, making the application vulnerable to Man-In-The-Middle attacks. "
                                    "This means the application may potentially accept a certificate from any trusted "
                                    "CA, regardless of the domain it was issued for. The can be validated using the "
                                    "free version of Burpsuite by installing the Portswigger CA certificate, thereby "
                                    "making it a trusted CA on the device. Set the device network settings to use the "
                                    "Burpsuite proxy, then go Proxy > Options > Edit the Proxy Listener by changing "
                                    "the Certificate tab to Generate a CA-signed certificate with a specific hostname "
                                    "and enter a domain like foobar.com which doesn't match the domain name(s) the app "
                                    "is connecting to normally. You should always verify your results by visiting an "
                                    "https site in the native browser and confirming you see a certificate warning. "
                                    "For details, please see: "
                                    "https://developer.android.com/training/articles/security-ssl.html")


class HostnameVerifier(BasePlugin):
    """
    This plugin checks if:
     1. `AllowAllHostnameVerifier` is instantiated
     2. `setHostnameVerifier` is called with a value of `.ALLOW_ALL_HOSTNAME_VERIFIERS`
    """
    def __init__(self):
        BasePlugin.__init__(self, category="cert")
        self.severity = Severity.WARNING

    def _process_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                file_contents = f.read()
        except IOError:
            log.debug("Unable to read file")
            return

        try:
            tree = javalang.parse.parse(file_contents)
        except (javalang.parser.JavaSyntaxError, IndexError):
            log.debug("Couldn't parse the java file: %s", filepath)
            return

        current_file = filepath
        self._allow_all_hostname_verifier_created(tree, current_file)
        self._set_hostname_verifier_allow_all(tree, current_file)

    def _allow_all_hostname_verifier_created(self, tree, current_file):
        """
        Checks for a class creation of `AllowAllHostnameVerifier`.

        :param tree: javalang parsed tree
        """
        hostname_verifiers = [hostname_verifier for _, hostname_verifier in tree.filter(ClassCreator)
                              if hostname_verifier.type.name == "AllowAllHostnameVerifier"]
        if hostname_verifiers:
            self.issues.append(Issue(category=self.category, name="Allow all hostname verifier used",
                                     severity=Severity.WARNING, description=ALLOW_ALL_HOSTNAME_VERIFIER_DESC,
                                     file_object=current_file))

    def _set_hostname_verifier_allow_all(self, tree, current_file):
        """Check for setHostnameVerifier with argument ALLOW_ALL_HOSTNAME_VERIFIER

        :param tree: javalang parsed tree
        """
        set_hostname_verifiers = (allow_all_verifier for _, allow_all_verifier in tree.filter(MethodInvocation)
                                  if allow_all_verifier.member == "setHostnameVerifier"
                                  and len(allow_all_verifier.arguments) == 1
                                  and type(allow_all_verifier.arguments[0]) is MemberReference
                                  and allow_all_verifier.arguments[0].member == "ALLOW_ALL_HOSTNAME_VERIFIER")
        for set_hostname_verifier in set_hostname_verifiers:
            self.issues.append(Issue(category=self.category, name="setHostnameVerifier set to ALLOW_ALL",
                                     severity=Severity.WARNING, description=ALLOW_ALL_HOSTNAME_VERIFIER_DESC,
                                     file_object=current_file, line_number=set_hostname_verifier.position))

    def run(self, files, apk_constants=None):
        relevant_files = java_files_from_files(files)
        for file_path in relevant_files:
            self._process_file(file_path)


plugin = HostnameVerifier()
