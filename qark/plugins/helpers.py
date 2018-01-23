import logging
import re
from xml.dom import minidom

log = logging.getLogger(__name__)


def get_min_sdk(manifest_xml):
    """
    Given the manifest as a `minidom.parse`'d object or path to manifest,
    try to get the minimum SDK the manifest specifies.

    :param manifest_xml: object after parsing the XML
    :return: int of the version if it exists, else 1 (the default)
    """
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


def get_target_sdk(manifest_xml):
    """
    Given the manifest as a `minidom.parse`'d object, try to get the target SDK the manifest specifies.

    :param manifest_xml: object after parsing the XML
    :return: int of the version if it exists, else 1 (the default)
    """
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


def get_manifest_out_of_files(files):
    """
    Parses `files` for a file that ends with `androidmanifest.xml`.
    :param Set[str] files: list of paths to files as absolute paths
    :return: manifest string if in `files`, else None
    """
    for file_name in files:
        if file_name.lower().endswith("androidmanifest.xml"):
            return file_name
    return None


def run_regex(filename, rex):
    """
    Read a file line by line, run a regular expression against the content and return list of things that require inspection
    """
    things_to_inspect = []
    try:
        with open(filename) as f:
            for curr_line in f:
                if re.search(rex, curr_line):
                    if re.match(r'^\s*(//|/\*)', curr_line):  # exclude single-line or beginning comments
                        pass
                    elif re.match(r'^\s*\*', curr_line):  # exclude lines that are comment bodies
                        pass
                    elif re.match(r'.*\*\/$', curr_line):  # exclude lines that are closing comments
                        pass
                    elif re.match(r'^\s*Log\..\(', curr_line):  # exclude Logging functions
                        pass
                    elif re.match(r'(.*)(public|private)\s(String|List)', curr_line):  # exclude declarations
                        pass
                    else:
                        things_to_inspect.append(curr_line)
    except Exception:
        log.exception("Unable to read file: " + str(filename) + " results will be inaccurate")
    return things_to_inspect
