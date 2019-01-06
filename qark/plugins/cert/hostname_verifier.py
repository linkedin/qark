import logging

from javalang.tree import ClassCreator, MemberReference, MethodInvocation

from qark.issue import Issue, Severity
from qark.scanner.plugin import CoroutinePlugin

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


class HostnameVerifier(CoroutinePlugin):
    """
    This plugin checks if:
     1. `AllowAllHostnameVerifier` is instantiated
     2. `setHostnameVerifier` is called with a value of `.ALLOW_ALL_HOSTNAME_VERIFIERS`
    """
    def __init__(self):
        super(HostnameVerifier, self).__init__(category="cert", name="Hostname Verifier")
        self.severity = Severity.WARNING

    def run_coroutine(self):
        while True:
            _, class_ = (yield)

            if isinstance(class_, ClassCreator):
                if class_.type.name == "AllowAllHostnameVerifier":
                    self.issues.append(Issue(category=self.category, name="Allow all hostname verifier used",
                                             severity=Severity.WARNING, description=ALLOW_ALL_HOSTNAME_VERIFIER_DESC,
                                             file_object=self.file_path))

                elif class_.type.name == "NullHostNameVerifier" or class_.type.name == "NullHostnameVerifier":
                    self.issues.append(Issue(category=self.category, name="Allow all hostname verifier used",
                                             severity=Severity.WARNING, description=ALLOW_ALL_HOSTNAME_VERIFIER_DESC,
                                             file_object=self.file_path))

            elif isinstance(class_, MethodInvocation):
                if (class_.member == "setHostnameVerifier"
                        and len(class_.arguments) == 1
                        and type(class_.arguments[0]) is MemberReference
                        and class_.arguments[0].member == "ALLOW_ALL_HOSTNAME_VERIFIER"):
                    self.issues.append(Issue(category=self.category, name="setHostnameVerifier set to ALLOW_ALL",
                                             severity=Severity.WARNING, description=ALLOW_ALL_HOSTNAME_VERIFIER_DESC,
                                             file_object=self.file_path, line_number=class_.position))


plugin = HostnameVerifier()
