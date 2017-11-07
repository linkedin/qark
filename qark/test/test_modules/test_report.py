import csv
import os

import qark.modules.report
import qark.modules.common


def test_write_csv_section():
    issue = qark.modules.common.ReportIssue(severity=0, details="test_details", file="test_filename")
    csv_file = open("test_csv_file.csv", "w")
    writer = csv.writer(csv_file)
    qark.modules.report.write_csv_section(issue, writer)
    csv_file.close()
    file_contents_okay("INFO")

    issue = qark.modules.common.ReportIssue(severity=1, details="test_details", file="test_filename")
    csv_file = open("test_csv_file.csv", "w")
    writer = csv.writer(csv_file)
    qark.modules.report.write_csv_section(issue, writer)
    csv_file.close()
    file_contents_okay("WARNING")

    issue = qark.modules.common.ReportIssue(severity=2, details="test_details", file="test_filename")
    csv_file = open("test_csv_file.csv", "w")
    writer = csv.writer(csv_file)
    qark.modules.report.write_csv_section(issue, writer)
    csv_file.close()
    file_contents_okay("ERROR")

    issue = qark.modules.common.ReportIssue(severity=3, details="test_details", file="test_filename")
    csv_file = open("test_csv_file.csv", "w")
    writer = csv.writer(csv_file)
    qark.modules.report.write_csv_section(issue, writer)
    csv_file.close()
    file_contents_okay("VULNERABILITY")

    os.remove("test_csv_file.csv")


def file_contents_okay(severity):
    with open("test_csv_file.csv", "r") as f:
        contents = "\n".join(f.readlines())
        assert severity in contents
        assert "test_details" in contents
        assert "test_filename" in contents
