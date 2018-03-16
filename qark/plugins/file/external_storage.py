import logging

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

EXTERNAL_STORAGE_DESCRIPTION = (
    "Reading files stored on {storage_location} makes it vulnerable to data injection attacks. "
    "Note that this code does no error checking and there is no security enforced with these files. "
    "For example, any application holding WRITE_EXTERNAL_STORAGE can write to these files. "
    "Reference: https://developer.android.com/reference/android/content/Context.html"
)

EXTERNAL_FILES_DIR_METHOD = 'getExternalFilesDir'
EXTERNAL_MEDIA_DIR_METHOD = 'getExternalMediaDirs'
EXTERNAL_STORAGE_PUBLIC_DIR_METHOD = 'getExternalStoragePublicDirectory'


class ExternalStorage(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="file", name="External storage used",
                            description=EXTERNAL_STORAGE_DESCRIPTION)
        self.severity = Severity.WARNING

    def run(self, files, apk_constants=None):
        java_files = java_files_from_files(files)

        for java_file in java_files:
            self._process(java_file)

    def _process(self, java_file):
        try:
            with open(java_file, "r") as java_file_to_read:
                file_contents = java_file_to_read.read()
        except IOError:
            log.debug("File does not exist %s, continuing", java_file)
            return

        try:
            tree = javalang.parse.parse(file_contents)
        except (javalang.parser.JavaSyntaxError, IndexError):
            log.debug("Error parsing file %s, continuing", java_file)
            return

        if any(["File" in imp for imp in tree.imports]):
            for _, method_invocation in tree.filter(MethodInvocation):
                storage_location = None
                if method_invocation.member == EXTERNAL_FILES_DIR_METHOD:
                    storage_location = "External Storage"
                elif method_invocation.member == EXTERNAL_MEDIA_DIR_METHOD:
                    storage_location = "External Media Directory"
                elif method_invocation.member == EXTERNAL_STORAGE_PUBLIC_DIR_METHOD:
                    storage_location = "External Storage Public Directory"

                if storage_location:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=java_file,
                        line_number=method_invocation.pos)
                    )


plugin = ExternalStorage()
