import logging

from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue
from qark.plugins.utils import run_regex

log = logging.getLogger(__name__)


class PackagedPrivateKeys(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="crypto", name="Encryption keys are packaged with the application")

        self.severity = Severity.VULNERABILITY

    def run(self, file_object):
        if run_regex(file_object, r'PRIVATE\sKEY'):
            log.info("It appears there is a private key embedded in your application: %s", file_object)
            description = "It appears there is a private key embedded in your application in the following file:"
            self.issues.append(
                Issue(self.category, self.name, self.severity, description, file_object=file_object))
