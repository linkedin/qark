import logging
import re

from qark.issue import Severity, Issue
from qark.scanner.plugin import FileContentsPlugin

log = logging.getLogger(__name__)

PHONE_IDENTIFIER_DESCRIPTION = (
    "Access of phone number or IMEI, is detected. Avoid storing or transmitting this data."
)

TELEPHONY_MANAGER_VARIABLE_NAMES_REGEX = re.compile(r'(android\.telephony\.)?TelephonyManager\s(\w*?)([,);]|(\s=))')
TELEPHONY_MANAGER_REGEX = re.compile(r'android\.telephony\.TelephonyManager')
TELEPHONY_INLINE_REGEX = re.compile(r'\({2,}(android.telephony.)?TelephonyManager\)\w*?\.getSystemService\([\'\"]phone'
                                    r'[\'\"]\){2,}\.(getLine1Number|getDeviceId)')


class PhoneIdentifier(FileContentsPlugin):
    def __init__(self):
        super(PhoneIdentifier, self).__init__(category="file", name="Phone number or IMEI detected",
                                              description=PHONE_IDENTIFIER_DESCRIPTION)
        self.severity = Severity.INFO

    def run(self):
        if re.search(TELEPHONY_MANAGER_REGEX, self.file_contents):
            if re.search(TELEPHONY_INLINE_REGEX, self.file_contents):
                self._add_issue(java_path=self.file_path)

            else:

                for match in re.finditer(TELEPHONY_MANAGER_VARIABLE_NAMES_REGEX, self.file_contents):

                    for variable_name in match.group(2):

                        if re.search(r'{var_name}\.(getLine1Number|getDeviceId)\(.*?\)'.format(var_name=variable_name),
                                     self.file_contents):
                            self._add_issue(java_path=self.file_path)

    def _add_issue(self, java_path):
        self.issues.append(Issue(
            category=self.category, severity=self.severity, name=self.name,
            description=self.description,
            file_object=java_path)
        )


plugin = PhoneIdentifier()
