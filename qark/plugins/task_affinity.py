import sys, os, re

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
        global parser, tree, fileName
        parser = plyj.Parser()
        tree = ''
        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            fileName = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception:
                continue

            try:
                for import_decl in tree.import_declarations:
                    if 'Intent' in import_decl.name.value:
                        fileBody = str(open(fileName, 'r').read())
                        if PluginUtil.contains(self.NEW_TASK, fileBody):
                            PluginUtil.reportWarning(fileName, self.NewTaskIssueDetails(fileName), res)
                            break
                        if PluginUtil.contains(self.MULTIPLE_TASK_TASK, fileBody):
                            PluginUtil.reportWarning(fileName, self.MultipleTaskIssueDetails(fileName), res)
                            break

            except Exception:
                continue

        queue.put(res)

    def NewTaskIssueDetails(self, fileName):
        return 'FLAG_ACTIVITY_NEW_TASK - intent flag is set. \n ' \
               'This results in activity being loaded as a part of a new task. This can' \
               ' be abused in the task hijacking attack. \n%s\n' \
               'Reference: https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf\n' \
               % fileName

    def MultipleTaskIssueDetails(self, fileName):
        return 'FLAG_ACTIVITY_MULTIPLE_TASK - intent flag is set. \n ' \
               'This results in activity being loaded as a part of a new task. This can' \
               ' be abused in the task hijacking attack. \n%s\n' \
               'Reference: https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf\n' \
               % fileName

    def getName(self):
        return "Task Hijacking"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target