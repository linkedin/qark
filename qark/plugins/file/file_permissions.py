from qark.plugins.helpers import java_files_from_files, run_regex
from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue

import logging

log = logging.getLogger(__name__)


WORLD_READABLE = "MODE_WORLD_READABLE"
WORLD_WRITEABLE = "MODE_WORLD_WRITEABLE"

WORLD_READABLE_DESCRIPTION = "World readable file found. Any application or file browser can access and read this file"
WORLD_WRITEABLE_DESCRIPTION = "World writeable file found. Any application or file browser can write to this file"


class FilePermissions(BasePlugin):
    """
    This module runs a regex search on every Java file looking for `WORLD_READABLE` and `WORLD_WRITEABLE` modes.
    """
    def __init__(self):
        BasePlugin.__init__(self, category="file", name="File Permissions")
        self.severity = Severity.WARNING

    def run(self, filepath, file_contents=None, **kwargs):
        if not file_contents:
            return

        if run_regex(filepath, WORLD_READABLE):
            self.issues.append(Issue(category=self.category, name="World readable file", severity=self.severity,
                                     description=WORLD_READABLE_DESCRIPTION, file_object=filepath))
        if run_regex(filepath, WORLD_WRITEABLE):
            self.issues.append(Issue(category=self.category, name="World writeable file", severity=self.severity,
                                     description=WORLD_WRITEABLE_DESCRIPTION, file_object=filepath))


plugin = FilePermissions()
