import sys, os, re

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj
import lib.plyj.model as m


class LoggingIssuesPlugin(IPlugin):

    debug_regex = r'Log\.d'
    verbose_regex = r'Log\.v'

    def __init__(self):
        self.name = 'Detect exposed logs'

    def target(self, queue):
        files = common.java_files
        global parser, tree, fileName, verbose, debug, debug_logs_path, verbose_logs_path
        parser = plyj.Parser()
        debug_logs = []
        verbose_logs = []
        discovered_debug_logs = []
        discovered_verbose_logs = []
        res = []
        tree = ''
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
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
                                    verbose_logs.append(str(t.name))
                                    discovered_verbose_logs.append(fileName)
                                elif str(t.name) == 'd':
                                        debug_logs.append(str(t.name))
                                        discovered_debug_logs.append(fileName)
            except Exception:
                continue

        # Join all the filename and path containing debug and verbose logging
        debug_logs_path = " \n".join(discovered_debug_logs)
        verbose_logs_path = " \n".join(discovered_verbose_logs)
        queue.put(res)

        if discovered_debug_logs:
            PluginUtil.reportInfo(fileName, self.DebugLogsIssueDetails(debug_logs_path), res)

        if discovered_verbose_logs:
            PluginUtil.reportInfo(fileName, self.VerboseLogsIssueDetails(verbose_logs_path), res)

        # Provide the count of verbose/debug logs.
        # Written separately so that issue description is mentioned once and not repeated for each warning.
        if debug_logs or verbose_logs:
            x = str(len(debug_logs))
            y = str(len(verbose_logs))
            PluginUtil.reportInfo(fileName, self.LogIssueDetails((x, y)), res)

        global reg, reg1, filename
        len_reg = []
        len_reg1 = []
        # Sometimes Log functions may be called from a constructor and hence maybe skipped by tree
        if len(debug_logs) == 0 and len(verbose_logs) == 0:
            for f in files:
                with open(f, 'r') as fi:
                    filename = fi.read()
                    file_name = str(f)
                reg = re.findall(self.debug_regex, filename)
                reg1 = re.findall(self.verbose_regex, filename)
                if reg:
                    len_reg.append(str(reg))
                    PluginUtil.reportInfo(filename, self.DebugLogsIssueDetails(file_name), res)
                if reg1:
                    len_reg1.append(str(reg1))
                    PluginUtil.reportInfo(filename, self.VerboseLogsIssueDetails(file_name), res)

        if len_reg or len_reg1:
            x = str(len(len_reg))
            y = str(len(len_reg1))
            PluginUtil.reportInfo(filename, self.LogIssueDetails((x, y)), res)

    def DebugLogsIssueDetails(self, string_filename_d):
        return 'Debug logs are detected in file: \n%s.\n' \
               % string_filename_d

    def VerboseLogsIssueDetails(self, fileName):
        return 'Verbose logs are detected in file: \n%s.\n' \
               % fileName

    def LogIssueDetails(self, (x, y)):
        return 'This may allow potential leakage of information from Android applications. \n' \
               'Verbose/Debug should never be compiled into an application except during development \n'\
               'https://developer.android.com/reference/android/util/Log.html \n' \
               '%s debug logs and %s verbose logs were found in the application\n' \
               % (x, y)

    def getName(self):
        return "Detect exposed logs"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target