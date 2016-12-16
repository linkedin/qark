import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub


class JsInterfacePlugin(IPlugin):
    # regex to determine if file contains WebView
    webViewRegex = r'android.webkit.WebView'

    # regexes to get WebView names
    argRegex = r'(android\.webkit\.)?WebView\s(\w*?)[,)]'
    declRegex = r'(android\.webkit\.)?WebView\s(\w*?)[;|\s]=?'

    # regexes to match addJavascriptInterface() calls
    inlineRegex = r'new\s(android\.webkit\.)?WebView\(.*?\)\.addJavascriptInterface\(.*?\)'

    # returns a list of WebView argument variable names
    def getWebViewArgNames(self, fileBody):
        argNames = []
        for match in re.finditer(self.argRegex, fileBody):
            argNames.append(match.group(2))
        return argNames

    # returns a list of WebView declared variable names
    def getWebViewDeclarationNames(self, fileBody):
        declNames = []
        for match in re.finditer(self.declRegex, fileBody):
            declNames.append(match.group(2))
        return declNames

    # True if fileBody contains an inline addJavascriptInterface() call i.e. new WebView(..).addJavascriptInterface(),
    # False otherwise
    def containsInlineJavascriptInterfaceCall(self, fileBody):
        return re.search(self.inlineRegex, fileBody) is not None

    # True if file contains an addJavascriptInterface() call on the given WebView, False otherwise
    def containsJavascriptInterfaceCall(self, fileBody, webViewVarName):
        # escape w
        if webViewVarName == 'w':
            webViewVarName = r'\\w'
        regex = r'%s\.addJavascriptInterface\(.*?\)' % webViewVarName
        return re.search(regex, fileBody) is not None

    def createIssueDetails(self, fileName):
        return 'addJavascriptInterface() called on instance of WebView in file: %s\n' \
               'This allows Javascript to invoke operations that are normally reserved for Android applications.' \
               'Expose addJavascriptInterface() only to web pages from which all input is trustworthy.' \
               % fileName

    def target(self, queue):
        # get all decompiled files that contains usages of WebView
        files = common.text_scan(common.java_files, self.webViewRegex)

        results = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.getName(), percent=round(count * 100 / len(files)))

            # get decompiled file body
            fileName = f[1]
            with open(fileName, 'r') as fi:
                fileBody = fi.read()

            if self.containsInlineJavascriptInterfaceCall(fileBody):
                PluginUtil.reportIssue(fileName, self.createIssueDetails(fileName), results)
                break

            # get all possible WebView variable names and see if addJavascriptInterface() is invoked on any of them
            webViewVarNames = self.getWebViewArgNames(fileBody) + self.getWebViewDeclarationNames(fileBody)
            for webViewVarName in webViewVarNames:
                if self.containsJavascriptInterfaceCall(fileBody, webViewVarName):
                    PluginUtil.reportIssue(fileName, self.createIssueDetails(fileName), results)
                    break

        queue.put(results)

    def getName(self):
        # The name to be displayed against the progressbar
        return "Exposed Javascript Interface"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target

