import logging
import re

from qark.issue import Severity, Issue
from qark.utils import is_java_file
from qark.scanner.plugin import FileContentsPlugin

log = logging.getLogger(__name__)

HARDCODED_HTTP_DESCRIPTION = (
    "Application contains hardcoded HTTP url: {http_url}, unless HSTS is implemented, this request can be "
    "intercepted and modified by a man-in-the-middle attack."
)

HTTP_URL_REGEX = re.compile(r'http://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class HardcodedHTTP(FileContentsPlugin):
    def __init__(self):
        super(HardcodedHTTP, self).__init__(category="file", name="Hardcoded HTTP url found",
                                            description=HARDCODED_HTTP_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self):
        if not is_java_file(self.file_path):
            return

        for line_number, line in enumerate(self.file_contents.split('\n')):
            http_url_match = re.search(HTTP_URL_REGEX, line)
            if http_url_match:
                self.issues.append(Issue(
                    category=self.category, severity=self.severity, name=self.name,
                    description=self.description.format(http_url=http_url_match.group(0)),
                    file_object=self.file_path,
                    line_number=(line_number, 0))
                )


plugin = HardcodedHTTP()
