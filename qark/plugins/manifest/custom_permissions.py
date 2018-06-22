from qark.scanner.plugin import ManifestPlugin

import logging

from qark.issue import Severity, Issue
from qark.plugins.manifest_helpers import get_min_sdk

log = logging.getLogger(__name__)

SIGNATURE_OR_SIGNATURE_OR_SYSTEM_DESCRIPTION = (
    "This permission can be obtained by malicious apps installed prior to this "
    "one, without the proper signature. Applicable to Android Devices prior to "
    "L (Lollipop). More info: "
    "https://github.com/commonsguy/cwac-security/blob/master/PERMS.md"
)
SIGNATURE_OR_SIGNATURE_OR_SYSTEM_SEVERITY = Severity.WARNING

DANGEROUS_PERMISSION_DESCRIPTION = (
    "This permission can give a requesting application access to private user data or control over the "
    "device that can negatively impact the user."
)


class CustomPermissions(ManifestPlugin):
    def __init__(self):
        super(CustomPermissions, self).__init__(category="manifest",
                                                name="Custom permissions are enabled in the manifest",
                                                description=(
                                                    "This permission can be obtained by malicious apps installed prior to this "
                                                    "one, without the proper signature. Applicable to Android Devices prior to "
                                                    "L (Lollipop). More info: "
                                                    "https://github.com/commonsguy/cwac-security/blob/master/PERMS.md"))

        self.severity = Severity.WARNING

    def run(self):
        permission_sections = self.manifest_xml.getElementsByTagName("permission")
        for permission in permission_sections:
            try:
                protection_level = permission.attributes["android:protectionLevel"].value
            except KeyError:
                continue

            if protection_level in ("signature", "signatureOrSystem"):
                if self.min_sdk < 21:
                    self.issues.append(Issue(category=self.category,
                                             severity=SIGNATURE_OR_SIGNATURE_OR_SYSTEM_SEVERITY,
                                             name=self.name,
                                             description=SIGNATURE_OR_SIGNATURE_OR_SYSTEM_DESCRIPTION,
                                             file_object=self.manifest_path))

            elif protection_level == "dangerous":
                self.issues.append(Issue(category=self.category,
                                         severity=Severity.INFO,
                                         name=self.name,
                                         description=DANGEROUS_PERMISSION_DESCRIPTION,
                                         file_object=self.manifest_path))


plugin = CustomPermissions()
