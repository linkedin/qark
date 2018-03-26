from __future__ import absolute_import

import os
import logging
from sys import stderr

import click

from qark.decompiler.decompiler import Decompiler
from qark.scanner.scanner import Scanner
from qark.report import Report
from qark.apk_builder import APKBuilder

DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "qark_debug.log")


@click.command()
@click.option("--sdk-path", type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help="Path to the downloaded SDK directory if already downloaded")
@click.option("--build-path", type=click.Path(resolve_path=True, file_okay=False),
              help="Path to place decompiled files and exploit APK", default="build", show_default=True)
@click.option("--debug/--no-debug", default=False, help="Show debugging statements (helpful for issues)",
              show_default=True)
@click.option("--apk", "source", help="APK to run and run static analysis. If passed, "
                                      "the --java option is not used",
              type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True))
@click.option("--java", "source", type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True),
              help="A directory containing Java code, or a Java file, to run and run static analysis. If passed,"
                   "the --apk option is not used")
@click.option("--report-type", type=click.Choice(["html", "xml", "json", "csv"]),
              help="Type of report to generate along with terminal output", default="html", show_default=True)
@click.option("--exploit-apk/--no-exploit-apk", default=False,
              help="Create an exploit APK targetting a few vulnerabilities", show_default=True)
@click.version_option()
@click.pass_context
def cli(ctx, sdk_path, build_path, debug, source, report_type, exploit_apk):
    if not source:
        click.secho("Please pass a source for scanning through either --java or --apk")
        click.secho(ctx.get_help())
        return

    if exploit_apk and not sdk_path:
        click.secho("Please provide path to android SDK if building exploit APK.")
        return

    # Debug controls the output to stderr, debug logs are ALWAYS stored in `qark_debug.log`
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    initialize_logging(level)

    click.secho("Decompiling...")
    decompiler = Decompiler(path_to_source=source, build_directory=build_path)
    decompiler.run()

    click.secho("Running scans...")
    scanner = Scanner(manifest_path=decompiler.manifest_path, path_to_source=decompiler.path_to_source,
                      build_directory=decompiler.build_directory)
    scanner.run()
    click.secho("Finish scans...")

    click.secho("Writing report...")
    report = Report(issues=scanner.issues)
    report_path = report.generate(file_type=report_type)
    click.secho("Finish writing report to %s...", report_path)

    if exploit_apk:
        click.secho("Building exploit APK...")
        exploit_builder = APKBuilder(exploit_apk_path=build_path, issues=scanner.issues, apk_name=decompiler.apk_name,
                                     manifest_path=decompiler.manifest_path, sdk_path=sdk_path)
        exploit_builder.build()
        click.secho("Finish building exploit APK...")


# @cli.command()
@click.option("--apk", required=True, type=click.Path(exists=True, resolve_path=True, file_okay=True,
                                                           dir_okay=False),
              help="Path to APK to run")
@click.option("--build-path", type=click.Path(resolve_path=True, file_okay=False),
              help="Path to place decompiled files and exploit APK", default="build", show_default=True)
def decompile(apk, build_path):
    pass


def initialize_logging(level):
    """Creates two root handlers, one to file called `qark_debug.log` and one to stderr"""

    debug_handler = logging.FileHandler(DEBUG_LOG_PATH, mode="w")
    debug_handler.setLevel(logging.DEBUG)

    stderr_handler = logging.StreamHandler(stream=stderr)
    stderr_handler.setLevel(level)

    logging.getLogger().addHandler(debug_handler)
    logging.getLogger().addHandler(stderr_handler)
