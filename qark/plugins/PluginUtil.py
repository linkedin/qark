import re

from modules.common import ReportIssue, Severity, terminalPrint
from modules.createExploit import ExploitType

# returns all matches of the given regex in the given group number in the supplied file
def returnGroupMatches(regex, groupNum, fileBody):
    res = []
    for match in re.finditer(regex, fileBody):
        res.append(match.group(groupNum))
    return res


# returns True if given file contains a regex match, False otherwise
def contains(regex, fileBody):
    return re.search(regex, fileBody) is not None


def reportVulnerability(fileName, details, res):
    # put results in HTML report
    issue = ReportIssue()
    issue.setCategory(ExploitType.PLUGIN)
    issue.setSeverity(Severity.VULNERABILITY)
    issue.setFile(fileName)
    issue.setDetails(details)
    res.append(issue)

    # put results in terminal output
    issue = terminalPrint()
    issue.setLevel(Severity.VULNERABILITY)
    issue.setData(details)
    res.append(issue)

def reportWarning(fileName, details, res):
    # put results in HTML report
    issue = ReportIssue()
    issue.setCategory(ExploitType.PLUGIN)
    issue.setSeverity(Severity.WARNING)
    issue.setFile(fileName)
    issue.setDetails(details)
    res.append(issue)

    # put results in terminal output
    issue = terminalPrint()
    issue.setLevel(Severity.WARNING)
    issue.setData(details)
    res.append(issue)

def reportInfo(fileName, details, res):
    # put results in HTML report
    issue = ReportIssue()
    issue.setCategory(ExploitType.PLUGIN)
    issue.setSeverity(Severity.INFO)
    issue.setFile(fileName)
    issue.setDetails(details)
    res.append(issue)

    # put results in terminal output
    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData(details)
    res.append(issue)