import logging
import os
import re
import shutil
from io import open

from javalang.tree import MethodInvocation

from qark.plugins.manifest_helpers import get_min_sdk
from qark.utils import is_java_file

log = logging.getLogger(__name__)

EXCLUDE_REGEXES = (r'^\s*(//|/\*)',
                   r'^\s*\*',
                   r'.*\*\/$',
                   r'^\s*Log\..\(',
                   r'(.*)(public|private)\s(String|List)')

EXCLUSION_REGEX = re.compile("|".join(EXCLUDE_REGEXES))


def run_regex(filename, rex, encoding="utf-8"):
    """
    Read a file line by line, run a regular expression against the content and return list of things that require inspection

    :param str filename: path to file
    :param Union[re.Pattern, str, bytes] rex: can be a compiled regex or a string/bytes of the regex to search
    :param str encoding: encoding to read the files
    """
    things_to_inspect = []
    try:
        with open(filename, encoding=encoding) as f:
            for curr_line in f:
                if re.search(rex, curr_line):
                    # exclude everything in EXCLUDE_REGEXES
                    if not re.match(EXCLUSION_REGEX, curr_line):
                        things_to_inspect.append(curr_line)
    except IOError:
        log.debug("Unable to open file: %s results will be inaccurate", filename)
    except UnicodeDecodeError:
        pass  # Since the user passes in the encoding we eat this error - any occurrences of this are expected
    except Exception:
        log.exception("Failed to read file: %s", filename)
    return things_to_inspect


def java_files_from_files(files):
    """
    Returns a generator of everything in `files` that ends with the `.java` extension.

    :param list files:
    :return: generator of file paths
    """
    return (file_path for file_path in files if is_java_file(file_path))


def remove_dict_entry_by_value(dictionary, value):
    """Helper to remove an entry in a dictionary by its value instead of its key."""
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

    :param Iterable files: file names that should be iterated over
    :param Dict apk_constants: dictionary that can have constants throughout the apk
    :return: min_sdk if it exists or 1
    :rtype: int
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
    log.debug("Copying from %s to %s", directory_to_copy, destination)
    try:
        shutil.copytree(src=directory_to_copy, dst=destination)
    except Exception:
        raise
