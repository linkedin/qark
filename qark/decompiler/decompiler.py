import logging
import os
import platform
import re
import shlex
import shutil
import stat
import subprocess
import zipfile
from multiprocessing.pool import ThreadPool

import requests

from qark.decompiler.external_decompiler import DECOMPILERS, LIB_PATH
from qark.utils import create_directories_to_path, is_java_file

log = logging.getLogger(__name__)

OS = platform.system()
JAVA_VERSION_REGEX = '"(\d+\.\d+\..+)\"'
APK_TOOL_PATH = os.path.join(LIB_PATH, "apktool")

DEX2JAR_URL = "https://downloads.sourceforge.net/project/dex2jar/dex2jar-2.0.zip"
DEX2JAR_NAME = DEX2JAR_URL.replace("/download", "").split("/")[-1].rsplit(".zip")[0]
DEX2JAR_PATH = os.path.join(LIB_PATH, DEX2JAR_NAME)
DEX2JAR_EXTENSION = "sh" if OS != "Windows" else "bat"
DEX2JAR_EXECUTABLE = "d2j-dex2jar.{extension}".format(extension=DEX2JAR_EXTENSION)
DEX2JAR_INVOKE = "d2j_invoke.{extension}".format(extension=DEX2JAR_EXTENSION)

DECOMPILERS_PATH = os.path.join(LIB_PATH, "decompilers")

APK_TOOL_COMMAND = ("java -Djava.awt.headless=true -jar {apktool_path}/apktool.jar "
                    "d {path_to_source} --no-src --force -m --output {build_directory}")
DEX2JAR_COMMAND = "{dex2jar_path} {path_to_dex} -o {build_apk}.jar"


def escape_windows_path(path):
    if "\\" in path and OS == "Windows":
        try:
            path = path.encode('string-escape')
        except Exception:
            path = path.encode('unicode-escape')

    return path


