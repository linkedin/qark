import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')
from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj


class AccessControlCheckPlugin(IPlugin):

    CHECK_PERMISSION = r'checkCallingOrSelfPermission|checkCallingOrSelfUriPermission|checkPermission'
    ENFORCE_PERMISSION = r'enforceCallingOrSelfPermission|enforceCallingOrSelfUriPermission|enforcePermission'

    def __init__(self):
        self.name = 'Access Control Checks'

    def target(self, queue):
        files = common.java_files
        global parser, tree, fileName
        parser = plyj.Parser()
        tree = ''
        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            fileName = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception:
                continue
            try:
                for import_decl in tree.import_declarations:
                    if 'Service' in import_decl.name.value:
                        fileBody = str(open(fileName, 'r').read())
                        if PluginUtil.contains(self.CHECK_PERMISSION, fileBody):
                            PluginUtil.reportWarning(fileName, self.CheckPermissionIssueDetails(fileName), res)
                            break
                        if PluginUtil.contains(self.ENFORCE_PERMISSION, fileBody):
                            PluginUtil.reportWarning(fileName, self.EnforcePermissionIssueDetails(fileName), res)
                            break
            except Exception:
                continue

        queue.put(res)

    def CheckPermissionIssueDetails(self, fileName):
        return 'Inappropriate use of Check Permissions \n' \
               'These functions should be used with care as they can grant access ' \
               'to malicious applications, lacking the appropriate permissions, by assuming your applications permissions.' \
               'This means a malicious application, without appropriate permissions, can bypass its permission check by using your application ' \
               'permission to get access to otherwise denied resources. This can result in what is known as the confused deputy attack.' \
               'Use - checkCallingPermission instead.\n%s.\n' \
               'Reference: https://developer.android.com/reference/android/content/Context.html#checkCallingOrSelfPermission(java.lang.String)\n' \
               % fileName

    def EnforcePermissionIssueDetails(self, fileName):
        return 'Inappropriate use of Enforce Permissions \n ' \
               'App is vulnerable to Privilege escalation or Confused Deputy Attack. \n' \
               'Use - enforceCallingPermission instead. This is done to protect against accidentally leaking permissions.\n%s.\n' \
               'Reference: https://developer.android.com/reference/android/content/Context.html#enforceCallingOrSelfPermission(java.lang.String, java.lang.String)\n' \
               % fileName

    def getName(self):
        return "Access Control Checks"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target