from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import sys
import os
import lib.plyj.parser as plyj
import lib.plyj.model as m

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')


def intercept_request(file_name):
    STRING = ("Improper implementation of shouldInterceptRequest method\n"
              "Returning null allows any url to load in the webview\nFilepath: {}\n")
    return STRING.format(file_name)


def url_override(file_name):
    STRING = ("Improper implementation of shouldOverrideUrlLoading method\n"
              "This incorrect implementation allows any url to load in the webview\nFilepath: {}\n")
    return STRING.format(file_name)


def secure_content(issue_name):
    STRING = ("File System Access is by default enabled\n"
              "setAllowFileAccess() and setAllowContentAccess() are by default true. This should"
              " be set to false to restrict access to local data since it is used to display"
              " content from locally stored HTML or fetch HTML and other content from the server.\n"
              "Reference: https://developer.android.com/reference/android/webkit/WebSettings.html\nFilepath: {}\n")
    return STRING.format(issue_name)


def load_http_urls(file_name):
    STRING = ("Webview is loading http urls\nIf WebView is allowing to load clear-text content"
              " from the Internet then it would be open to various forms of attack such as MiTM.\nFilepath: {}\n")
    return STRING.format(file_name)


def mixed_content(file_name):
    STRING = ("Usage of setMixedContentMode is found\n"
              "In this mode, the WebView will allow a secure origin to load content from"
              " any other origin, even if that origin is insecure. This is the least secure"
              " mode of operation for the WebView, and where possible apps should not set this mode.\n"
              "Reference: https://developer.android.com/reference/android/webkit/WebSettings.html#MIXED_CONTENT_ALWAYS_ALLOW \nFilepath: {}\n")
    return STRING.format(file_name)


class WebViewChecksPlugin(IPlugin):
    JAVASCRIPT_ENABLED = r'setJavaScriptEnabled\(true\)'
    LOAD_URL_HTTP = r'loadUrl\([\'\"]http:'
    ALLOW_CONTENT_ACCESS = r'setAllowContentAccess\(true\)'
    MIXED_CONTENT = r'setMixedContentMode'

    def __init__(self):
        self.name = 'Webview Issues'

    def target(self, queue):
        files = common.java_files
        parser = plyj.Parser()
        global filepath, tree
        tree = ''
        res = []
        issues_list = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            filepath = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception as e:
                common.logger.exception(
                    "Unable to parse the file and generate as AST. Error: " + str(e))
                continue

            try:
                global url
                url = []
                for import_decl in tree.import_declarations:
                    # Check import statements with value declared as WebView and WebSettings for the potential use of web views
                    if 'WebView' in import_decl.name.value or 'WebSettings' in import_decl.name.value:
                        with open(filepath, 'r') as r:
                            data = r.read()

                        if PluginUtil.contains(self.JAVASCRIPT_ENABLED, data):
                            if PluginUtil.contains(self.MIXED_CONTENT, data):
                                PluginUtil.reportWarning(filepath, mixed_content(filepath), res)

                            if "setAllowFileAccess(false)" or "setAllowContentAccess(false)" not in data:
                                if filepath not in issues_list:
                                    issues_list.append(filepath)

                        if PluginUtil.contains(self.LOAD_URL_HTTP, data):
                            PluginUtil.reportWarning(filepath, load_http_urls(filepath), res)
                        break

            except Exception as e:
                common.logger.info("Plyj parser failed while parsing the file: " + filepath + "\nError" + str(e))
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
                                                PluginUtil.reportWarning(filepath, url_override(filepath), res)
                                                break
                                            else:
                                                continue
                                        if 'shouldInterceptRequest' in fields.name:
                                            if 'null' in str(fields.body):
                                                PluginUtil.reportWarning(filepath, intercept_request(filepath), res)
                                                break
                                            else:
                                                continue
                        break

            except Exception as e:
                common.logger.info("Plyj parser failed while parsing the file: " + filepath + "\nError" + str(e))
                continue

        if issues_list:
            issue_name = " \n".join(issues_list)
            PluginUtil.reportInfo(filepath, secure_content(issue_name), res)

        queue.put(res)

    @staticmethod
    def getName():
        return "Webview Issues"

    @staticmethod
    def getCategory():
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
