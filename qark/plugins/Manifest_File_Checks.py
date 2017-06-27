import sys
import os
import re
import qarkMain

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub


class PermissionPlugin(IPlugin):

    def target(self, queue):
        f = str(common.manifest)
        # plugin scan results
        res = []
        count = 0
        global fileName
        # full path to app manifest
        fileName = qarkMain.find_manifest_in_source()
        for line in f.splitlines():
            count += 1
            # update progress bar
            pub.sendMessage('progress', bar=self.getName(), percent=round(count * 100 / len(f.splitlines())))
            if "provider" in line:
                if "exported" and "true" in line:
                    if not any(re.findall(r'readPermission|writePermission|signature', line)):
                        PluginUtil.reportIssue(fileName, self.createIssueDetails(line), res)

        for line in f.splitlines():
            # Matches android:path which is set to "/"
            uri_regex = r'android:path=[\'\"]/[\'\"]'
            # Matches android:pathPrefix which is set to "/"
            uri1_regex = r'android:pathPrefix=[\'\"]/[\'\"]'
            if any(re.findall(r'grant-uri-permission|path-permission', line)):
                if re.findall(uri_regex, line) or re.findall(uri1_regex, line):
                    PluginUtil.reportIssue(fileName, self.createIssueDetails1(line), res)

        # Check for google safebrowsing API
        if "WebView" in f.splitlines():
            if "EnableSafeBrowsing" and "true" not in f.splitlines():
                PluginUtil.reportIssue(fileName, self.createIssueDetails2(fileName), res)

        # send all results back to main thread
        queue.put(res)

    def createIssueDetails(self, line):
        return '%s \nIf your content provider is just for your apps use then set it to be android:exported=false in the manifest.\n' \
               'If you are intentionally exporting the content provider then you should also specify one or more permissions for reading and writing. \n'\
                'If you are using a content provider for sharing data between only your own apps, ' \
                'it is preferable to use the android:protectionLevel attribute set to signature protection. \n'\
               % line

    def createIssueDetails1(self, line):
        return '%s \nInsecure path permission set in the manifest.\n' \
               'If path prefix / means entire file system of android has access.\n' \
               % line

    def createIssueDetails2(self, fileName):
        return 'To provide users with a safer browsing experience, you can configure your apps' \
                'WebView objects to verify URLs using Google Safe Browsing. \n When this security measure is enabled,'\
                'your app shows users a warning when they attempt to navigate to a potentially unsafe website. \n %s'\
               % fileName

    def getName(self):
        # The name to be displayed against the progressbar
        return "Insecure Content Provider"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target