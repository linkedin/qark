"""This plugin checks if there are any lines in the file that match the regex ``API_KEY_REGEX`` while
also not matching ``SPECIAL_CHARACTER_REGEX``."""

import logging
import re

from qark.issue import Severity, Issue
from qark.scanner.plugin import FileContentsPlugin

log = logging.getLogger(__name__)

API_KEY_REGEX = re.compile(r'(?=.{20,})(?=.+\d)(?=.+[a-z])(?=.+[A-Z])(?=.+[-_])')
SPECIAL_CHARACTER_REGEX = re.compile(r'(?=.+[!$%^&*()_+|~=`{}\[\]:<>?,./])')
BLACKLISTED_EXTENSIONS = (".apk", ".dex", ".png", ".jar")

API_KEY_DESCRIPTION = "Please confirm and investigate the API key to determine its severity."


class JavaAPIKeys(FileContentsPlugin):
    def __init__(self):
        super(JavaAPIKeys, self).__init__(category="file", name="Potential API Key found",
                                          description=API_KEY_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self):
        if any(self.file_path.endswith(extension) for extension in BLACKLISTED_EXTENSIONS):
            return

        for line_number, line in enumerate(self.file_contents.split("\n")):
            for word in line.split():
                if re.search(API_KEY_REGEX, word) and not re.search(SPECIAL_CHARACTER_REGEX, word):
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=self.file_path,
                        line_number=(line_number, 0))
                    )


plugin = JavaAPIKeys()
