import sys, os, re

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj
import lib.plyj.model as m


class WebViewChecksPlugin(IPlugin):

    JAVASCRIPT_ENABLED = r'setJavaScriptEnabled\(true\)'
    LOAD_URL_HTTP = r'loadUrl\([\'\"]http:'
    ALLOW_CONTENT_ACCESS = r'setAllowContentAccess\(true\)'
    MIXED_CONTENT = r'setMixedContentMode'

    def __init__(self):
        self.name = 'Webview Issues'

    def target(self, queue):
        files = common.java_files
        global parser
        parser = plyj.Parser()
        global tree
        global fileName
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
                global url
                url = []
                for import_decl in tree.import_declarations:
                    if 'WebView' in import_decl.name.value or 'WebSettings' in import_decl.name.value:
                        fileBody = str(open(fileName, 'r').read())

                        if PluginUtil.contains(self.JAVASCRIPT_ENABLED, fileBody):

                            if PluginUtil.contains(self.MIXED_CONTENT, fileBody):
                                PluginUtil.reportWarning(fileName, self.MixedContentIssueDetails(fileName), res)

                            if "setAllowFileAccess(false)" or "setAllowContentAccess(false)" not in fileBody:
                                PluginUtil.reportInfo(fileName, self.SecureContentIssueDetails(fileName), res)

                        if PluginUtil.contains(self.LOAD_URL_HTTP, fileBody):
                            PluginUtil.reportWarning(fileName, self.loadhttpurlsIssueDetails(fileName), res)

                        break

            except Exception:
                continue

            try:
                for import_decl in tree.import_declarations:
                    if 'WebView' in import_decl.name.value or 'WebSettings' in import_decl.name.value:
                        for type_decl in tree.type_declarations:
                            if type(type_decl) is m.ClassDeclaration:
                                for t in type_decl.body:
                                    if type(t) is m.MethodDeclaration:
                                        if 'shouldOverrideUrlLoading' in t.name:
                                            if 'true' not in str(t.body):
                                                PluginUtil.reportWarning(fileName, self.OverrideUrlIssueDetails(fileName), res)
                                            else:
                                                continue
                                        if 'shouldInterceptRequest' in t.name:
                                            if 'null' in str(t.body):
                                                PluginUtil.reportWarning(fileName, self.InterceptRequestIssueDetails(fileName), res)
                                            else:
                                                continue
                        break

            except Exception as e:
                continue

        queue.put(res)

    def loadhttpurlsIssueDetails(self, fileName):
        return 'If WebView is allowing to load clear-text content from the Internet\n ' \
               'then it would be open to various forms of attack such as MiTM. \n%s\n' \
                % fileName

    def MixedContentIssueDetails(self, fileName):
        return 'Usage of setMixedContentMode is found\n' \
               'In this mode, the WebView will allow a secure origin to load content ' \
               'from any other origin, even if that origin is insecure. ' \
               'This is the least secure mode of operation for the WebView, ' \
               'and where possible apps should not set this mode.\n ' \
               'https://developer.android.com/reference/android/webkit/WebSettings.html#MIXED_CONTENT_ALWAYS_ALLOW \n%s\n'\
                % fileName

    def SecureContentIssueDetails(self, fileName):
        return 'File System Access is by default enabled\n' \
               'setAllowFileAccess() and setAllowContentAccess() are by default true. ' \
               'This should be set to false to restrict access to local data since it is used to display content from locally stored HTML ' \
               'or fetch HTML and other content from the server.\n ' \
               'https://developer.android.com/reference/android/webkit/WebSettings.html \n%s\n' \
                % fileName


    def OverrideUrlIssueDetails(self, fileName):
        return 'Improper implementation of shouldOverrideUrlLoading method\n' \
               'This incorrect implementation allows any url to load in the webview \n%s\n' \
                % fileName

    def InterceptRequestIssueDetails(self, fileName):
        return 'Improper implementation of shouldInterceptRequest method\n' \
               'Returning null allows any url to load in the webview \n%s\n' \
                % fileName

    def getName(self):
        return "Webview Issues"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target