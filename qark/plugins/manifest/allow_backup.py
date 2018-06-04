from qark.scanner.plugin import ManifestPlugin
from qark.issue import Severity, Issue

import logging

log = logging.getLogger(__name__)


class ManifestBackupAllowed(ManifestPlugin):
    def __init__(self, **kwargs):
        kwargs.update(dict(category="manifest", name="Backup is allowed in manifest",
                           description=(
                               "Backups enabled: Potential for data theft via local attacks via adb "
                               "backup, if the device has USB debugging enabled (not common). "
                               "More info: "
                               "http://developer.android.com/reference/android/R.attr.html#allowBackup")))

        super(ManifestBackupAllowed, self).__init__(**kwargs)

        self.severity = Severity.WARNING

    def run(self, **kwargs):
        if not self.manifest_xml:
            return

        application_sections = self.manifest_xml.getElementsByTagName("application")

        for application in application_sections:
            if "android:allowBackup" in application.attributes.keys():
                self.issues.append(Issue(category=self.category, severity=self.severity,
                                         name=self.name, description=self.description,
                                         file_object=self.manifest_path))


plugin = ManifestBackupAllowed()
