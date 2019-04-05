#!/usr/bin/env python

from __future__ import absolute_import

import logging
import logging.config
import os

import click

from qark.apk_builder import APKBuilder
from qark.decompiler.decompiler import Decompiler
from qark.report import Report
from qark.scanner.scanner import Scanner
from qark.utils import environ_path_variable_exists

DEBUG_LOG_PATH = os.path.join(os.getcwd(),
                              "qark_debug.log")

# Environment variable names for the SDK
ANDROID_SDK_HOME = "ANDROID_SDK_HOME"
ANDROID_HOME = "ANDROID_HOME"
ANDROID_SDK_ROOT = "ANDROID_SDK_ROOT"

logger = logging.getLogger(__name__)


@click.command()
@click.option("--sdk-path", type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help="Path to the downloaded SDK directory if already downloaded. "
                   "Only necessary if --exploit-apk is passed. If --exploit-apk is passed and this flag is not passed,"
                   "QARK will attempt to use the ANDROID_SDK_HOME, ANDROID_HOME, ANDROID_SDK_ROOT "
                   "environment variables (in that order) for a path.")
@click.option("--build-path", type=click.Path(resolve_path=True, file_okay=False),
              help="Path to place decompiled files and exploit APK.", default="build", show_default=True)
@click.option("--debug/--no-debug", default=False, help="Show debugging statements (helpful for issues).",
              show_default=True)
@click.option("--apk", "source", help="APK to decompile and run static analysis. If passed, "
                                      "the --java option is not used.",
              type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True))
@click.option("--java", "source", type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True),
              help="A directory containing Java code, or a Java file, to run static analysis. If passed,"
                   "the --apk option is not used.")
@click.option("--report-type", type=click.Choice(["html", "xml", "json", "csv"]),
              help="Type of report to generate along with terminal output.", default="html", show_default=True)
@click.option("--exploit-apk/--no-exploit-apk", default=False,
              help="Create an exploit APK targetting a few vulnerabilities.", show_default=True)
@click.option("--report-path", type=click.Path(resolve_path=True, file_okay=False), default=None,
              help="report output path.", show_default=True)
@click.option("--keep-report/--no-keep-report", default=False,
              help="Append to final report file.", show_default=True)
@click.version_option()
@click.pass_context
def cli(ctx, sdk_path, build_path, debug, source, report_type, exploit_apk, report_path, keep_report):
    if not source:
        click.secho("Please pass a source for scanning through either --java or --apk")
        click.secho(ctx.get_help())
        return

    if exploit_apk:

        if not sdk_path:
            # Try to set the SDK from environment variables if they exist
            # Follows the guidelines from https://developer.android.com/studio/command-line/variables
            if environ_path_variable_exists(ANDROID_SDK_HOME):
                sdk_path = os.environ[ANDROID_SDK_HOME]

            elif environ_path_variable_exists(ANDROID_HOME):
                sdk_path = os.environ[ANDROID_HOME]

            elif environ_path_variable_exists(ANDROID_SDK_ROOT):
                sdk_path = os.environ[ANDROID_SDK_ROOT]

            else:
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
    path_to_source = decompiler.path_to_source if decompiler.source_code else decompiler.build_directory

    scanner = Scanner(manifest_path=decompiler.manifest_path, path_to_source=path_to_source)
    scanner.run()
    click.secho("Finish scans...")

    click.secho("Writing report...")
    report = Report(issues=set(scanner.issues), report_path=report_path, keep_report=keep_report)
    report_path = report.generate(file_type=report_type)
    click.secho("Finish writing report to {report_path} ...".format(report_path=report_path))

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

    if level == "DEBUG":
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

    if level == "DEBUG":
        logger.debug("Debug logging enabled")
