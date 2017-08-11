from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import sys
import os
import re
import lib.plyj.parser as plyj
import lib.plyj.model as m

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

STRING = ("{} logs are detected\nThis may allow potential leakage of information from Android applications.\n"
          "{} logs should never be compiled into an application except during development.\nhttps://developer."
          "android.com/reference/android/util/Log.html\n\nFilepath:\n{}\n{} {} logs were found in the application\n")


def debug_log_issues(filepath, x):
    return STRING.format("Debug", "Debug", filepath, x, "debug")


def verbose_log_issues(filepath, y):
    return STRING.format("Verbose", "Verbose", filepath, y, "verbose")


class LoggingIssuesPlugin(IPlugin):
    debug_regex = r'Log\.d'
    verbose_regex = r'Log\.v'

    def __init__(self):
        self.name = 'Detect exposed logs'

    def target(self, queue):
        files = common.java_files
        global filepath
        parser = plyj.Parser()
        total_debug_logs, total_verbose_logs, debug_logs, verbose_logs, verbose_logs_list, res, \
        debug_logs_list, discovered_debug_logs, discovered_verbose_logs = ([] for _ in xrange(9))
        tree = ''
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

            # Traverse down the tree to find out verbose or debug logs
            try:
                for type_decl in tree.type_declarations:
                    if type(type_decl) is m.ClassDeclaration:
                        for fields in type_decl.body:
                            if type(fields) is m.MethodDeclaration:
                                # Check if the app is send verbose logging message
                                if str(fields.name) == 'v':
                                    verbose_logs.append(str(fields.name))
                                    if filepath not in discovered_verbose_logs:
                                        discovered_verbose_logs.append(filepath)
                                # Check if the app is send debug logging message
                                elif str(fields.name) == 'd':
                                    debug_logs.append(str(fields.name))
                                    if filepath not in discovered_debug_logs:
                                        discovered_debug_logs.append(filepath)
            except Exception as e:
                common.logger.exception(
                    "Unable to traverse the tree. Error: " + str(e))
                continue

        # Join all the filename and path containing debug and verbose logging
        debug_logs_path = " \n".join(discovered_debug_logs)
        verbose_logs_path = " \n".join(discovered_verbose_logs)
        queue.put(res)

        # Display the file paths of all discovered logs
        if discovered_debug_logs:
            x = len(debug_logs)
            PluginUtil.reportInfo(filepath, debug_log_issues(debug_logs_path, x), res)

        if discovered_verbose_logs:
            y = len(verbose_logs)
            PluginUtil.reportInfo(filepath, verbose_log_issues(verbose_logs_path, y), res)

        # Sometimes Log functions may be called from a constructor and hence maybe skipped by tree
        # if len(debug_logs) == 0 and len(verbose_logs) == 0:
        for f in files:
            with open(f, 'r') as fi:
                filename = fi.read()
            filepath = str(f)
            find_debug_logs = re.findall(self.debug_regex, filename)
            find_verbose_logs = re.findall(self.verbose_regex, filename)

            if find_debug_logs:
                total_debug_logs.append(str(find_debug_logs))
                if filepath not in debug_logs_list:
                    debug_logs_list.append(filepath)

            if find_verbose_logs:
                total_verbose_logs.append(str(find_verbose_logs))
                if filepath not in verbose_logs_list:
                    verbose_logs_list.append(filepath)

        debug_path = " \n".join(debug_logs_list)
        verbose_path = " \n".join(verbose_logs_list)

        if total_debug_logs:
            x = len(total_debug_logs)
            PluginUtil.reportInfo(filepath, debug_log_issues(debug_path, x), res)

        if total_verbose_logs:
            y = len(total_verbose_logs)
            PluginUtil.reportInfo(filepath, verbose_log_issues(verbose_path, y), res)

    @staticmethod
    def getName():
        return "Detect exposed logs"

    @staticmethod
    def getCategory():
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
