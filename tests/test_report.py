import os

import pytest

from qark.report import Report, DEFAULT_REPORT_PATH
from qark.vulnerability import (Vulnerability, Severity)


def test_report_singleton():
    assert Report() is Report()
    report3 = Report()
    report4 = Report()
    assert report3 is report4
    report3.value = 4
    assert report4.value == 4


def test_report_html():
    report = Report()
    issue = Vulnerability(category='Test', issue_name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    report.issues.add(issue)
    report.generate_report_file()
    # We remove the issue we added to clean up after ourselves.
    report.issues.remove(issue)
    assert os.path.exists(DEFAULT_REPORT_PATH + '/report.html')