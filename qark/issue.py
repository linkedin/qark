import logging
from copy import deepcopy
from enum import Enum
from json import JSONEncoder, dumps

log = logging.getLogger(__name__)


class Issue(object):
    def __init__(self, category, name, severity, description, line_number=None, file_object=None, apk_exploit_dict=None):
        """
        Create a vulnerability, used by Plugins.

        :param str category: category to put the vulnerability in the report.
        :param Severity severity: severity of the vulnerability, Severity.INFO, Severity.VULNERABILITY, Severity.ERROR, or Severity.WARNING.
        :param Tuple[int, int] line_number: line number of where the vulnerability was found.
        :param str file_object: file where the vulnerability occurred.
        :param Dict apk_exploit_dict: dictionary containing information that is needed to build the exploit apk
        """
        self.category = category

        # convert severity to its enum
        if not isinstance(severity, Severity):
            if isinstance(severity, str):
                if severity.lower() == "info":
                    severity = Severity.INFO
                elif severity.lower() == "vulnerability":
                    severity = Severity.VULNERABILITY
                elif severity.lower() == "error":
                    severity = Severity.ERROR
                elif severity.lower() == "warning":
                    severity = Severity.WARNING
                else:
                    log.info("Severity is not set for issue. Setting severity to a warning.")
                    severity = Severity.WARNING
            else:
                log.info("Severity is not set for issue. Setting severity to a warning.")
                severity = Severity.WARNING

        self.severity = severity
        self.description = description
        self.name = name
        self.line_number = line_number
        self.file_object = file_object
        self.apk_exploit_dict = apk_exploit_dict

    def __repr__(self):
        return ("Issue(category={}, name={}, severity={}, description={}, line_number={}, "
                "file_object={}, apk_exploit_dict={})".format(self.category, self.name, self.severity,
                                                              self.description, self.line_number, self.file_object,
                                                              self.apk_exploit_dict))

    def __hash__(self):
        return hash((self.name, self.file_object, self.line_number))


class Severity(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    VULNERABILITY = 3


class IssueEncoder(JSONEncoder):
    def default(self, issue):
        if isinstance(issue, Issue):
            working_dict = deepcopy(issue.__dict__)
            working_dict['severity'] = working_dict['severity'].name
            return working_dict
        else:
            log.error('Error converting issue %r to JSON %s', issue, type(issue))
            return


def issue_json(value):
    try:
        return dumps(value, cls=IssueEncoder)
    except TypeError:
        log.exception('Error encoding to JSON')
        return dumps('Error encoding to JSON')
