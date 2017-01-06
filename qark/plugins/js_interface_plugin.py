import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub


class JsInterfacePlugin(IPlugin):
    # regex to determine if file contains usage of WebView
    webViewRegex = r'android\.webkit\.WebView'

    # regex to extract WebView variable names in group 2
    varNameRegex = r'(android\.webkit\.)?WebView\s(\w*?)([,);]|(\s=))'

    # regex to match inline calls
    inlineRegex = r'new\s(android\.webkit\.)?WebView\(.*?\)\.addJavascriptInterface\(.*?\)'

    def target(self, queue):
        # get all decompiled files that contains usage of WebView
        files = common.text_scan(common.java_files, self.webViewRegex)

        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.getName(), percent=round(count * 100 / len(files)))

            # get decompiled file body
            fileName = f[1]
            with open(fileName, 'r') as fi:
                fileBody = fi.read()

            # report if file contains any inline calls
            if PluginUtil.contains(self.inlineRegex, fileBody):
                PluginUtil.reportIssue(fileName, self.createIssueDetails(fileName), res)
                break

            # report if any WebView variables invoke calls
            for varName in PluginUtil.returnGroupMatches(self.varNameRegex, 2, fileBody):
                if PluginUtil.contains(r'%s\.addJavascriptInterface\(.*?\)' % varName, fileBody):
                    PluginUtil.reportIssue(fileName, self.createIssueDetails(fileName), res)
                    break

        queue.put(res)

    def createIssueDetails(self, fileName):
        return 'Call to addJavascriptInterface() is detected on instance of WebView in file: %s.\n' \
               'This will allow Javascript to invoke operations that are normally reserved for Android applications.' \
               % fileName

    def getName(self):
        # The name to be displayed against the progressbar
        return "Exposed javascript interface"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target

