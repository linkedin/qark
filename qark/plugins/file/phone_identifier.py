import logging
import re

from qark.issue import Severity, Issue
from qark.plugins.helpers import java_files_from_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

PHONE_IDENTIFIER_DESCRIPTION = (
    "Access of phone number or IMEI, is detected. Avoid storing or transmitting this data."
)

TELEPHONY_MANAGER_VARIABLE_NAMES_REGEX = re.compile(r'(android\.telephony\.)?TelephonyManager\s(\w*?)([,);]|(\s=))')
TELEPHONY_MANAGER_REGEX = re.compile(r'android\.telephony\.TelephonyManager')
TELEPHONY_INLINE_REGEX = re.compile(r'\({2,}(android.telephony.)?TelephonyManager\)\w*?\.getSystemService\([\'\"]phone'
                                    r'[\'\"]\){2,}\.(getLine1Number|getDeviceId)')


class PhoneIdentifier(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="file", name="Phone number or IMEI detected",
                            description=PHONE_IDENTIFIER_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self, files, apk_constants=None):
        java_files = java_files_from_files(files)

        for java_file in java_files:
            self._process(java_file)

    def _process(self, java_file):
        try:
            with open(java_file, "r") as java_file_to_read:
                file_contents = java_file_to_read.read()
        except IOError:
            log.debug("File does not exist %s, continuing", java_file)
            return

        if re.search(TELEPHONY_MANAGER_REGEX, file_contents):
            if re.search(TELEPHONY_INLINE_REGEX, file_contents):
                self._add_issue(java_path=java_file)

            else:

                for match in re.finditer(TELEPHONY_MANAGER_VARIABLE_NAMES_REGEX, file_contents):

                    for variable_name in match.group(2):

                        if re.search(r'{var_name}\.(getLine1Number|getDeviceId)\(.*?\)'.format(var_name=variable_name),
                                     file_contents):
                            self._add_issue(java_path=java_file)

    def _add_issue(self, java_path):
        self.issues.append(Issue(
            category=self.category, severity=self.severity, name=self.name,
            description=self.description,
            file_object=java_path)
        )


plugin = PhoneIdentifier()