class Decompiler(object):
    """This class handles unpacking and decompiling APKs into Java source code.

    New compilers can be added by adding the command to run the compiler to the `DECOMPILER_COMMANDS` dictionary and
    adding them into the `Decompiler.decompilers` dictionary with the path to the decompiler on the system.
    Each decompiler should have at most the following keys in their command string:
    {path_to_decompiler}, {jar}, {build_directory} -- Keys can be less than these but there can be no extra keys.
    """
    def __init__(self, path_to_source, build_directory=None):
        """
        :param path_to_source: Path to directory, APK, or a .java file
        :param build_directory: directory to unpack and decompile APK to.
                                If directory does not exist it will be created, defaults to same directory as APK/qark
        """
        if not os.path.exists(path_to_source):
            raise ValueError("Invalid path, path must be to an APK, directory, or a Java file")

        self.path_to_source = path_to_source
        self.build_directory = os.path.join(build_directory, "qark") if build_directory else os.path.join(os.path.dirname(os.path.abspath(path_to_source)), "qark")

        # validate we are running on an APK, Directory, or Java source code
        if os.path.isfile(self.path_to_source) and os.path.splitext(self.path_to_source.lower())[1] not in (".java",
                                                                                                            ".apk"):
            raise ValueError("Invalid path, path must be to an APK, directory, or a Java file")

        if os.path.isdir(path_to_source) or is_java_file(path_to_source):
            self.source_code = True
            self.manifest_path = None
            log.debug("Decompiler got directory to run on, assuming Java source code")
            return

        self.source_code = False
        self.apk_name = os.path.splitext(os.path.basename(path_to_source))[0]  # name of APK without the .apk extension

        self.dex_path = self._unpack_apk()
        self.jar_path = self._run_dex2jar()
        self.manifest_path = self.run_apktool()

        self.decompilers = DECOMPILERS
        for decompiler in self.decompilers:
            if decompiler.name == "procyon":
                log.debug("Downloading %s...", decompiler.name)
                download_procyon()
            elif decompiler.name == "cfr":
                log.debug("Downloading %s...", decompiler.name)
                download_cfr()

    def run(self):
        """Top-level function which runs each decompiler and waits for them to finish decompilation."""
        if self.source_code:
            return

        decompiler_pool = ThreadPool(len(self.decompilers))

        for decompiler in self.decompilers:
            if not os.path.isdir(os.path.join(self.build_directory, decompiler.name)):
                os.makedirs(os.path.join(self.build_directory, decompiler.name))
            log.debug("Starting decompilation with %s", decompiler.name)
            decompiler_pool.apply_async(self._decompiler_function, args=(decompiler,))

        decompiler_pool.close()
        decompiler_pool.join()

    def _decompiler_function(self, decompiler):
        """
        Abstract function that subprocesses a call to a decompiler and passes it the path of the decompiler supplied.
        If the `self.jar_path` is not set this will run `self._run_dex2jar` to set its value.

        :param decompiler: Decompiler that extends `ExternalDecompiler` base class
        """
        if not self.jar_path:
            log.debug(".jar file path not found, trying to create dex file.")
            self.jar_path = self._run_dex2jar()

        decompiler_command = escape_windows_path(
            decompiler.command.format(path_to_decompiler=decompiler.path_to_decompiler,
                                      jar=self.jar_path,
                                      build_directory=self.build_directory))

        try:
            retcode = subprocess.call(shlex.split(decompiler_command))
        except Exception:
            log.exception("%s failed to finish decompiling, continuing", decompiler.name)
        else:
            if retcode != 0:
                log.info("Error running %s", decompiler.name)
                log.debug("Decompiler failed with command %s", decompiler_command)

    def run_apktool(self):
        """
        Runs `APK_TOOL_COMMAND` with the users path to APK to decompile the APK.
        Sets `self.manifest_path` to its correct location.
        """
        # check that java is version 1.7 or higher
        java_version = get_java_version()

        try:
            if float(java_version[:3]) < 1.7:
                raise SystemExit("Java version of 1.7 or higher is required to run apktool")
        except TypeError:
            log.info("Java version %s not expected, continuing run", java_version)

        user_os = platform.system().lower()
        if user_os not in ("linux", "windows", "darwin"):
            raise SystemExit("OS %s is not supported, please use Linux, Windows, or Mac OSX", user_os)

        download_apktool()
        log.debug("APKTool downloaded")

        try:
            apktool_path = os.path.join(APK_TOOL_PATH, user_os)
        except Exception:
            log.exception("Failed to create path to apktool, is the directory structure correct?")
            raise SystemExit("Failed to create path to apktool")

        custom_apktool_command = escape_windows_path(APK_TOOL_COMMAND.format(apktool_path=apktool_path,
                                                                             path_to_source=self.path_to_source,
                                                                             build_directory=os.path.join(
                                                                                 self.build_directory, "apktool")))
        log.debug("Calling APKTool with following command")
        log.debug(custom_apktool_command)
        try:
            subprocess.call(shlex.split(custom_apktool_command))
        except Exception:
            log.exception("Failed to run APKTool with command: %s", custom_apktool_command)
            raise SystemExit("Failed to run APKTool")

        log.debug("APKTool finish executing, trying to move manifest into proper location")
        # copy valid XML file to correct location
        shutil.move(os.path.join(self.build_directory, "apktool", "AndroidManifest.xml"),
                    os.path.join(self.build_directory, "AndroidManifest.xml"))
        log.debug("Manifest moved successfully")

        log.debug("Removing apktool subdirectory of build")
        # remove the apktool generated files (only needed manifest file)
        shutil.rmtree(os.path.join(self.build_directory, "apktool"))
        log.debug("Removed apktool directory")

        return os.path.join(self.build_directory, "AndroidManifest.xml")

    def _unpack_apk(self):
        """
        Unpacks an APK and extracts its contents.
        :return: location for `self.dex_path` to use
        :rtype: os.path object
        """
        log.debug("Unpacking apk")
        unzip_file(self.path_to_source, destination_to_unzip=self.build_directory)

        return os.path.join(self.build_directory, "classes.dex")

    def _run_dex2jar(self):
        """Runs dex2jar in the lib on the dex file.
        If `self.dex_path` is None or empty it will run `_unpack_apk` to get a value for it."""
        # dex_path should always be set if being called through run
        if not self.dex_path:
            log.debug("Path to .dex file not found, unpacking APK")
            self.dex_path = self._unpack_apk()

        download_dex2jar()

        dex2jar_command = escape_windows_path(DEX2JAR_COMMAND.format(dex2jar_path=os.path.join(DEX2JAR_PATH,
                                                                                               "d2j-dex2jar.{extension}".format(
                                                                                                   extension=DEX2JAR_EXTENSION)),
                                                                     path_to_dex=self.dex_path,
                                                                     build_apk=os.path.join(self.build_directory,
                                                                                            self.apk_name)))

        log.debug("Running dex2jar with command %s", dex2jar_command)
        try:
            ret_code = subprocess.call(shlex.split(dex2jar_command))
            if ret_code != 0:
                log.critical("Error running dex2jar command: %s", dex2jar_command)
                raise SystemExit("Error running dex2jar")
        except Exception:
            log.exception("Error running dex2jar command: %s", dex2jar_command)
            raise SystemExit("Error running dex2jar command")

        return os.path.join(self.build_directory, "{apk_name}.jar".format(apk_name=self.apk_name))


