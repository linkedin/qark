from __future__ import absolute_import

import logging
import logging.config

import click
import os

from qark.apk_builder import APKBuilder
from qark.decompiler.decompiler import Decompiler
from qark.report import Report
from qark.scanner.scanner import Scanner

DEBUG_LOG_PATH = os.path.join(os.getcwd(),
                              "qark_debug.log")


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
              help="A directory containing Java code, or a Java file, to run static analysis. If passed,"
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
        level = "DEBUG"
    else:
        level = "INFO"

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
    click.secho("Finish writing report to {report_path}...".format(report_path=report_path))

    if exploit_apk:
        click.secho("Building exploit APK...")
        exploit_builder = APKBuilder(exploit_apk_path=build_path, issues=scanner.issues, apk_name=decompiler.apk_name,
                                     manifest_path=decompiler.manifest_path, sdk_path=sdk_path)
        exploit_builder.build()
        click.secho("Finish building exploit APK...")


def initialize_logging(level):
    """Creates two root handlers, one to file called `qark_debug.log` and one to stderr"""
    handlers = {
        "stderr_handler": {
            "level": level,
            "class": "logging.StreamHandler"
        }
    }
    loggers = ["stderr_handler"]

    if level == logging.DEBUG:
        handlers["debug_handler"] = {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": DEBUG_LOG_PATH,
            "mode": "w",
            "formatter": "standard"
        }
        loggers.append("debug_handler")

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            }
        },
        "handlers": handlers,
        "loggers": {
            "": {
                "handlers": handlers,
                "level": "DEBUG",
                "propagate": True
            }
        }
    })
