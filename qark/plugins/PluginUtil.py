from modules.common import ReportIssue, Severity, terminalPrint
from modules.createExploit import ExploitType


def reportIssue(fileName, details, results):
    # put results in HTML report
    issue = ReportIssue()
    issue.setCategory(ExploitType.PLUGIN)
    issue.setSeverity(Severity.VULNERABILITY)
    issue.setFile(fileName)
    issue.setDetails(details)
    results.append(issue)

    # put results in terminal output
    issue = terminalPrint()
    issue.setLevel(Severity.VULNERABILITY)
    issue.setData(details)
    results.append(issue)