def unzip_file(file_to_unzip, destination_to_unzip="unzip_apk"):
    """
    Extract all directories in the zip to the destination.

    :param str file_to_unzip:
    :param str destination_to_unzip:
    """
    if not os.path.isdir(destination_to_unzip):
        os.makedirs(destination_to_unzip)
    try:
        zipped_apk = zipfile.ZipFile(file_to_unzip, "r")
        zipped_apk.extractall(path=destination_to_unzip)
    except Exception:
        log.exception("Failed to extract zipped APK from %s to %s", file_to_unzip, destination_to_unzip)
        raise SystemExit("Failed to extract zipped APK")


def get_java_version():
    """
    Run `java -version` and return its output
    :return: String of the version like '1.7.0' or '1.6.0_36'
    :rtype: str
    :raise: Exception if `java -version` fails to run properly
    """
    log.debug("Getting java version")
    try:
        full_version = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT).decode('utf-8')
    except Exception:
        raise SystemExit("Error getting java version, is Java installed?")

    log.debug("Got full java version %s", full_version)
    # use regex to search for version like "1.6.0_38"
    version_regex = re.search(JAVA_VERSION_REGEX, full_version)

    try:
        return version_regex.group(1)
    except TypeError:
        raise SystemExit("Java version %s doesn't match regex search of %s", full_version, JAVA_VERSION_REGEX)


