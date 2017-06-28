import sys, os, re

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj
import lib.plyj.model as m
from modules.common import terminalPrint

class LoggingIssuesPlugin(IPlugin):

    def target(self, queue):
        # get all decompiled files that contains usage of WebView
        files = common.java_files
        parser = plyj.Parser()
        global parser
        global tree
        global fileName, verbose, debug
        len_d = []
        len_v = []
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
            # Traverse down the tree to find out verbose or debug logs
            try:
                for type_decl in tree.type_declarations:
                    if type(type_decl) is m.ClassDeclaration:
                        for t in type_decl.body:
                            if type(t) is m.MethodDeclaration:
                                if str(t.name) == 'v':
                                    len_v.append(str(t.name))
                                    PluginUtil.reportIssue(fileName, self.createIssueDetails(fileName), res)
                                elif str(t.name) == 'd':
                                        len_d.append(str(t.name))
                                        PluginUtil.reportIssue(fileName, self.createIssueDetails(fileName), res)
            except Exception as e:
                continue
        queue.put(res)

        # Give the count of verbose/debug logs.
        # Written separately so that issue description is mentioned once and not repeated for each warning.
        if len(len_d) > 0 or len(len_v) > 0:
            x = str(len(len_d))
            y = str(len(len_v))
            PluginUtil.reportIssue(fileName, self.createIssueDetails1((x,y)), res)

        global reg, reg1, filename
        len_reg = []
        len_reg1 = []
        # Sometimes Log functions may be called from a constructor and hence maybe skipped by above tree
        if len(len_d) == 0 and len(len_v) == 0:

            for f in files:
                with open(f, 'r') as fi:
                    filename = fi.read()
                    file_name = str(f)
                reg = re.findall('Log\.d', filename)
                reg1 = re.findall('Log\.v', filename)
                if len(reg) > 0:
                    len_reg.append(str(reg))
                    PluginUtil.reportIssue(filename, self.createIssueDetails(file_name), res)
                if len(reg1) > 0:
                    len_reg1.append(str(reg1))
                    PluginUtil.reportIssue(filename, self.createIssueDetails(file_name), res)

        if len(len_reg) > 0 or len(len_reg1) > 0:
            x = str(len(len_reg))
            y = str(len(len_reg1))
            PluginUtil.reportIssue(filename, self.createIssueDetails1((x, y)), res)

    def createIssueDetails(self, fileName):
        return 'Verbose/Debug logs are detected in file: %s.\n' \
               % fileName

    def createIssueDetails1(self, (x, y)):
        return 'This may allow potential leakage of information from Android applications. \n' \
               'Verbose/Debug should never be compiled into an application except during development \n'\
               'https://developer.android.com/reference/android/util/Log.html \n' \
               ' %s debug logs and %s verbose logs were found in the application' \
               % (x, y)

    def getName(self):
        # The name to be displayed against the progressbar
        return "Logging functions detected"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target