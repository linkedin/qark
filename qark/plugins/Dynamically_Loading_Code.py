import sys, os, re

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj
import lib.plyj.model as m
from modules.common import terminalPrint

class DynamicalPlugin(IPlugin):

    def target(self, queue):
        # get all decompiled files that contains usage of WebView
        files = common.java_files
        parser = plyj.Parser()
        global parser
        global tree
        global fileName
        tree = ''
        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.getName(), percent=round(count * 100 / len(files)))
            fileName = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception as e:
                continue

            try:
                for import_decl in tree.import_declarations:
                    if 'DexClassLoader' in import_decl.name.value:
                        if "loadClass" in str(tree):
                            PluginUtil.reportIssue(fileName, self.createIssueDetails(fileName), res)
            except Exception as e:
                continue
        queue.put(res)

    def createIssueDetails(self, fileName):
        return 'Application dynamically load an external class through DexClassLoader %s.\n' \
               'https://developer.android.com/reference/dalvik/system/DexClassLoader.html' \
               % fileName

    def getName(self):
        # The name to be displayed against the progressbar
        return "Dynamically loading code"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target