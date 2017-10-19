from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import sys
import os
import lib.plyj.parser as plyj

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

STRING = ("FLAG_ACTIVITY_{}_TASK - intent flag is set.\nThis results in activity being loaded"
          "as a part of a new task. This can be abused in the task hijacking attack.\n{}\n"
          "Reference: https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf\n")


def new_task(file_path):
    return STRING.format("NEW", file_path)


def multiple_task(file_path):
    return STRING.format("MULTIPLE", file_path)


class TaskAffinityPlugin(IPlugin):
    NEW_TASK = r'FLAG\_ACTIVITY\_NEW\_TASK'
    MULTIPLE_TASK = r'FLAG\_ACTIVITY\_MULTIPLE\_TASK'

    def __init__(self):
        self.name = 'Task Hijacking'

    def target(self, queue):
        files = common.java_files
        global filepath, tree
        parser = plyj.Parser()
        tree = ''
        res = []
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
                for import_decl in tree.import_declarations:
                    # Check if Intent is called in the import statement
                    if 'Intent' in import_decl.name.value:
                        with open(filepath, 'r') as r:
                            file_body = r.read()
                        if PluginUtil.contains(self.NEW_TASK, file_body):
                            PluginUtil.reportInfo(filepath, new_task(filepath), res)
                            break
                        if PluginUtil.contains(self.MULTIPLE_TASK, file_body):
                            PluginUtil.reportInfo(filepath, multiple_task(filepath), res)
                            break
            except Exception as e:
                common.logger.debug("Plyj parser failed while parsing the file: " + filepath + "\nError" + str(e))
                continue

        queue.put(res)

    @staticmethod
    def getName():
        return "Task Hijacking"

    @staticmethod
    def getCategory():
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
