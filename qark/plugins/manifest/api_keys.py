import logging
import re

from qark.issue import Severity, Issue
from qark.scanner.plugin import BasePlugin
from qark.xml_helpers import get_manifest_out_of_files

log = logging.getLogger(__name__)

API_KEY_REGEX = re.compile(r'(?=.{20,})(?=.+\d)(?=.+[a-z])(?=.+[A-Z])')
SPECIAL_CHARACTER_REGEX = re.compile(r'(?=.+[!$%^~])')
HARDCODED_API_KEY_REGEX = re.compile(r'API_KEY|api_key|API|api|key')

API_KEY_DESCRIPTION = "Please confirm and investigate the API key to determine its severity."


class APIKeys(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="manifest", name="Potential API Key found",
                            description=API_KEY_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self, files, apk_constants=None):
        manifest_path = get_manifest_out_of_files(files)
        if not manifest_path:
            return

        with open(manifest_path, "r") as manifest_file:
            for line_number, line in enumerate(manifest_file):
                if re.search(API_KEY_REGEX, line) and not re.search(SPECIAL_CHARACTER_REGEX, line):
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=manifest_path,
                        line_number=line_number)
                    )
                elif re.search(HARDCODED_API_KEY_REGEX, line):
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=manifest_path,
                        line_number=line_number)
                    )


plugin = APIKeys()
