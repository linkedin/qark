import logging
import re

from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

API_KEY_REGEX = re.compile(r'(?=.{20,})(?=.+\d)(?=.+[a-z])(?=.+[A-Z])(?=.+[-_])')
SPECIAL_CHARACTER_REGEX = re.compile(r'(?=.+[!$%^&*()_+|~=`{}\[\]:<>?,./])')

API_KEY_DESCRIPTION = "Please confirm and investigate the API key to determine its severity."


class JavaAPIKeys(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="file", name="Potential API Key found",
                            description=API_KEY_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self, files, apk_constants=None):
        java_files = java_files_from_files(files)
        for java_file in java_files:
            self._process(java_file)

    def _process(self, java_file_path):
        with open(java_file_path, "r") as java_file:
            for line_number, line in enumerate(java_file):
                for word in line.split():
                    if re.search(API_KEY_REGEX, word) and not re.search(SPECIAL_CHARACTER_REGEX, word):
                        self.issues.append(Issue(
                            category=self.category, severity=self.severity, name=self.name,
                            description=self.description,
                            file_object=java_file_path,
                            line_number=line_number)
                        )


plugin = JavaAPIKeys()
