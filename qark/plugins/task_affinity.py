import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj

class TaskAffinityPlugin(IPlugin):

    NEW_TASK = r'FLAG\_ACTIVITY\_NEW\_TASK'
    MULTIPLE_TASK = r'FLAG\_ACTIVITY\_MULTIPLE\_TASK'

    def __init__(self):
        self.name = 'Task Hijacking'

    def target(self, queue):
        files = common.java_files
        global parser, tree, file_name
        parser = plyj.Parser()
        tree = ''
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
                for import_decl in tree.import_declarations:
                    # Check if Intent is called in the import statement
                    if 'Intent' in import_decl.name.value:
                        with open(file_name, 'r') as f:
                            file_body = f.read()
                        if PluginUtil.contains(self.NEW_TASK, file_body):
                            PluginUtil.reportWarning(file_name, self.new_task_issue(file_name), res)
                            break
                        if PluginUtil.contains(self.MULTIPLE_TASK_TASK, file_body):
                            PluginUtil.reportWarning(file_name, self.multiple_task_issue(file_name), res)
                            break
            except Exception:
                continue

        queue.put(res)

    def new_task_issue(self, file_name):
        return 'FLAG_ACTIVITY_NEW_TASK - intent flag is set. \n ' \
               'This results in activity being loaded as a part of a new task. This can' \
               ' be abused in the task hijacking attack. \n%s\n' \
               'Reference: https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf\n' \
               % file_name

    def multiple_task_issue(self, file_name):
        return 'FLAG_ACTIVITY_MULTIPLE_TASK - intent flag is set. \n ' \
               'This results in activity being loaded as a part of a new task. This can' \
               ' be abused in the task hijacking attack. \n%s\n' \
               'Reference: https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf\n' \
               % file_name

    def getName(self):
        return "Task Hijacking"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
