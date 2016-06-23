from yapsy.IPlugin import IPlugin
from modules import common, report
from modules.common import ReportIssue, Severity, terminalPrint, logger
from modules.createExploit import ExploitType
from lib.progressbar import *
from lib.pubsub import pub
from qark import lock
import logging


class PluginTwo(IPlugin):
    def target(self, queue):
        results = []
        possibleFiles = common.text_scan(common.java_files, r'HashMap')
        count = 0
        for f in possibleFiles:
            count += 1
            pub.sendMessage('progress', bar='hash_plugin', percent=round(count*100/len(possibleFiles)))
            common.logger.debug("Text found, " + str(f))
            issue = ReportIssue()
            issue.setCategory(ExploitType.PLUGIN)
            issue.setDetails("The string 'HashMap' appears in the file: %s" % f[1])
            issue.setFile(str(f[1]))
            issue.setSeverity(Severity.VULNERABILITY)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.VULNERABILITY)
            issue.setData("The string appears in the file: " + f[1])
            results.append(issue)
        
        queue.put(results)

    def getName(self):
        return "hash_plugin"

    def getCategory(self):
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target

