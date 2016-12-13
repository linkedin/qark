import sys
import os
import re
import qarkMain

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from modules import common
from modules.common import ReportIssue, Severity, terminalPrint
from modules.createExploit import ExploitType
from lib.pubsub import pub


class PermissionPlugin(IPlugin):
    def target(self, queue):

        # matches 0 or 1 (?) of any number of any character after "<permission"
        perm_regex = r'<permission.*?>'
        # matches permissions with protection level set to "dangerous"
        dang_regex = r'android:protectionLevel=[\'\"]dangerous[\'\"]'
        # find full path to app manifest
        manifestPath = qarkMain.find_manifest_in_source()

        # finds all user created permissions
        perm_list = re.findall(perm_regex, common.manifest)


        # plugin scan results
        results = []
        count = 0
        for item in perm_list:
            count += 1
            # update progress bar
            pub.sendMessage('progress', bar=self.getName(), percent=round(count * 100 / len(perm_list)))

            # put results in HTML report
            issue = ReportIssue()
            issue.setCategory(ExploitType.PLUGIN)
            issue.setSeverity(Severity.VULNERABILITY)
            issue.setFile(manifestPath)

            details = ""
            if re.search(dang_regex, item):
                # found permission with protection level set to "dangerous"
                details += "User created permission with DANGEROUS protection level: %s" % item
            else:
                details += "User created permission: %s" % item

            issue.setDetails(details)
            results.append(issue)

            # put results in terminal output
            issue = terminalPrint()
            issue.setLevel(Severity.VULNERABILITY)
            issue.setData(details)
            results.append(issue)

        # send all results back to main thread
        queue.put(results)

    def getName(self):
        # The name to be displayed against the progressbar
        return "User created permissions"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target

