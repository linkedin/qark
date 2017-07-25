from plugins import PluginUtil
from modules.createExploit import ExploitType
from modules.common import Severity


def testZeroGroupMatches():
    assert len(PluginUtil.returnGroupMatches(r'(test123)', 1, 'test321')) == 0


def testOneGroupMatch():
    res = PluginUtil.returnGroupMatches(r'(test123)', 1, 'test321test123test321')
    assert len(res) == 1
    assert res[0] == 'test123'


def testTwoGroupMatches():
    res = PluginUtil.returnGroupMatches(r'(test123)', 1, 'test123test321test123')
    assert len(res) == 2
    assert res[0] == 'test123'
    assert res[1] == 'test123'


def testContains():
    assert PluginUtil.contains(r'test123', 'test123') is True


def testNotContains():
    assert PluginUtil.contains(r'test123', 'test321') is False


def testReportIssue():
    res = []
    PluginUtil.reportVulnerability('fileName', 'details', res)
    assert len(res) == 2
    assert res[0].getCategory() == ExploitType.PLUGIN
    assert res[0].getSeverity() == Severity.VULNERABILITY
    assert res[0].getFile() == 'fileName'
    assert res[0].getDetails() == 'details'
    assert res[1].getLevel() == Severity.VULNERABILITY
    assert res[1].getData() == 'details'

def testReportIssue1():
    res = []
    PluginUtil.reportWarning('fileName', 'details', res)
    assert len(res) == 2
    assert res[0].getCategory() == ExploitType.PLUGIN
    assert res[0].getSeverity() == Severity.WARNING
    assert res[0].getFile() == 'fileName'
    assert res[0].getDetails() == 'details'
    assert res[1].getLevel() == Severity.WARNING
    assert res[1].getData() == 'details'

def testReportIssue2():
    res = []
    PluginUtil.reportInfo('fileName', 'details', res)
    assert len(res) == 2
    assert res[0].getCategory() == ExploitType.PLUGIN
    assert res[0].getSeverity() == Severity.INFO
    assert res[0].getFile() == 'fileName'
    assert res[0].getDetails() == 'details'
    assert res[1].getLevel() == Severity.INFO
    assert res[1].getData() == 'details'

if __name__ == '__main__':
    testZeroGroupMatches()
    testOneGroupMatch()
    testTwoGroupMatches()
    testContains()
    testNotContains()
    testReportIssue()
    testReportIssue1()
    testReportIssue2()
