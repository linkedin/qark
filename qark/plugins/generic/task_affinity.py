import logging
import re

import javalang

from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

TASK_AFFINITY_DESCRIPTION = (
    "FLAG_ACTIVITY_{type}_TASK - intent flag is set. This results in activity being loaded as a part of a new task. "
    "This can be abused in the task hijacking attack. "
    "Reference: https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf"
)
NEW_TASK_REGEX = re.compile(r'FLAG_ACTIVITY_NEW_TASK')
MULTIPLE_TASK_REGEX = re.compile(r'FLAG_ACTIVITY_MULTIPLE_TASK')


class TaskAffinity(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="generic", name="Potential task hijacking",
                            description=TASK_AFFINITY_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self, filepath, file_contents=None, java_ast=None, **kwargs):
        if not java_ast:
            return

        if any("Intent" in import_decl.path for import_decl in java_ast.imports):
            description = None

            if re.search(NEW_TASK_REGEX, file_contents):
                description = TASK_AFFINITY_DESCRIPTION.format("NEW")
            elif re.search(MULTIPLE_TASK_REGEX, file_contents):
                description = TASK_AFFINITY_DESCRIPTION.format("MULTIPLE")

            if description:
                self.issues.append(Issue(category=self.category,
                                         severity=self.severity,
                                         name=self.name,
                                         description=description,
                                         file_object=filepath))


plugin = TaskAffinity()
