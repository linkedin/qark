from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj
import lib.plyj.model as m
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

string = ("Be careful with use of {} permission function\nApp maybe vulnerable to Privilege escalation or "
          "Confused Deputy Attack. This function can grant access to malicious application, lacking the "
          "appropriate permission, by assuming your applications permissions. This means a malicious application, "
          "without appropriate permissions, can bypass its permission check by using your application"
          "permission to get access to otherwise denied resources. Use - {}CallingPermission instead.\n{}\n"
          "Reference: https://developer.android.com/reference/android/content/Context.html#{}\n")


def check_permission(file_name):
    return string.format("Check", "check", file_name, "checkCallingOrSelfPermission(java.lang.String)")


def enforce_permission(file_name):
    return string.format("Enforce", "enforce", file_name, "enforceCallingOrSelfPermission(java.lang.String, java.lang.String)" )


class AccessControlCheckPlugin(IPlugin):
    CHECK_PERMISSION = r'checkCallingOrSelfPermission|checkCallingOrSelfUriPermission|checkPermission'
    ENFORCE_PERMISSION = r'enforceCallingOrSelfPermission|enforceCallingOrSelfUriPermission|enforcePermission'

    def __init__(self):
        self.name = 'Access Control Checks'

    def target(self, queue):
        files = common.java_files
        global file_name
        parser = plyj.Parser()
        tree = ''
        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            file_name = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception as e:
                common.logger.exception(
                    "Unable to parse the file and generate as AST. Error: " + str(e))
            try:
                for import_decl in tree.import_declarations:
                    if 'Service' in import_decl.name.value:
                        with open(file_name, 'r') as r:
                            data = r.read()
                        if PluginUtil.contains(self.CHECK_PERMISSION, data):
                            PluginUtil.reportInfo(file_name, check_permission(file_name), res)
                            break
                        if PluginUtil.contains(self.ENFORCE_PERMISSION, data):
                            PluginUtil.reportInfo(file_name, enforce_permission(file_name), res)
                            break
            except Exception:
                pass

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
