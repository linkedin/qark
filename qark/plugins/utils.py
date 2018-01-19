import logging
import re

log = logging.getLogger(__name__)


def run_regex(filename, rex):
    """
    Read a file line by line, run a regular expression against the content and return list of things that require inspection
    """
    things_to_inspect = []
    try:
        with open(filename) as f:
            content = f.readlines()
            for y in content:
                if re.search(rex, y):
                    if re.match(r'^\s*(//|/\*)', y):  # exclude single-line or beginning comments
                        pass
                    elif re.match(r'^\s*\*', y):  # exclude lines that are comment bodies
                        pass
                    elif re.match(r'.*\*\/$', y):  # exclude lines that are closing comments
                        pass
                    elif re.match(r'^\s*Log\..\(', y):  # exclude Logging functions
                        pass
                    elif re.match(r'(.*)(public|private)\s(String|List)', y):  # exclude declarations
                        pass
                    else:
                        things_to_inspect.append(y)
    except Exception as e:
        log.error("Unable to read file: " + str(filename) + " results will be inaccurate")
    return things_to_inspect
