import logging

from qark.issue import Severity, Issue
from qark.scanner.plugin import ManifestPlugin
from qark.xml_helpers import get_manifest_out_of_files

log = logging.getLogger(__name__)

TASK_LAUNCH_MODE_DESCRIPTION = (
    "This results in AMS either resuming the earlier activity or loads it in a task with same affinity "
    "or the activity is started as a new task. This may result in Task Poisoning. "
    "https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf"
)


class SingleTaskLaunchMode(ManifestPlugin):
    def __init__(self, **kwargs):
        kwargs.update(category="manifest", name="launchMode=singleTask found", description=TASK_LAUNCH_MODE_DESCRIPTION)
        super(SingleTaskLaunchMode, self).__init__(**kwargs)
        self.severity = Severity.WARNING

    def run(self, files, apk_constants=None):
        if not self.manifest_path:
            return

        with open(self.manifest_path, "r") as manifest_file:
            for line_number, line in enumerate(manifest_file):
                if 'android:launchMode="singleTask"' in line:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=self.manifest_path,
                        line_number=line_number)
                    )


plugin = SingleTaskLaunchMode()
