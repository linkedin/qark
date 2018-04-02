import logging

import javalang
from javalang.tree import MethodDeclaration, MethodInvocation, ReturnStatement, StatementExpression

from qark.issue import Issue, Severity
from qark.scanner.plugin import BasePlugin
from qark.plugins.helpers import java_files_from_files

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


class CertValidation(BasePlugin):
    """
    This plugin checks if a method in `CERT_METHODS` is overriden with an insecure version that usually does not verify
    SSL connections.
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
        cert_methods = (method_declaration for _, method_declaration in tree.filter(MethodDeclaration)
                        if method_declaration.name in CERT_METHODS)
        for cert_method in cert_methods:
            if cert_method.name == "checkServerTrusted":
                self._check_server_trusted(cert_method, current_file)
            elif cert_method.name == "onReceivedSslError":
                self._on_received_ssl_error(cert_method, current_file)

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
        if len(cert_method.body) == 1 and type(cert_method.body[0]) is StatementExpression:
            for _, method_invocation in cert_method.filter(MethodInvocation):
                if method_invocation.member == "proceed":
                    self.issues.append(Issue(category=self.category, name="Unsafe implementation of onReceivedSslError",
                                             severity=self.severity,
                                             description=ON_RECEIVED_SSL_DESC,
                                             file_object=current_file,
                                             line_number=method_invocation.position))

    def run(self, files, apk_constants=None):
        relevant_files = java_files_from_files(files)
        for file_path in relevant_files:
            self._process_file(file_path)


plugin = CertValidation()
