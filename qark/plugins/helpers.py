import logging
import os
import re
import shutil
import os
from xml.dom import minidom

from javalang.tree import MethodInvocation

log = logging.getLogger(__name__)

EXCLUDE_REGEXES = (r'^\s*(//|/\*)',
                   r'^\s*\*',
                   r'.*\*\/$',
                   r'^\s*Log\..\(',
                   r'(.*)(public|private)\s(String|List)')

EXCLUSION_REGEX = re.compile("|".join(EXCLUDE_REGEXES))

EXTRAS = (r'(getExtras\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getStringExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getIntExtra\s*[0-9A-Za-z_\"\'.]+)',
          r'(getIntArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getFloatExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getFloatArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getDoubleExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getDoubleArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getCharExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getCharArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getByteExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getByteArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getBundleExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getBooleanExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getBooleanArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getCharSequenceArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getCharSequenceArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getCharSequenceExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getInterArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getLongArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getLongExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getParcelableArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getParcelableArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getParcelableExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getSeriablizableExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getShortArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getShortExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getStringArrayExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          r'(getStringArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+)',
          # These are not necessarily Intent extras, but may contain them
          r'(getString\(\s*[0-9A-Za-z_\"\'.]+)')

EXTRAS_REGEX = re.compile("|".join(EXTRAS))


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


def remove_dict_entry_by_value(dictionary, value):
    return {k: v for k, v in dictionary.items() if v != dictionary.get(value)}


def valid_method_invocation(method_invocation, method_name, num_arguments):
    """
    Determines if a `MethodInvocation` has the name `method_name` and the number of arguments `num_arguments`

    :param MethodInvocation method_invocation: the javalang MethodInvocation
    :param str method_name: the name of the method that should be called
    :param int num_arguments: the number of arguments the method should contain
    :return: Whether the method invocation matches the parameters
    :rtype: bool
    """
    return (isinstance(method_invocation, MethodInvocation)
            and method_invocation.member == method_name
            and len(method_invocation.arguments) == num_arguments)


def get_min_sdk_from_files(files, apk_constants=None):
    """
    Get the min_sdk from either the `apk_constants` if it exists, or the manifest file in `files` if it exists. If
    neither exists, return 1 as the default minimum SDK

    :param files:
    :return:
    """
    try:
        # int conversion to change it if it is a NoneType, which will throw TypeError
        return int(apk_constants["min_sdk"])
    except (KeyError, TypeError):
        for decompiled_file in files:
            if decompiled_file.lower().endswith("{separator}androidmanifest.xml".format(separator=os.sep)):
                return get_min_sdk(decompiled_file)
    return 1


def copy_directory_to_location(directory_to_copy, destination):
    try:
        shutil.copytree(src=directory_to_copy, dst=destination)
    except Exception:
        raise


def java_files_from_files(files):
    """
    Returns a generator of everything in `files` that ends with the `.java` extension.

    :param list files:
    :return: generator of file paths
    """
    return (file_path for file_path in files if os.path.splitext(file_path.lower())[1] == '.java')


def copy_directory_to_location(directory_to_copy, destination):
    try:
        shutil.copytree(src=directory_to_copy, dst=destination)
    except Exception:
        raise


def find_extras(path):
    """
    Runs the regexes in `EXTRAS` against the file contents at `filepath`.

    :param str path: path to file to find extras
    :return: list of extras in use at path
    :rtype: list
    """
    extras = []
    for regex in EXTRAS:
        list_of_usages = run_regex(path, regex)
        for extra in list_of_usages:
            # remove extraneous information
            extra = re.sub(r'^get', '', extra)
            extra = re.sub(r'\\.*', '', extra)
            extra = re.sub(r'Extra.*', '', extra)

            extras.append(extra)

    extras = list(set(extras))
    return extras


def find_file(path, regex):
    regex = re.compile(regex)
    res = []
    for root, _, fnames in os.walk(path):
        for fname in fnames:
            if regex.match(fname):
                res.append(os.path.join(root, fname))
    return res
