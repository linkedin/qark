import logging

from javalang.tree import MethodDeclaration, MethodInvocation, ReturnStatement, StatementExpression

from qark.issue import Issue, Severity
from qark.scanner.plugin import CoroutinePlugin

log = logging.getLogger(__name__)

CERT_METHODS = ("checkServerTrusted", "onReceivedSslError")
CHECK_SERVER_TRUSTED = "Instance of checkServerTrusted, with empty body found. "
ON_RECEIVED_SSL_DESC = ("Specifically, the implementation ignores all SSL certificate validation errors, making your "
                        "app vulnerable to man-in-the-middle attacks. To properly handle SSL certificate validation, "
                        "change your code to invoke SslErrorHandler.cancel(). For details, please see: "
                        "https://developer.android.com/reference/android/webkit/WebViewClient.html")
MITM_DESCRIPTION = ("This means this application is likely "
                    "vulnerable to Man-In-The-Middle attacks. This can be confirmed using the free version of "
                    "Burpsuite. Simply set the Android device's proxy to use Burpsuite via the network settings, "
                    "but DO NOT install the Portswigger CA certificate on the device. If you still see traffic in the "
                    "proxy, the app is vulnerable. Note: You need to ensure you exercise this code path. If you are "
                    "unsure, make sure you click through each part of the application which makes network requests. "
                    "You may need to toggle the proxy on/off to get past sections that do validate certificates "
                    "properly in order to reach the vulnerable code. This proves that it will accept certificates "
                    "from any CA. You should always validate your configuration by visiting an HTTPS site in the "
                    "native browser and verifying you receive a certificate warning. For details, please see: "
                    "https://developer.android.com/training/articles/security-ssl.html")


class CertValidation(CoroutinePlugin):
    """
    This plugin checks if a method in `CERT_METHODS` is overriden with an insecure version that usually does not verify
    SSL connections.
    """
    def __init__(self):
        super(CertValidation, self).__init__(category="cert", name="Certification Validation")
        self.severity = Severity.WARNING

    def run_coroutine(self):
        while True:
            _, method_declaration = (yield)

            if not isinstance(method_declaration, MethodDeclaration) or method_declaration.name not in CERT_METHODS:
                continue

            if method_declaration.name == "checkServerTrusted":
                self._check_server_trusted(method_declaration, self.file_path)
            elif method_declaration.name == "onReceivedSslError":
                self._on_received_ssl_error(method_declaration, self.file_path)

    def _check_server_trusted(self, cert_method, current_file):
        """
        Determines if the `checkServerTrusted` method is overriden with either no function body (defaults to allow)
        or if the body just returns.
        """
        if not cert_method.body:
            self.issues.append(Issue(category=self.category, name="Empty certificate method",
                                     severity=self.severity,
                                     description=CHECK_SERVER_TRUSTED + MITM_DESCRIPTION,
                                     file_object=current_file,
                                     line_number=cert_method.position))
        elif len(cert_method.body) == 1 and type(cert_method.body[0]) is ReturnStatement:
            self.issues.append(Issue(category=self.category, name="Empty (return) certificate method",
                                     severity=self.severity,
                                     description=CHECK_SERVER_TRUSTED + MITM_DESCRIPTION,
                                     file_object=current_file,
                                     line_number=cert_method.position))

    def _on_received_ssl_error(self, cert_method, current_file):
        """
        Determines if the `onReceivedSslError` method is overriden with a body of `handler.proceed()` which will
        drop SSL errors.
        """
        if cert_method.body and len(cert_method.body) == 1 and type(cert_method.body[0]) is StatementExpression:
            for _, method_invocation in cert_method.filter(MethodInvocation):
                if method_invocation.member == "proceed":
                    self.issues.append(Issue(category=self.category, name="Unsafe implementation of onReceivedSslError",
                                             severity=self.severity,
                                             description=ON_RECEIVED_SSL_DESC,
                                             file_object=current_file,
                                             line_number=method_invocation.position))


plugin = CertValidation()
