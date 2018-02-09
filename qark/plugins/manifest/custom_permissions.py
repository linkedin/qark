from qark.plugins.manifest_helpers import get_min_sdk
from qark.plugins.helpers import get_manifest_out_of_files
from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue

import logging
from xml.dom import minidom

log = logging.getLogger(__name__)


class CustomPermissions(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="manifest", name="Custom permissions are enabled in the manifest",
                            description=("This permission can be obtained by malicious apps installed prior to this "
                                         "one, without the proper signature. Applicable to Android Devices prior to "
                                         "L (Lollipop). More info: "
                                         "https://github.com/commonsguy/cwac-security/blob/master/PERMS.md"))
        self.severity = Severity.WARNING

    def run(self, files, apk_constants=None):
        manifest_path = get_manifest_out_of_files(files)
        if not manifest_path:
            return

        try:
            manifest_xml = minidom.parse(manifest_path)
        except Exception:
            log.exception("Failed to parse manifest file, is it valid syntax?")
            return  # do not raise a SystemExit because other checks can still be ran

        permission_sections = manifest_xml.getElementsByTagName("permission")
        for permission in permission_sections:
            try:
                if permission.attributes["android:protectionLevel"].value in ("signature", "signatureOrSystem"):
                    if apk_constants.get("minimum_sdk", get_min_sdk(manifest_xml)) < 21:
                        self.issues.append(Issue(category=self.category, severity=self.severity,
                                                 name=self.name, description=self.description,
                                                 file_object=manifest_path))

            except KeyError:
                continue


plugin = CustomPermissions()
