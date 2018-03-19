from qark.plugins.manifest_helpers import get_min_sdk
from qark.scanner.plugin import ManifestPlugin
from qark.issue import Severity, Issue

import logging

from qark.issue import Severity, Issue
from qark.plugins.manifest_helpers import get_min_sdk
from qark.scanner.plugin import BasePlugin
from qark.xml_helpers import get_manifest_out_of_files

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
    def __init__(self, **kwargs):
        kwargs.update(dict(category="manifest", name="Custom permissions are enabled in the manifest",
                           description=("This permission can be obtained by malicious apps installed prior to this "
                                        "one, without the proper signature. Applicable to Android Devices prior to "
                                        "L (Lollipop). More info: "
                                        "https://github.com/commonsguy/cwac-security/blob/master/PERMS.md")))

        super(CustomPermissions, self).__init__(**kwargs)

        self.severity = Severity.WARNING

    def run(self, files, apk_constants=None):
        permission_sections = self.manifest_xml.getElementsByTagName("permission")
        for permission in permission_sections:
            try:
                if permission.attributes["android:protectionLevel"].value in ("signature", "signatureOrSystem"):
                    if apk_constants.get("minimum_sdk", get_min_sdk(self.manifest_xml)) < 21:
                        self.issues.append(Issue(category=self.category, severity=self.severity,
                                                 name=self.name, description=self.description,
                                                 file_object=self.manifest_path))

                protection_level = permission.attributes["android:protectionLevel"].value
            except KeyError:
                continue

            if protection_level in ("signature", "signatureOrSystem"):
                if apk_constants.get("minimum_sdk", get_min_sdk(manifest_xml)) < 21:
                    self.issues.append(Issue(category=self.category,
                                             severity=SIGNATURE_OR_SIGNATURE_OR_SYSTEM_SEVERITY,
                                             name=self.name,
                                             description=SIGNATURE_OR_SIGNATURE_OR_SYSTEM_DESCRIPTION,
                                             file_object=manifest_path))

            elif protection_level == "dangerous":
                self.issues.append(Issue(category=self.category,
                                         severity=Severity.INFO,
                                         name=self.name,
                                         description=DANGEROUS_PERMISSION_DESCRIPTION,
                                         file_object=manifest_path))


plugin = CustomPermissions()
