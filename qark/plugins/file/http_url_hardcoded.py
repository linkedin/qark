import logging
import re
import os

import javalang

from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

HARDCODED_HTTP_DESCRIPTION = (
    "Application contains hardcoded HTTP url: {http_url}, unless HSTS is implemented, this request can be "
    "intercepted and modified by a man-in-the-middle attack."
)

HTTP_URL_REGEX = re.compile(r'http://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class HardcodedHTTP(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="file", name="Hardcoded HTTP url found",
                            description=HARDCODED_HTTP_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self, filepath, file_contents=None, **kwargs):
        if not file_contents or not os.path.splitext(filepath.lower())[1] == ".java":
            return

        for line_number, line in enumerate(file_contents.split('\n')):
            http_url_match = re.search(HTTP_URL_REGEX, line)
            if http_url_match:
                self.issues.append(Issue(
                    category=self.category, severity=self.severity, name=self.name,
                    description=self.description.format(http_url=http_url_match.group(0)),
                    file_object=filepath,
                    line_number=(line_number, 0))
                )


plugin = HardcodedHTTP()
