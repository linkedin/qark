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


class LoggingIssuesPlugin(IPlugin):

    debug_regex = r'Log\.d'

    def __init__(self):
        self.name = 'Hardcoded secrets'

    def target(self, queue):
        files = common.java_files

        parser = plyj.Parser()

        tree = ''
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            fileName = str(f)

            try:
                tree = parser.parse_file(f)
            except Exception as e:
                common.logger.exception(
                    "Unable to parse the file and generate as AST. Error: " + str(e))

            try:
                for import_decl in tree.import_declarations:
                    if self.DEX_CLASS_LOADER in import_decl.name.value:

            except Exception:
                continue


            for f in files:
                with open(f, 'r') as fi:
                    filename = fi.read()
                    file_name = str(f)

    def DebugLogsIssueDetails(self, string_filename_d):
        return 'Debug logs are detected in file: \n%s.\n' \
               % string_filename_d

    def getName(self):
        return "Hardcoded secrets"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
