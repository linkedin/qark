import json

import pytest
from qark.issue import Issue, Severity, IssueEncoder, issue_json


def test_convert_severity():
    issue = Issue(category='Test', issue_name='Test Issue', severity='INFO', description='Test')
    assert issue.severity == Severity.INFO
    issue = Issue(category='Test', issue_name='Test Issue', severity='VULNERABILITY', description='Test')
    assert issue.severity == Severity.VULNERABILITY
    issue = Issue(category='Test', issue_name='Test Issue', severity='ERROR', description='Test')
    assert issue.severity == Severity.ERROR
    issue = Issue(category='Test', issue_name='Test Issue', severity='WARNING', description='Test')
    assert issue.severity == Severity.WARNING
    issue = Issue(category='Test', issue_name='Test Issue', severity='', description='Test')
    assert issue.severity == Severity.WARNING
    issue = Issue(category='Test', issue_name='Test Issue', severity=4, description='Test')
    assert issue.severity == Severity.WARNING


def test_issue_json_single():
    issue = Issue(category='Test', issue_name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    json_output = issue_json(issue)
    json_issue = json.loads(json_output)
    assert json_issue['severity'] == issue.severity.name
    assert json_issue['name'] == issue.name


def test_issue_json_list():
    issue = Issue(category='Test', issue_name='Test Issue', severity=Severity.VULNERABILITY, description='Test')
    json_output = issue_json([issue])
    json_issue = json.loads(json_output)
    assert json_issue[0]['severity'] == issue.severity.name
    assert json_issue[0]['name'] == issue.name


def test_IssueEncoder_not_an_issue():
    issue = Severity(Severity.INFO)
    with pytest.raises(TypeError, match=r'Expecting an object of type Issue.*'):
        json.dumps(issue, cls=IssueEncoder)


def test_issue_json_dump_error():
        issue = Severity(Severity.INFO)
        assert issue_json(issue) == '"Error encoding to JSON"'
