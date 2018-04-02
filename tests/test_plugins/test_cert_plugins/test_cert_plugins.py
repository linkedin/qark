from qark.plugins.cert.cert_validation_methods_overriden import CertValidation
from qark.plugins.cert.hostname_verifier import HostnameVerifier, ALLOW_ALL_HOSTNAME_VERIFIER_DESC


from qark.issue import Severity

import os


def test_cert_validation_methods():
    plugin = CertValidation()
    plugin.run([os.path.join(os.path.dirname(os.path.abspath(__file__)), "testCertMethodsFile.java")])
    assert 3 == len(plugin.issues)


def test_hostname_verifier():
    plugin = HostnameVerifier()
    plugin.run([os.path.join(os.path.dirname(os.path.abspath(__file__)), "testHostnameVerifier.java")])
    assert 2 == len(plugin.issues)
    assert "Allow all hostname verifier used" == plugin.issues[0].name
    assert "setHostnameVerifier set to ALLOW_ALL" == plugin.issues[1].name
    assert plugin.issues[1].line_number

    for issue in plugin.issues:
        assert Severity.WARNING == issue.severity
        assert plugin.category == issue.category
        assert ALLOW_ALL_HOSTNAME_VERIFIER_DESC == issue.description
        assert os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "testHostnameVerifier.java") == issue.file_object
