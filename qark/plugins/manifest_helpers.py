from xml.etree import ElementTree
from xml.dom import minidom
import logging

from qark.xml_helpers import get_manifest_out_of_files

log = logging.getLogger(__name__)


def get_package_from_manifest(manifest_path):
    """
    Gets the package name from an AndroidManifest.xml file path

    :param manifest_path: path to android manifest
    :return: package name if exists
    """
    try:
        manifest_xml = ElementTree.parse(manifest_path)
    except IOError:
        raise

    return manifest_xml.getroot().attrib.get("package")


def get_min_sdk(manifest_xml, files=None):
    """
    Given the manifest as a `minidom.parse`'d object or path to manifest,
    try to get the minimum SDK the manifest specifies.

    :param manifest_xml: object after parsing the XML
    :param Set[str] files: list of files received from Scanner
    :return: int of the version if it exists, else 1 (the default)
    """
    if manifest_xml is None and files:
        manifest_xml = get_manifest_out_of_files(files)

    if isinstance(manifest_xml, str):
        manifest_xml = minidom.parse(manifest_xml)

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


def get_target_sdk(manifest_xml, files=None):
    """
    Given the manifest as a `minidom.parse`'d object, try to get the target SDK the manifest specifies.

    :param manifest_xml: object after parsing the XML
    :param Set[str] files: list of files received from Scanner
    :return: int of the version if it exists, else 1 (the default)
    """
    if manifest_xml is None and files:
        manifest_xml = get_manifest_out_of_files(files)

    if isinstance(manifest_xml, str):
        manifest_xml = minidom.parse(manifest_xml)

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

