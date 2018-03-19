from qark.plugins.manifest_helpers import get_min_sdk
from qark.scanner.plugin import ManifestPlugin
from qark.issue import Severity, Issue

import logging

log = logging.getLogger(__name__)


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

            except KeyError:
                continue


plugin = CustomPermissions()
