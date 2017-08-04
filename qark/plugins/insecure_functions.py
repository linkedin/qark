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

class InsecureFunctionsPlugin(IPlugin):
    CALL_FUNCTION = r'call'

    def __init__(self):
        self.name = 'Insecure functions'

    # recursive function to check for the function name by traversing down the AST
    def recursive_insecure_call_function(self, fields, file, res):
        if type(fields) is m.MethodDeclaration:
            if str(fields.name) == self.CALL_FUNCTION:
                PluginUtil.reportInfo(file_name, self.insecure_function_issue(file_name), res)
        elif type(fields) is list:
            for fieldname in fields:
                self.recursive_insecure_call_function(fieldname, file, res)
        elif hasattr(fields, '_fields'):
            for fieldname in fields._fields:
                self.recursive_insecure_call_function(getattr(fields, fieldname), file, res)
        return

    def target(self, queue):
        files = common.java_files
        global parser, tree, file_name
        parser = plyj.Parser()
        tree = ''
        global res
        res = []

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
                for type_decl in tree.type_declarations:
                    if type(type_decl) is m.ClassDeclaration:
                        for fields in type_decl.body:
                            try:
                                self.recursive_insecure_call_function(fields, file, res)

                            except Exception as e:
                                common.logger.error(
                                    "Unable to run insecure function plugin " + str(e))

            except Exception:
                continue
        queue.put(res)

    def insecure_function_issue(self, file_name):
        return 'The Content provider API provides a method call\n' \
               'The framework does no permission checking on this entry into the content provider besides the basic ability ' \
               'for the application to get access to the provider at all. \n' \
               'Any implementation of this method must do its own permission checks on incoming calls to make sure they are allowed. ' \
               'Failure to do so will allow unauthorized components to interact with the content provider.\n' \
               'Filepath: %s\n' \
               'Reference: https://bitbucket.org/secure-it-i/android-app-vulnerability-benchmarks/src/d5305b9481df3502e60e98fa352d5f58e4a69044/ICC/WeakChecksOnDynamicInvocation-InformationExposure/?at=master \n' \
               % file_name

    def getName(self):
        return "Insecure functions"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
