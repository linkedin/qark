import logging

from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue
from qark.plugins.helpers import run_regex

log = logging.getLogger(__name__)


class PackagedPrivateKeys(BasePlugin):

    PRIVATE_KEY_REGEXES = (r'PRIVATE\sKEY',)

    def __init__(self):
        BasePlugin.__init__(self, category="crypto", name="Encryption keys are packaged with the application")

        self.severity = Severity.VULNERABILITY

    def run(self, files, apk_constants=None):
        for file_path in files:
            for regex in PackagedPrivateKeys.PRIVATE_KEY_REGEXES:
                if run_regex(file_path, regex):
                    log.debug("It appears there is a private key embedded in your application: %s", file_path)
                    description = "It appears there is a private key embedded in your application in the following file:"
                    self.issues.append(
                        Issue(self.category, self.name, self.severity, description, file_object=file_path))
