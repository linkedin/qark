import logging
import re

from qark.issue import Severity, Issue
from qark.plugins.helpers import run_regex
from qark.scanner.plugin import FileContentsPlugin

log = logging.getLogger(__name__)

WORLD_READABLE = re.compile("MODE_WORLD_READABLE")
WORLD_WRITEABLE = re.compile("MODE_WORLD_WRITEABLE")

WORLD_READABLE_DESCRIPTION = "World readable file found. Any application or file browser can access and read this file"
WORLD_WRITEABLE_DESCRIPTION = "World writeable file found. Any application or file browser can write to this file"


class FilePermissions(FileContentsPlugin):
    """
    This module runs a regex search on every Java file looking for `WORLD_READABLE` and `WORLD_WRITEABLE` modes.
    """
    def __init__(self):
        super(FilePermissions, self).__init__(category="file", name="File Permissions")
        self.severity = Severity.WARNING

    def run(self):
        if run_regex(self.file_path, WORLD_READABLE):
            self.issues.append(Issue(category=self.category, name="World readable file", severity=self.severity,
                                     description=WORLD_READABLE_DESCRIPTION, file_object=self.file_path))
        if run_regex(self.file_path, WORLD_WRITEABLE):
            self.issues.append(Issue(category=self.category, name="World writeable file", severity=self.severity,
                                     description=WORLD_WRITEABLE_DESCRIPTION, file_object=self.file_path))


plugin = FilePermissions()
