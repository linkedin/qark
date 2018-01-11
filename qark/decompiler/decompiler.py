import logging
from multiprocessing import Pool
import os
import platform
import shlex
import shutil
import subprocess
import re
import zipfile

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

JAVA_VERSION_REGEX = '"(\d+\.\d+\..+)\"'
LIB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../lib")
APK_TOOL_PATH = os.path.join(LIB_PATH, "apktool")
DEX2JAR_PATH = os.path.join(LIB_PATH, "dex2jar-2.0")
DECOMPILERS_PATH = os.path.join(LIB_PATH, "decompilers")

APK_TOOL_COMMAND = ("java -Djava.awt.headless=true -jar {apktool_path}/apktool.jar "
                    "d {path_to_apk} --no-src --force -m --output {build_directory}")
DEX2JAR_COMMAND = "{dex2jar_path}/d2j-dex2jar.sh {path_to_dex} -o {build_directory}/{apk_name}.jar"
DECOMPILER_COMMANDS = {"JDCORE": "java -jar {path_to_decompiler} {jar} {build_directory}/jdcore",
                       "PROCYON": "java -jar {path_to_decompiler} {jar} -o {build_directory}/procyon",
                       "CFR": "java -jar {path_to_decompiler} {jar} --outputdir {build_directory}/cfr"}


