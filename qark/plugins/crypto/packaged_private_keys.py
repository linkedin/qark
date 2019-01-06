import logging
import re

from qark.issue import Severity, Issue
from qark.plugins.helpers import run_regex
from qark.scanner.plugin import FileContentsPlugin

log = logging.getLogger(__name__)


class PackagedPrivateKeys(FileContentsPlugin):
    PRIVATE_KEY_REGEXES = (
        re.compile(r'PRIVATE\sKEY'),
    )

    def __init__(self):
        super(PackagedPrivateKeys, self).__init__(category="crypto",
                                                  name="Encryption keys are packaged with the application")

        self.severity = Severity.VULNERABILITY

    def run(self):
        for regex in PackagedPrivateKeys.PRIVATE_KEY_REGEXES:
            if run_regex(self.file_path, regex):
                log.debug("It appears there is a private key embedded in your application: %s", self.file_path)
                description = "It appears there is a private key embedded in your application in the following file:"
                self.issues.append(
                    Issue(self.category, self.name, self.severity, description, file_object=self.file_path))


plugin = PackagedPrivateKeys()
