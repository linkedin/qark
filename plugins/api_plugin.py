import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from modules import common, report
from modules.common import ReportIssue, Severity, terminalPrint, logger
from modules.createExploit import ExploitType
from lib.progressbar import *
from lib.pubsub import pub
import logging


class PluginOne(IPlugin):
    def target(self, queue):
        results = []
        possibleFiles = common.text_scan(common.java_files, r'API_KEY')
        count = 0
        for f in possibleFiles:
            count += 1
            pub.sendMessage('progress', bar=self.getName(), percent=round(count*100/len(possibleFiles)))
            common.logger.debug("Text found, " + str(f))
            issue = ReportIssue()
            issue.setCategory(ExploitType.PLUGIN)
            issue.setDetails("The string 'API_KEY' appears in the file: %s\n%s" % (f[1], str(f[0])))
            issue.setFile(str(f[1]))
            issue.setSeverity(Severity.VULNERABILITY)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.VULNERABILITY)
            issue.setData("The string 'API_KEY' appears in the file: %s\n%s" % (f[1], str(f[0])))
            results.append(issue)
        
        
        queue.put(results)
            

    def getName(self):
        return "Hardcoded API Key Check"

    def getCategory(self):
        return "Hardcoded API keys"

    def getTarget(self):
        return self.target