def download_apktool():
    """Attempts to download apktool to lib/apktool/{operating_system}/, on error raises `SystemExit`."""
    APK_TOOL_URL = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.3.1.jar"
    OS_TO_FILE_NAME = {"linux": "apktool", "windows": "apktool.bat", "darwin": "apktool"}
    OS_TO_WRAPPER = {"linux": "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool",
                     "darwin": "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/osx/apktool",
                     "windows": "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat"}

    user_os = platform.system().lower()
    if user_os not in OS_TO_FILE_NAME:
        raise SystemExit("OS %s is not supported, please use Linux, Windows, or Mac OSX", user_os)

    # create directory for operating system
    log.debug("Creating directory to store apktool files")
    apktool_path = os.path.join(APK_TOOL_PATH, user_os)

    if not os.path.exists(apktool_path):
        log.debug("Directory at %s does not exist, creating one", apktool_path)
        os.makedirs(apktool_path)

    else:
        log.debug("Directory already exists")
        if (os.path.isfile(os.path.join(apktool_path, OS_TO_FILE_NAME[user_os]))
                and os.path.isfile(os.path.join(apktool_path, "apktool.jar"))):
            # files for download already exist on file system, don't download them again
            log.debug("Files already exist, not downloading APKTool")
            return

    # download the APKTool wrapper for operating system specific
    log.debug("Starting download for APKTool wrapper")
    try:
        download_file(url=OS_TO_WRAPPER[user_os], download_path=os.path.join(apktool_path, OS_TO_FILE_NAME[user_os]))
    except Exception:
        log.exception("Failed to download APKTool wrapper")
        raise SystemExit("Failed to download APKTool wrapper")

    # download the APKTool jar
    log.debug("Starting download for APKTool jar")
    try:
        download_file(url=APK_TOOL_URL, download_path=os.path.join(apktool_path, "apktool.jar"))
    except Exception:
        raise SystemExit("Failed to download APKTool")

    # make downloaded files executable
    log.debug("Attempting to make downloaded files executable")
    for downloaded_file_path in (os.path.join(apktool_path, "apktool.jar"),
                                 os.path.join(apktool_path, OS_TO_FILE_NAME[user_os])):
        try:
            make_executable(downloaded_file_path)
        except Exception:
            log.exception("Failed to make downloaded APKTool files executable, continuing")


def download_file(url, download_path):
    """
    Helper that sends a GET to the URL and then writes its contents in the download path

    :param url:
    :param download_path: file system path to place contents of url
    """
    try:
        response = requests.get(url)
    except Exception:
        log.exception("Unable to download file from %s to %s", url, download_path)
        raise

    create_directories_to_path(download_path)

    # ensure output directory exists
    try:
        os.makedirs(os.path.dirname(download_path))
    except Exception:
        # Directory already exists, continue
        log.debug("Directory %s already exists for file download %s", download_path, url)

    with open(download_path, "wb") as download_path_file:
        download_path_file.write(response.content)


def make_executable(file_path):
    """
    Make the file at `file_path` executable.

    :param file_path: path to file to make executable
    """
    file_path = escape_windows_path(file_path)

    try:
        st = os.stat(file_path)
        os.chmod(file_path, st.st_mode | stat.S_IEXEC)
    except Exception:
        log.exception("Failed to make downloaded APKTool files executable, continuing")
        raise


def download_cfr():
    CFR_URL = "http://www.benf.org/other/cfr/cfr_0_124.jar"
    file_name = CFR_URL.split("/")[-1]
    if os.path.isfile(os.path.join(DECOMPILERS_PATH, file_name)):
        return

    try:
        download_file(CFR_URL, os.path.join(DECOMPILERS_PATH, file_name))
    except Exception:
        raise SystemExit("Failed to download CFR jar")


def download_procyon():
    PROCYON_URL = "https://bitbucket.org/mstrobel/procyon/downloads/procyon-decompiler-0.5.30.jar"
    file_name = PROCYON_URL.split("/")[-1]
    if os.path.isfile(os.path.join(DECOMPILERS_PATH, file_name)):
        return

    try:
        download_file(PROCYON_URL, os.path.join(DECOMPILERS_PATH, file_name))
    except Exception:
        raise SystemExit("Failed to download Procyon jar")


def download_dex2jar():
    if os.path.isfile(os.path.join(DEX2JAR_PATH, DEX2JAR_EXECUTABLE)):
        return

    try:
        download_file(DEX2JAR_URL, os.path.join(LIB_PATH, "temp_dex2jar.zip"))
    except Exception:
        log.exception("Failed to download dex2jar jar")
        raise SystemExit("Failed to download dex2jar jar")

    unzip_file(os.path.join(LIB_PATH, "temp_dex2jar.zip"), destination_to_unzip=LIB_PATH)
    os.remove(os.path.join(LIB_PATH, "temp_dex2jar.zip"))
    make_executable(os.path.join(DEX2JAR_PATH, DEX2JAR_EXECUTABLE))
    make_executable(os.path.join(DEX2JAR_PATH, DEX2JAR_INVOKE))
