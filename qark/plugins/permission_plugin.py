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
    # matches 0 or 1 (?) of any number of any character after "<permission"
    permission_regex = r'<permission.*?>'
    # matches permissions with protection level set to "dangerous"
    dangerous_regex = r'android:protectionLevel=[\'\"]dangerous[\'\"]'

    def getUserCreatedPermissions(self):
        return re.findall(self.permission_regex, common.manifest)

    def isDangerousPermission(self, permission):
        # if re.search returns None, then permission is not dangerous
        return re.search(self.dangerous_regex, permission) is not None

    def target(self, queue):
        permissions = self.getUserCreatedPermissions()

        # full path to app manifest
        manifest_path = qarkMain.find_manifest_in_source()

        # plugin scan results
        results = []
        count = 0
        for permission in permissions:
            count += 1
            # update progress bar
            pub.sendMessage('progress', bar=self.getName(), percent=round(count * 100 / len(permissions)))

            # put results in HTML report
            issue = ReportIssue()
            issue.setCategory(ExploitType.PLUGIN)
            issue.setSeverity(Severity.VULNERABILITY)
            issue.setFile(manifest_path)

            details = ""
            if self.isDangerousPermission(permission):
                # found permission with protection level set to "dangerous"
                details += "User created permission with DANGEROUS protection level: %s" % permission
            else:
                details += "User created permission: %s" % permission

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

