import logging
from xml.dom import minidom

from qark.issue import Issue, Severity
from qark.plugins.helpers import get_min_sdk, get_manifest_out_of_files
from qark.scanner.plugin import BasePlugin

log = logging.getLogger(__name__)

TAP_JACKING = ("Since the minSdkVersion is less that 9, it is likely this application is vulnerable to TapJacking. "
               "QARK made no attempt to confirm, as the protection would have to be custom code, which is difficult for"
               " QARK to examine and understand properly. This vulnerability allows a malicious application to lay on "
               "top of this app, while letting the key strokes pass through to the application below. This can cause "
               "users to take unwanted actions, within the victim application, similar to Clickjacking on websites. "
               "Please select the appropriate options in the exploitation menus to verify manually using QARK's "
               "exploit APK. Note: The QARK proof-of-concept is transparent, but in real-world attacks, it would "
               "likely not be. This is done solely to aid in testing. For more information: "
               "https://media.blackhat.com/ad-12/Niemietz/bh-ad-12-androidmarcus_niemietz-WP.pdf")


class MinSDK(BasePlugin):
    """This plugin will create issues depending on the manifest's minimum SDK. For instance
    tapjacking is only protected when min_sdk > 9 (or custom code is used)."""
    def __init__(self):
        BasePlugin.__init__(self, category="manifest")
        self.severity = Severity.WARNING

    def run(self, files, apk_constants=None):
        try:
            min_sdk = apk_constants["min_sdk"]
        except (KeyError, TypeError):
            manifest_path = get_manifest_out_of_files(files)
            if not manifest_path:
                return

            try:
                manifest_xml = minidom.parse(manifest_path)
            except Exception:
                log.exception("Failed to parse manifest file, is it valid syntax?")
                return  # do not raise a SystemExit because other checks can still be ran
            min_sdk = get_min_sdk(manifest_xml)

        if min_sdk < 9:
            self.issues.append(Issue(category=self.category, name="Tap Jacking possible",
                                     severity=Severity.VULNERABILITY, description=TAP_JACKING))


plugin = MinSDK()
