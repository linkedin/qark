from qark.plugins.helpers import get_manifest_out_of_files
from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue

import logging
from xml.dom import minidom

log = logging.getLogger(__name__)


class ManifestBackupAllowed(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="manifest", name="Backup is allowed in manifest",
                            description=("Backups enabled: Potential for data theft via local attacks via adb backup, "
                                         "if the device has USB debugging enabled (not common). "
                                         "More info: "
                                         "http://developer.android.com/reference/android/R.attr.html#allowBackup"))
        self.severity = Severity.WARNING

    def run(self, files, apk_constants=None):
        manifest_path = get_manifest_out_of_files(files)
        try:
            manifest_xml = minidom.parse(manifest_path)
        except Exception:
            log.exception("Failed to parse manifest file, is it valid syntax?")
            return  # do not raise a SystemExit because other checks can still be ran

        application_sections = manifest_xml.getElementsByTagName("application")
        for application in application_sections:
            if "android:allowBackup" in application.attributes.keys():
                self.issues.append(Issue(category=self.category, severity=self.severity,
                                         name=self.name, description=self.description,
                                         file_object=manifest_path))


plugin = ManifestBackupAllowed()
