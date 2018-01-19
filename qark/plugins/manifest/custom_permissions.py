from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue

import logging
from xml.dom import minidom

log = logging.getLogger(__name__)


class CustomPermissions(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="manifest", issue_name="Custom permissions are enabled in the manifest",
                            description=("This permission can be obtained by malicious apps installed prior to this "
                                         "one, without the proper signature. Applicable to Android Devices prior to "
                                         "L (Lollipop). More info: "
                                         "https://github.com/commonsguy/cwac-security/blob/master/PERMS.md"))
        self.severity = Severity.WARNING

    def run(self, file_object):
        try:
            manifest_xml = minidom.parse(file_object)
        except Exception:
            log.exception("Failed to parse manifest file, is it valid syntax?")
            return  # do not raise a SystemExit because other checks can still be ran

        permission_sections = manifest_xml.getElementsByTagName("permission")
        for permission in permission_sections:
            try:
                if permission.attributes["android:protectionLevel"].value in ("signature", "signatureOrSystem"):
                    min_sdk = get_min_sdk(manifest_xml)
                    if min_sdk < 21:
                        self.issues.append(Issue(category=self.category, severity=self.severity,
                                                         issue_name=self.issue_name, description=self.description,
                                                         file_object=file_object))

            except KeyError:
                continue


def get_min_sdk(manifest_xml):
    """
    Given the manifest as a `minidom.parse`'d object, try to get the minimum SDK the manifest specifies.

    :param manifest_xml: object after parsing the XML
    :return: int of the version if it exists, else 1 (the default)
    """
    # TODO: try to get SDK from gradle file
    try:
        sdk_section = manifest_xml.getElementsByTagName("uses-sdk")[0]
    except IndexError:
        log.debug("Unable to get uses-sdk section")
        return 1

    try:
        return int(sdk_section.attributes["android:minSdkVersion"].value)
    except (KeyError, AttributeError):
        log.debug("Unable to get minSdkVersion from manifest")
        return 1


def get_target_sdk(manifest_xml):
    """
    Given the manifest as a `minidom.parse`'d object, try to get the target SDK the manifest specifies.

    :param manifest_xml: object after parsing the XML
    :return: int of the version if it exists, else 1 (the default)
    """
    # TODO: try to get SDK from gradle file
    try:
        sdk_section = manifest_xml.getElementsByTagName("uses-sdk")[0]
    except IndexError:
        log.debug("Unable to get uses-sdk section")
        return 1

    try:
        return int(sdk_section.attributes["android:targetSdkVersion"].value)
    except (KeyError, AttributeError):
        log.debug("Unable to get targetSdkVersion from manifest")
        return 1