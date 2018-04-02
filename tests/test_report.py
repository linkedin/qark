import os

import pytest

from qark.report import Report, DEFAULT_REPORT_PATH
from qark.issue import (Issue, Severity)


def test_report_singleton():
    assert Report() is Report()
    report3 = Report()
    report4 = Report()
    assert report3 is report4
    report3.value = 4
    assert report4.value == 4


def test_report_with_report_path():
    assert Report(report_path=DEFAULT_REPORT_PATH) is Report(report_path=DEFAULT_REPORT_PATH)


    # Currently the reports are placeholders which do not generate the full final report.
    # Once the reports are finalized their contents will be tested.


def test_report_html_defaults():
    report = Report()
    issue = Issue(category='Test', name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    report.issues.append(issue)
    report.generate()
    # We remove the issue we added to clean up after ourselves.
    report.issues.remove(issue)
    assert os.path.exists(os.path.join(DEFAULT_REPORT_PATH, 'report.html'))
    # We remove the report, to clean up after ourselves
    os.remove(os.path.join(DEFAULT_REPORT_PATH, 'report.html'))


def test_report_xml_defaults():
    report = Report()
    issue = Issue(category='Test', name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    report.issues.append(issue)
    report.generate(file_type='xml')
    # We remove the issue we added to clean up after ourselves.
    report.issues.remove(issue)
    assert os.path.exists(os.path.join(DEFAULT_REPORT_PATH, 'report.xml'))
    # We remove the report, to clean up after ourselves
    os.remove(os.path.join(DEFAULT_REPORT_PATH, 'report.xml'))


def test_report_csv_defaults():
    report = Report()
    issue = Issue(category='Test', name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    report.issues.append(issue)
    report.generate(file_type='csv')
    # We remove the issue we added to clean up after ourselves.
    report.issues.remove(issue)
    assert os.path.exists(os.path.join(DEFAULT_REPORT_PATH, 'report.csv'))
    # We remove the report, to clean up after ourselves
    os.remove(os.path.join(DEFAULT_REPORT_PATH, 'report.csv'))


def test_report_json_defaults():
    report = Report()
    issue = Issue(category='Test', name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    report.issues.append(issue)
    report.generate(file_type='json')
    # We remove the issue we added to clean up after ourselves.
    report.issues.remove(issue)
    assert os.path.exists(os.path.join(DEFAULT_REPORT_PATH, 'report.json'))
    # We remove the report, to clean up after ourselves
    os.remove(os.path.join(DEFAULT_REPORT_PATH, 'report.json'))


def test_report_html_custom_template():
    report = Report()
    issue = Issue(category='Test', name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    report.issues.append(issue)
    report.generate(template_file=os.path.join('templates', 'html_report.jinja'))
    # We remove the issue we added to clean up after ourselves.
    report.issues.remove(issue)
    assert os.path.exists(os.path.join(DEFAULT_REPORT_PATH, 'report.html'))
    # We remove the report, to clean up after ourselves
    os.remove(os.path.join(DEFAULT_REPORT_PATH, 'report.html'))