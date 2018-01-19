import logging

from plyj.parser import Parser

from qark.scanner.plugin import BasePlugin
from qark.vulnerability import Severity, Vulnerability

log = logging.getLogger(__name__)


class SeedWithSecureRandom(BasePlugin):
    def __init__(self):

        BasePlugin.__init__(self, category="crypto", issue_name="Random number generator is seeded with SecureSeed",
                            description=("Specifying a fixed seed will cause a predictable sequence of numbers. "
                                         "This may be useful for testing, but not for secure use"))

        self.severity = Severity.WARNING
        self.parser = Parser()
        self.tree = None

    def run(self, file_object):
        try:
            self.tree = self.parser.parse_file(file_object)
            if not self.tree:
                return
        except Exception:
            log.exception("Unable to create tree for %s" + str(file_object))
            return

        for import_decl in self.tree.import_declarations:
            for setter_func in ("setSeed", "generateSeed"):
                if 'SecureRandom' in import_decl.name.value and setter_func in str(self.tree):
                    self.issues.append(Vulnerability(self.category, self.issue_name, self.severity, self.description,
                                                     file_object=file_object))
