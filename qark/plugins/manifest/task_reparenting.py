import logging

from qark.issue import Severity, Issue
from qark.scanner.plugin import ManifestPlugin

log = logging.getLogger(__name__)

TASK_REPARENTING_DESCRIPTION = (
    "This allows an existing activity to be reparented to a new native task i.e task having the same affinity as the "
    "activity. This may lead to UI spoofing attack on this application."
    "https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf"
)


class TaskReparenting(ManifestPlugin):
    def __init__(self, **kwargs):
        kwargs.update(category="manifest", name="android:allowTaskReparenting='true' found",
                      description=TASK_REPARENTING_DESCRIPTION)
        super(TaskReparenting, self).__init__(**kwargs)
        self.severity = Severity.WARNING

    def run(self, files, apk_constants=None):
        if not self.manifest_path:
            return

        with open(self.manifest_path, "r") as manifest_file:
            for line_number, line in enumerate(manifest_file):
                if 'android:allowTaskReparenting="true"' in line:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=self.manifest_path,
                        line_number=line_number)
                    )


plugin = TaskReparenting()
