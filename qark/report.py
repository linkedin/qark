from __future__ import absolute_import

from os import path

from jinja2 import Environment, PackageLoader, select_autoescape, Template

from qark.issue import (Issue, Severity, issue_json)  # noqa:F401 These are expected to be used later.
from qark.utils import create_directories_to_path

DEFAULT_REPORT_PATH = path.join(path.dirname(path.realpath(__file__)), 'report', '')


jinja_env = Environment(
    loader=PackageLoader('qark', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

jinja_env.filters['issue_json'] = issue_json


class Report(object):
    """An object to store issues against and to generate reports in different formats.

    There is one instance created per QARK run and it uses a classic Singleton pattern
    to make it easy to get a reference to that instance anywhere in QARK.
    """

    # The one instance to rule them all
    # http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html#the-singleton
    __instance = None

    def __new__(cls, issues=None, report_path=None):
        if Report.__instance is None:
            Report.__instance = object.__new__(cls)

        return Report.__instance

    def __init__(self, issues=None, report_path=None):
        """This will give you an instance of a report, with a default report path which is local
        to where QARK is on the file system.

        :param report_path: The path to the report directory where all generated report files will be written.
        :type report_path: str or None

        """
        self.issues = issues if issues else []
        self.report_path = report_path or DEFAULT_REPORT_PATH

    def generate(self, file_type='html', template_file=None):
        """This method uses Jinja2 to generate a standalone HTML version of the report.

        :param str file_type:     The type of file for the report. Defaults to 'html'.
        :param str template_file: The path to an optional template file to override the default.
        :return: Path to the written report
        :rtype: str
        """
        create_directories_to_path(self.report_path)

        full_report_path = path.join(self.report_path, 'report.{file_type}'.format(file_type=file_type))

        with open(full_report_path, mode='w') as report_file:
            if not template_file:
                template = jinja_env.get_template('{file_type}_report.jinja'.format(file_type=file_type))
            else:
                template = Template(template_file)
            report_file.write(template.render(issues=list(self.issues)))

        return full_report_path
