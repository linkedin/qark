import logging

from qark.issue import Severity, Issue
from qark.scanner.plugin import ManifestPlugin

log = logging.getLogger(__name__)

PATH_USAGE_DESCRIPTION = ("android:path means that the permission applies to the exact path declared"
                          " in android:path. This expression does not protect the sub-directories")


class AndroidPath(ManifestPlugin):
    def __init__(self):
        super(AndroidPath, self).__init__(category="manifest", name="android:path tag used",
                                          description=PATH_USAGE_DESCRIPTION)

        self.severity = Severity.WARNING

    def run(self):
        with open(self.manifest_path, "r") as manifest_file:
            for line_number, line in enumerate(manifest_file):
                if "android:path=" in line:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=self.manifest_path,
                        line_number=line_number)
                    )


plugin = AndroidPath()
