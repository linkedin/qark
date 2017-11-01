import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from modules import common, report
from modules.common import ReportIssue, Severity, terminalPrint, logger
from modules.createExploit import ExploitType
from progressbar import *
from pubsub import pub
import logging


class PluginOne(IPlugin):
    def target(self, queue):
        results = []
        #TODO: add documentation for available API calls. Sample shown below.
        # Here, we want to scan all decompiled files to see if any file contains the text "pass"
        possibleFiles = common.text_scan(common.java_files, r'pass')
        count = 0
        for f in possibleFiles:
            count += 1
            # The following call generates the progress bar in the terminal output
            pub.sendMessage('progress', bar=self.getName(), percent=round(count*100/len(possibleFiles)))

            # Mostly for logging. This goes in the log file generated under /logs
            common.logger.debug("Text found, " + str(f))
            issue = ReportIssue()

            # This will put individual results of the plugin scan in the HTML report.
            issue.setCategory(ExploitType.PLUGIN)
            issue.setDetails("The string 'pass' appears in the file: %s\n%s" % (f[1], str(f[0])))
            issue.setFile(str(f[1]))
            issue.setSeverity(Severity.VULNERABILITY)
            results.append(issue)

            # This puts individual results of the plugin scan in the terminal output.
            issue = terminalPrint()
            issue.setLevel(Severity.VULNERABILITY)
            issue.setData("The string 'pass' appears in the file: %s\n%s" % (f[1], str(f[0])))
            results.append(issue)

        # This is required to send the complete list of results (including the ones to be printed on terminal as well as
        # issues to be printed in tht HTML report) back to the main thread.
        queue.put(results)


    def getName(self):
        # The name to be displayed against the progressbar
        return "Hardcoded passwords"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target

