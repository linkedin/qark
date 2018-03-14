import logging

from qark.issue import Severity, Issue
from qark.scanner.plugin import BasePlugin
from qark.xml_helpers import get_manifest_out_of_files

log = logging.getLogger(__name__)

TASK_REPARENTING_DESCRIPTION = (
    "This allows an existing activity to be reparented to a new native task i.e task having the same affinity as the "
    "activity. This may lead to UI spoofing attack on this application."
    "https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf"
)


class TaskReparenting(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="manifest", name="android:allowTaskReparenting='true' found",
                            description=TASK_REPARENTING_DESCRIPTION)
        self.severity = Severity.WARNING

    def run(self, files, apk_constants=None):
        manifest_path = get_manifest_out_of_files(files)
        if not manifest_path:
            return

        with open(manifest_path, "r") as manifest_file:
            for line_number, line in enumerate(manifest_file):
                if 'android:allowTaskReparenting="true"' in line:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=manifest_path,
                        line_number=line_number)
                    )


plugin = TaskReparenting()
