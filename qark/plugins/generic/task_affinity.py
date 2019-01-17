import logging
import re

from qark.issue import Severity, Issue
from qark.scanner.plugin import JavaASTPlugin

log = logging.getLogger(__name__)

TASK_AFFINITY_DESCRIPTION = (
    "FLAG_ACTIVITY_{type}_TASK - intent flag is set. This results in activity being loaded as a part of a new task. "
    "This can be abused in the task hijacking attack. "
    "Reference: https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf"
)
NEW_TASK_REGEX = re.compile(r'FLAG_ACTIVITY_NEW_TASK')
MULTIPLE_TASK_REGEX = re.compile(r'FLAG_ACTIVITY_MULTIPLE_TASK')


class TaskAffinity(JavaASTPlugin):
    def __init__(self):
        super(TaskAffinity, self).__init__(category="generic", name="Potential task hijacking",
                                           description=TASK_AFFINITY_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self):
        if any("Intent" in import_decl.path for import_decl in self.java_ast.imports):
            description = None

            if re.search(NEW_TASK_REGEX, self.file_contents):
                description = TASK_AFFINITY_DESCRIPTION.format(type="NEW")
            elif re.search(MULTIPLE_TASK_REGEX, self.file_contents):
                description = TASK_AFFINITY_DESCRIPTION.format(type="MULTIPLE")

            if description:
                self.issues.append(Issue(category=self.category,
                                         severity=self.severity,
                                         name=self.name,
                                         description=description,
                                         file_object=self.file_path))


plugin = TaskAffinity()
