import json

from qark.issue import Issue, Severity, issue_json


def test_convert_severity():
    issue = Issue(category='Test', name='Test Issue', severity='INFO', description='Test')
    assert issue.severity == Severity.INFO
    issue = Issue(category='Test', name='Test Issue', severity='VULNERABILITY', description='Test')
    assert issue.severity == Severity.VULNERABILITY
    issue = Issue(category='Test', name='Test Issue', severity='ERROR', description='Test')
    assert issue.severity == Severity.ERROR
    issue = Issue(category='Test', name='Test Issue', severity='WARNING', description='Test')
    assert issue.severity == Severity.WARNING
    issue = Issue(category='Test', name='Test Issue', severity='', description='Test')
    assert issue.severity == Severity.WARNING
    issue = Issue(category='Test', name='Test Issue', severity=4, description='Test')
    assert issue.severity == Severity.WARNING


def test_issue_json_single():
    issue = Issue(category='Test', name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    json_output = issue_json(issue)
    json_issue = json.loads(json_output)
    assert json_issue['severity'] == issue.severity.name
    assert json_issue['name'] == issue.name


def test_issue_json_list():
    issue = Issue(category='Test', name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    json_output = issue_json([issue])
    json_issue = json.loads(json_output)
    assert json_issue[0]['severity'] == issue.severity.name
    assert json_issue[0]['name'] == issue.name
