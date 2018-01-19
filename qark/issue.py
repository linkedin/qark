import logging
from enum import Enum
from json import JSONEncoder, dumps
from copy import deepcopy


log = logging.getLogger(__name__)


class Issue(object):
    def __init__(self, category, name, severity, description, line_number=None, file_object=None):
        """
        Create a vulnerability, used by Plugins.

        :param str category: category to put the vulnerability in the report.
        :param severity: severity of the vulnerability, Severity.INFO, Severity.VULNERABILITY, Severity.ERROR, or Severity.WARNING.
        :param line_number: line number of where the vulnerability was found.
        :param file_object: file where the vulnerability occurred.
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
            raise TypeError('Expecting an object of type Issue. Got object of type {}'.format(type(Issue)))


def issue_json(value):
    try:
        return dumps(value, cls=IssueEncoder)
    except TypeError:
        return dumps('Error encoding to JSON')
