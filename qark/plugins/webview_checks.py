import sys
import os
import re

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
        global file_name
        tree = ''
        res = []
        issues_list =[]
        count = 0
        for file in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            file_name = str(file)
            try:
                tree = parser.parse_file(file)
            except Exception:
                continue

            try:
                global url
                url = []
                for import_decl in tree.import_declarations:
                    # Check import statements with value declared as WebView and WebSettings for the potential use of web views
                    if 'WebView' in import_decl.name.value or 'WebSettings' in import_decl.name.value:
                        with open(file_name, 'r') as f:
                            data = f.read()

                        if PluginUtil.contains(self.JAVASCRIPT_ENABLED, data):

                            if PluginUtil.contains(self.MIXED_CONTENT, data):
                                PluginUtil.reportWarning(file_name, self.mixed_content_issue(file_name), res)

                            if "setAllowFileAccess(false)" or "setAllowContentAccess(false)" not in data:
                                if not file_name in issues_list:
                                    issues_list.append(file_name)

                        if PluginUtil.contains(self.LOAD_URL_HTTP, data):
                            PluginUtil.reportWarning(file_name, self.load_http_urls(file_name), res)

                        break

            except Exception:
                continue

            try:
                for import_decl in tree.import_declarations:
                    if 'WebView' in import_decl.name.value or 'WebSettings' in import_decl.name.value:
                        for type_decl in tree.type_declarations:
                            # Check for class declaration in java source code and traverse further down the AST to find method names
                            if type(type_decl) is m.ClassDeclaration:
                                for fields in type_decl.body:
                                    if type(fields) is m.MethodDeclaration:
                                        if 'shouldOverrideUrlLoading' in fields.name:
                                            if 'true' not in str(fields.body):
                                                PluginUtil.reportWarning(file_name, self.url_override_issue(file_name), res)
                                                break
                                            else:
                                                continue
                                        if 'shouldInterceptRequest' in fields.name:
                                            if 'null' in str(fields.body):
                                                PluginUtil.reportWarning(file_name, self.intercept_request_issue(file_name), res)
                                                break
                                            else:
                                                continue
                        break

            except Exception as e:
                continue

        if issues_list:
            issue_name = " \n".join(issues_list)
            PluginUtil.reportInfo(file_name, self.secure_content_issue(issue_name), res)

        queue.put(res)

    def load_http_urls(self, file_name):
        return 'If WebView is allowing to load clear-text content from the Internet\n ' \
               'then it would be open to various forms of attack such as MiTM. \n%s\n' \
                % file_name

    def mixed_content_issue(self, file_name):
        return 'Usage of setMixedContentMode is found\n' \
               'In this mode, the WebView will allow a secure origin to load content ' \
               'from any other origin, even if that origin is insecure. ' \
               'This is the least secure mode of operation for the WebView, ' \
               'and where possible apps should not set this mode.\n ' \
               'https://developer.android.com/reference/android/webkit/WebSettings.html#MIXED_CONTENT_ALWAYS_ALLOW \n%s\n'\
                % file_name

    def secure_content_issue(self, issue_name):
        return 'File System Access is by default enabled\n' \
               'setAllowFileAccess() and setAllowContentAccess() are by default true. ' \
               'This should be set to false to restrict access to local data since it is used to display content from locally stored HTML ' \
               'or fetch HTML and other content from the server.\n' \
               'https://developer.android.com/reference/android/webkit/WebSettings.html \n%s\n' \
                % issue_name

    def url_override_issue(self, file_name):
        return 'Improper implementation of shouldOverrideUrlLoading method\n' \
               'This incorrect implementation allows any url to load in the webview \n%s\n' \
                % file_name

    def intercept_request_issue(self, file_name):
        return 'Improper implementation of shouldInterceptRequest method\n' \
               'Returning null allows any url to load in the webview \n%s\n' \
                % file_name

    def getName(self):
        return "Webview Issues"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
