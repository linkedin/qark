import logging
import os
import re
from xml.dom import minidom

log = logging.getLogger(__name__)

EXCLUDE_REGEXES = (r'^\s*(//|/\*)',
                   r'^\s*\*',
                   r'.*\*\/$',
                   r'^\s*Log\..\(',
                   r'(.*)(public|private)\s(String|List)')

EXCLUSION_REGEX = re.compile("|".join(EXCLUDE_REGEXES))


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

    :param str filename: path to file
    :param rex: can be a compiled regex or a string of the regex to search
    """
    things_to_inspect = []
    try:
        with open(filename) as f:
            for curr_line in f:
                if re.search(rex, curr_line):
                    # exclude everythingin EXCLUDE_REGEXES
                    if not re.match(EXCLUSION_REGEX, curr_line):
                        things_to_inspect.append(curr_line)
    except IOError:
        log.debug("Unable to open file: %s results will be inaccurate", filename)
    except UnicodeDecodeError:
        log.debug("Error reading file: %s most likely it is of an invalid type", filename)
    except Exception:
        log.exception("Failed to read file: %s", filename)
    return things_to_inspect


def java_files_from_files(files):
    """
    Returns a generator of everything in `files` that ends with the `.java` extension.

    :param list files:
    :return: generator of file paths
    """
    return (file_path for file_path in files if os.path.splitext(file_path.lower())[1] == '.java')
