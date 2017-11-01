from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from pubsub import pub
import lib.plyj.parser as plyj
import lib.plyj.model as m
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

STRING = ("Be careful with use of {} permission function\nApp maybe vulnerable to Privilege escalation or "
          "Confused Deputy Attack. This function can grant access to malicious application, lacking the "
          "appropriate permission, by assuming your applications permissions. This means a malicious application, "
          "without appropriate permissions, can bypass its permission check by using your application"
          "permission to get access to otherwise denied resources. Use - {}CallingPermission instead.\nFilepath: {}\n"
          "Reference: https://developer.android.com/reference/android/content/Context.html#{}\n")


def check_permission(filepath):
    return STRING.format("Check", "check", filepath, "checkCallingOrSelfPermission(java.lang.String)")


def enforce_permission(filepath):
    return STRING.format("Enforce", "enforce", filepath, "enforceCallingOrSelfPermission(java.lang.String, java.lang.String)")


class AccessControlCheckPlugin(IPlugin):
    CHECK_PERMISSION = r'checkCallingOrSelfPermission|checkCallingOrSelfUriPermission|checkPermission'
    ENFORCE_PERMISSION = r'enforceCallingOrSelfPermission|enforceCallingOrSelfUriPermission|enforcePermission'

    def __init__(self):
        self.name = 'Access Control Checks'

    def target(self, queue):
        files = common.java_files
        global filepath, tree
        parser = plyj.Parser()
        tree = ''
        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            filepath = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception as e:
                common.logger.exception("Unable to parse the file and generate as AST. Error: " + str(e))
                continue

            try:
                for import_decl in tree.import_declarations:
                    if 'Service' in import_decl.name.value:
                        with open(filepath, 'r') as r:
                            data = r.read()
                        if PluginUtil.contains(self.CHECK_PERMISSION, data):
                            PluginUtil.reportInfo(filepath, check_permission(filepath), res)
                            break
                        if PluginUtil.contains(self.ENFORCE_PERMISSION, data):
                            PluginUtil.reportInfo(filepath, enforce_permission(filepath), res)
                            break
            except Exception as e:
                common.logger.debug("Plyj parser failed while parsing the file: " + filepath + "\nError" + str(e))
                continue

        queue.put(res)

    @staticmethod
    def getName():
        return "Access Control Checks"

    @staticmethod
    def getCategory():
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
