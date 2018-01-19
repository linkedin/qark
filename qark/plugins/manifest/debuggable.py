from qark.plugins.helpers import get_manifest_out_of_files
from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue

import logging
from xml.dom import minidom

log = logging.getLogger(__name__)


class DebuggableManifest(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="manifest", name="Manifest is manually set to debug",
                            description=("The android:debuggable flag is manually set to true in the"
                                         " AndroidManifest.xml. This will cause your application to be debuggable "
                                         "in production builds and can result in data leakage "
                                         "and other security issues. It is not necessary to set the "
                                         "android:debuggable flag in the manifest, it will be set appropriately "
                                         "automatically by the tools. More info: "
                                         "http://developer.android.com/guide/topics/manifest/application-element.html#debug"))
        self.severity = Severity.VULNERABILITY

    def run(self, files, apk_constants=None):
        manifest_path = get_manifest_out_of_files(files)
        try:
            manifest_xml = minidom.parse(manifest_path)
        except Exception:
            log.exception("Failed to parse manifest file, is it valid syntax?")
            return  # do not raise a SystemExit because other checks can still be ran

        application_sections = manifest_xml.getElementsByTagName("application")
        for application in application_sections:
            try:
                if application.attributes["android:debuggable"].value.lower() == "true":
                    self.issues.append(Issue(category=self.category, severity=self.severity,
                                             name=self.name, description=self.description,
                                             file_object=manifest_path))
            except (KeyError, AttributeError):
                log.debug("Application section does not have debuggable flag, continuing")
                continue


plugin = DebuggableManifest()
