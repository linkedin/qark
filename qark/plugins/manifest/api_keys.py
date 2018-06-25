import logging
import re

from qark.issue import Severity, Issue
from qark.scanner.plugin import ManifestPlugin

log = logging.getLogger(__name__)

API_KEY_REGEX = re.compile(r'(?=.{20,})(?=.+\d)(?=.+[a-z])(?=.+[A-Z])')
SPECIAL_CHARACTER_REGEX = re.compile(r'(?=.+[!$%^~])')
HARDCODED_API_KEY_REGEX = re.compile(r'api_key|api|key', re.IGNORECASE)

API_KEY_DESCRIPTION = "Please confirm and investigate for potential API keys to determine severity."


class APIKeys(ManifestPlugin):
    def __init__(self):
        super(APIKeys, self).__init__(category="manifest", name="Potential API Key found",
                                      description=API_KEY_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self):
        with open(self.manifest_path, "r") as manifest_file:
            for line_number, line in enumerate(manifest_file):
                # TODO: Fix API_KEY_REGEX, there are too many false positives
                # if re.search(API_KEY_REGEX, line) and not re.search(SPECIAL_CHARACTER_REGEX, line):
                #     self.issues.append(Issue(
                #         category=self.category, severity=self.severity, name=self.name,
                #         description=self.description,
                #         file_object=self.manifest_path,
                #         line_number=line_number)
                #     )
                if re.search(HARDCODED_API_KEY_REGEX, line):
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=self.manifest_path,
                        line_number=line_number)
                    )


plugin = APIKeys()
