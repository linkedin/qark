from __future__ import absolute_import

import logging

import click

from qark.decompiler.decompiler import Decompiler
from qark.scanner.scanner import Scanner
from qark.report import Report

log = logging.getLogger(__name__)


@click.command()
@click.option("--sdk-path", type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help="Path to the downloaded SDK directory if already downloaded")
@click.option("--build-path", type=click.Path(resolve_path=True, file_okay=False),
              help="Path to place decompiled files and exploit APK", default="build", show_default=True)
@click.option("--debug/--no-debug", default=False, help="Show debugging statements (helpful for issues)",
              show_default=True)
@click.option("--apk", "source", help="APK to decompile and run static analysis. If passed, "
                                      "the --java option is not used",
              type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True))
@click.option("--java", "source", type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True),
              help="A directory containing Java code, or a Java file, to decompile and run static analysis. If passed,"
                   "the --apk option is not used")
@click.option("--report-type", type=click.Choice(["html", "xml", "json", "csv"]),
              help="Type of report to generate along with terminal output", default="html", show_default=True)
@click.option("--exploit-apk/--no-exploit-apk", default=False,
              help="Create an exploit APK targetting a few vulnerabilities", show_default=True)
@click.version_option()
def cli(sdk_path, build_path, debug, source, report_type, exploit_apk):
    click.secho("Decompiling...")
    decompiler = Decompiler(path_to_apk=source, build_directory=build_path)
    decompiler.decompile()

    click.secho("Running scans...")
    scanner = Scanner(decompiler=decompiler)
    scanner.run()
    click.secho("Finish scans...")

    click.secho("Writing report...")
    report = Report(issues=scanner.issues)
    report.generate_report_file(file_type=report_type)
    click.secho("Finish writing report...")


# @cli.command()
@click.option("--apk", required=True, type=click.Path(exists=True, resolve_path=True, file_okay=True,
                                                           dir_okay=False),
              help="Path to APK to decompile")
@click.option("--build-path", type=click.Path(resolve_path=True, file_okay=False),
              help="Path to place decompiled files and exploit APK", default="build", show_default=True)
def decompile(apk, build_path):
    pass
