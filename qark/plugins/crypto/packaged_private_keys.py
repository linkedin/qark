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

    def run(self, filepath, file_contents=None, **kwargs):
        if not file_contents:
            return

        for regex in PackagedPrivateKeys.PRIVATE_KEY_REGEXES:
            if run_regex(filepath, regex):
                log.debug("It appears there is a private key embedded in your application: %s", filepath)
                description = "It appears there is a private key embedded in your application in the following file:"
                self.issues.append(
                    Issue(self.category, self.name, self.severity, description, file_object=filepath))


plugin = PackagedPrivateKeys()