class Decompiler(object):
    """This class handles unpacking and decompiling APKs into Java source code.

    New compilers can be added by adding the command to run the compiler to the `DECOMPILER_COMMANDS` dictionary and
    adding them into the `Decompiler.decompilers` dictionary with the path to the decompiler on the system.
    Each decompiler should have at most the following keys in their command string:
    {path_to_decompiler}, {jar}, {build_directory} -- Keys can be less than these but there can be no extra keys.
    """
    def __init__(self, path_to_apk, build_directory=None):
        """
        :param path_to_apk: path to APK to decompile
        :param build_directory: directory to unpack and decompile APK to.
                                If directory does not exist it will be created, defaults to same directory as APK
        """
        self.path_to_apk = path_to_apk
        self.build_directory = build_directory if build_directory else os.path.dirname(path_to_apk)
        self.apk_name = os.path.splitext(os.path.basename(path_to_apk))[0]  # name of APK without the .apk extension

        self.manifest_path = None
        self.dex_path = None
        self.jar_path = None

        self.decompilers = {"PROCYON": os.path.join(DECOMPILERS_PATH, "procyon-decompiler-0.5.30.jar"),
                            "CFR": os.path.join(DECOMPILERS_PATH, "cfr_0_124.jar"),
                            "JDCORE": os.path.join(DECOMPILERS_PATH, "jd-core-java-1.2.jar"), }

    def decompile(self):
        """Top-level function which runs each decompiler and waits for them to finish decompilation."""
        decompiler_pool = Pool(len(self.decompilers))

        for decompiler, path in self.decompilers.items():
            os.makedirs(os.path.join(self.build_directory, decompiler.lower()))
            decompiler_pool.apply_async(self._decompiler_function, args=(decompiler, path))

        decompiler_pool.close()
        decompiler_pool.join()

    def _decompiler_function(self, decompiler, path_to_decompiler):
        """
        Abstract function that subprocesses a call to a decompiler and passes it the path of the decompiler supplied.
        If the `self.jar_path` is not set this will run `self._run_dex2jar` to set its value.

        :param decompiler: name of the decompiler in all caps
        :param path_to_decompiler: path to the decompiler, usually taken from the `Decompiler.decompilers` dictionary
        """
        if not self.jar_path:
            log.debug(".jar file path not found, trying to create dex file.")
            self.jar_path = self._run_dex2jar()

        try:
            # devnull = open(os.devnull, 'wb')
            retcode = subprocess.call(
                shlex.split(DECOMPILER_COMMANDS.get(decompiler.upper()).format(path_to_decompiler=path_to_decompiler,
                                                                       jar=self.jar_path,
                                                                       build_directory=self.build_directory)),
                )
        except Exception:
            log.exception("%s failed to finish decompiling, continuing", decompiler)
        else:
            if retcode != 0:
                log.info("Error running %s, continuing", decompiler)
        # finally:
        #     devnull.close()

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

        try:
            apktool_path = os.path.join(APK_TOOL_PATH, user_os)
        except Exception:
            log.exception("Failed to create path to apktool, is the directory structure correct?")
            raise SystemExit("Failed to create path to apktool")

        custom_apktool_command = APK_TOOL_COMMAND.format(apktool_path=apktool_path,
                                                         path_to_apk=self.path_to_apk,
                                                         build_directory=self.build_directory)
        try:
            subprocess.call(shlex.split(custom_apktool_command))
        except Exception:
            log.exception("Failed to run APKTool with command: %s", custom_apktool_command)
            raise SystemExit("Failed to run APKTool")

        return os.path.join(self.build_directory, "AndroidManifest.xml")

    def _unpack_apk(self):
        """
        Unpacks an APK by making it a .zip file and then extracting its contents.
        Sets `self.dex_path` to its correct location.
        """
        try:
            temp_apk_zip = copy_apk_to_zip(self.path_to_apk)
        except Exception:
            raise SystemExit("Unable to copy APK to a ZIP")

        log.debug("Unzipping APK from %s to %s", self.path_to_apk, temp_apk_zip)

        try:
            unzip_file(temp_apk_zip, destination_to_unzip=self.build_directory)
        except Exception:
            raise SystemExit("Unable to unzip APK")
        finally:
            # clean up copied file
            log.debug("Removing created file at %s", temp_apk_zip)
            try:
                os.remove(temp_apk_zip)
            except OSError:
                log.exception("Failed to remove created file at %s. File should be deleted manually", temp_apk_zip)

        return os.path.join(self.build_directory, "classes.dex")

    def _run_dex2jar(self):
        """Runs dex2jar.sh in the lib on the dex file.
        If `self.dex_path` is None or empty it will run `_unpack_apk` to get a value for it."""
        # dex_path should always be set if being called through decompile
        if not self.dex_path:
            log.debug("Path to .dex file not found, unpacking APK")
            self.dex_path = self._unpack_apk()

        dex2jar_command = DEX2JAR_COMMAND.format(dex2jar_path=DEX2JAR_PATH, path_to_dex=self.dex_path,
                                                 build_directory=self.build_directory, apk_name=self.apk_name)
        try:
            ret_code = subprocess.call(shlex.split(dex2jar_command))
            if ret_code != 0:
                log.critical("Error running dex2jar command: %s", dex2jar_command)
                raise SystemExit("Error running dex2jar")
        except Exception:
            log.exception("Error running dex2jar command: %s", dex2jar_command)
            raise SystemExit("Error running dex2jar command")

        return os.path.join(self.build_directory, "{apk_name}.jar".format(apk_name=self.apk_name))

    '''
    def _run_jdcore(self):
        """Runs JDCore on the JAR in the `self.jar_path` (should be created during _run_dex2jar).
        If `self.jar_path` is None or empty, then it will run dex2jar to get a proper value for it."""
        if not self.jar_path:
            log.debug(".jar file path not found, trying to create dex file.")
            self.jar_path = self._run_dex2jar()
        os.makedirs(os.path.join(self.build_directory, "jdcore"))
        retcode = subprocess.call(shlex.split(JDCORE_COMMAND.format(path_to_jdcore=os.path.join(DECOMPILERS_PATH,
                                                                                                "jd-core-java-1.2.jar"),
                                                                    jar=self.jar_path,
                                                                    build_directory=self.build_directory)))

        if retcode != 0:
            log.info("Error running JDCore, continuing")

    def _run_procyon(self):
        if not self.jar_path:
            log.debug(".jar file path not found, trying to create dex file.")
            self.jar_path = self._run_dex2jar()
        os.makedirs(os.path.join(self.build_directory, "procyon"))
        retcode = subprocess.call(shlex.split(PROCYON_COMMAND.format(path_to_procyon=os.path.join(DECOMPILERS_PATH,
                                                                                                  "procyon-decompiler-0.5.30.jar"),
                                                                     jar=self.jar_path,
                                                                     build_directory=self.build_directory)))

        if retcode != 0:
            log.info("Error running procyon, continuing")

    def _run_cfr(self):
        if not self.jar_path:
            log.debug(".jar file path not found, trying to create dex file.")
            self.jar_path = self._run_dex2jar()
        os.makedirs(os.path.join(self.build_directory, "cfr"))
        retcode = subprocess.call(shlex.split(CFR_COMMAND.format(path_to_cfr=os.path.join(DECOMPILERS_PATH, "cfr_0_124.jar"),
                                                                 jar=self.jar_path,
                                                                 build_directory=self.build_directory)))

        if retcode != 0:
            log.info("Error running cfr, continuing")
    '''





def copy_apk_to_zip(path_to_apk):
    """
    Copies a .apk file to a .apk.zip file so that it can be unzipped later.

    :param str path_to_apk: Path to the APK file
    :return: path to the new .apk.zip
    :rtype: str
    :raise: Exception if cannot create a copy of the APK file
    """
    temp_apk_zip = path_to_apk + ".zip"
    log.debug("Copying %s to %s", path_to_apk, temp_apk_zip)
    try:
        shutil.copyfile(path_to_apk, temp_apk_zip)
    except Exception:
        log.exception("Unable to copy APK to zip file")
        raise SystemExit("Unable to copy APK to zip file")

    return temp_apk_zip


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
    try:
        full_version = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT).decode('utf-8')
    except Exception:
        raise SystemExit("Error getting java version, is Java installed?")

    # use regex to search for version like "1.6.0_38"
    version_regex = re.search(JAVA_VERSION_REGEX, full_version)

    try:
        return version_regex.group(1)
    except TypeError:
        raise SystemExit("Java version %s doesn't match regex search of %s", full_version, JAVA_VERSION_REGEX)


