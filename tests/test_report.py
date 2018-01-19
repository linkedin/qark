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


def test_report_with_report_path():
    assert Report(report_path=DEFAULT_REPORT_PATH) is Report(report_path=DEFAULT_REPORT_PATH)


def test_report_html_defaults():
    report = Report()
    issue = Vulnerability(category='Test', issue_name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    report.issues.append(issue)
    report.generate_report_file()
    # We remove the issue we added to clean up after ourselves.
    report.issues.remove(issue)
    assert os.path.exists(os.path.join(DEFAULT_REPORT_PATH, 'report.html'))
    # We remove the report, to clean up after ourselves
    os.remove(os.path.join(DEFAULT_REPORT_PATH, 'report.html'))


def test_report_html_custom_template():
    report = Report()
    issue = Vulnerability(category='Test', issue_name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    report.issues.append(issue)
    report.generate_report_file(template_file=os.path.join('templates', 'html_report.jinja'))
    # We remove the issue we added to clean up after ourselves.
    report.issues.remove(issue)
    assert os.path.exists(os.path.join(DEFAULT_REPORT_PATH, 'report.html'))
    # We remove the report, to clean up after ourselves
    os.remove(os.path.join(DEFAULT_REPORT_PATH, 'report.html'))