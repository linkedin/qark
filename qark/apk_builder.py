from __future__ import absolute_import

import logging
import os
import re
import shlex
import shutil
import subprocess
from qark.manifest_helpers import get_package_from_manifest
from qark.xml_helpers import write_key_value_to_xml

try:
    import ConfigParser as configparser
    from StringIO import StringIO
except ModuleNotFoundError:
    import configparser
    from io import StringIO

from qark.plugins.helpers import copy_directory_to_location
from qark.plugins.manifest.exported_tags import EXPORTED_TAGS_ISSUE_NAME

log = logging.getLogger(__name__)


COMPONENT_ENTRIES = {"activity": ("onCreate", "onStart"),
                     "activity-alias": ("onCreate", "onStart"),
                     "receiver": ("onReceive",),
                     "service": ("onCreate", "onBind", "onStartCommand", "onHandleIntent"),
                     "provider": ("onReceive",)
                     }
INTENT_EXTRAS_STRINGS = (r'getExtras\(\s*[0-9A-Za-z_\"\'.]+',
                         r'getStringExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getIntExtra\s*[0-9A-Za-z_\"\'.]+'
                         r'getIntArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getFloatExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getFloatArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getDoubleExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getDoubleArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getCharExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getCharArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getByteExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getByteArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getBundleExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getBooleanExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getBooleanArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getCharSequenceArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getCharSequenceArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getCharSequenceExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getInterArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getLongArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getLongExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getParcelableArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getParcelableArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getParcelableExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getSeriablizableExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getShortArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getShortExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getStringArrayExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         r'getStringArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+'
                         # These are not necessarily Intent extras, but may contain them
                         r'getString\(\s*[0-9A-Za-z_\"\'.]+'
                         )
INTENT_REGEX = re.compile("({extra_regex})".format(extra_regex="|".join(INTENT_EXTRAS_STRINGS)))

EXPLOIT_APK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exploit_apk")


class APKBuilder(object):
    __instance = None

    def __new__(cls, exploit_apk_path, issues, apk_name, manifest_path, sdk_path):
        if APKBuilder.__instance is None:
            APKBuilder.__instance = object.__new__(cls)

        return APKBuilder.__instance

    def __init__(self, exploit_apk_path, issues, apk_name, manifest_path, sdk_path):
        """
        Creates the APKBuilder.

        :param str exploit_apk_path: path to where the exploit apk should be built
        :param list issues: List of `Issue` found from the scanner
        :param str apk_name: name of the examined APK
        """
        self.exploit_apk_path = os.path.join(exploit_apk_path, "exploit_{apk_name}".format(apk_name=apk_name))

        # need to remove directory if it exists otherwise shutil.copytree will error from helper
        if os.path.isdir(self.exploit_apk_path):
            shutil.rmtree(self.exploit_apk_path)

        # copy template exploit APK to exploit location
        try:
            copy_directory_to_location(directory_to_copy=EXPLOIT_APK_PATH, destination=self.exploit_apk_path)
        except Exception:
            log.exception("Failed to copy %s to %s", EXPLOIT_APK_PATH, self.exploit_apk_path)
            raise SystemExit("Failed to copy %s to %s", EXPLOIT_APK_PATH, self.exploit_apk_path)

        values_path = os.path.join(self.exploit_apk_path, "app", "src", "main", "res", "values")
        self.strings_xml_path = os.path.join(values_path, "strings.xml")
        self.extra_keys_xml_path = os.path.join(values_path, "extraKeys.xml")
        self.intent_ids_xml_path = os.path.join(values_path, "intentID.xml")

        self.properties_file_path = os.path.join(self.exploit_apk_path, "local.properties")
        self.sdk_path = sdk_path

        self.issues = issues
        try:
            self.package_name = get_package_from_manifest(manifest_path)
        except IOError:
            log.exception("Failed to read manifest file at %s", manifest_path)
            raise SystemExit("Failed to read manifest file at %s", manifest_path)

        self.exported_activities = self._get_exported_tags(tag_type="activity")
        self.exported_services = self._get_exported_tags(tag_type="service")

    def _get_intent_extras(self):
        for exported_activity in self.exported_activities:
            pass


    def _get_exported_tags(self, tag_type="activity"):
        """
        Iterate over issues looking for exported tags of type `tag_type`. Return a set of found issues.

        :param tag_type: `tag_type` in ("activity", "activity-alias", "service", "receiver", "provider")
        :return: set of `Issue` of every issue found with `tag_type`
        :rtype: set
        """
        exported_tag_issues = (issue for issue in self.issues if issue.name == EXPORTED_TAGS_ISSUE_NAME)
        found_exported_tag_issues = set()

        for exported_tag_issue in exported_tag_issues:
            # find all tags of `tag_type`
            if re.search("\s{tag}\stags\s".format(tag=tag_type), exported_tag_issue.description):
                found_exported_tag_issues.add(exported_tag_issue)

        return found_exported_tag_issues

    def _write_intent_to_strings_xml(self, intent_name, value):
        """
        Checks if `intent_name` exists in the parsed XML `self.string_xml_path`, if it does not it creates a new
        element and appends it to the XML tree and then updates the file.

        :param intent_name:
        :param value:
        :return:
        """
        try:
            strings_xml = ElementTree.parse(self.strings_xml_path)
        except IOError:
            log.exception("Strings file for exploit APK does not exist")
            raise SystemExit("Strings file for exploit APK does not exist")

        if not strings_xml.find(intent_name):
            new_element = ElementTree.SubElement(strings_xml.getroot(), "string", attrib={"name": intent_name})
            new_element.text = value

            strings_xml.write(self.strings_xml_path)

    def _write_intent_id_to_xml(self, intent_id):
        """
        Checks if `intent_name` exists in the parsed XML `self.string_xml_path`, if it does not it creates a new
        element and appends it to the XML tree and then updates the file.

        :param intent_name:
        :param value:
        :return:
        """
        try:
            strings_xml = ElementTree.parse(self.intent_ids_xml_path)
        except IOError:
            log.exception("Strings file for exploit APK does not exist")
            raise SystemExit("Strings file for exploit APK does not exist")
        """
        if not strings_xml.findall("string-array"):
            new_element = ElementTree.SubElement(strings_xml.getroot(), "string", attrib={"name": intent_name})
            new_element.text = value

            strings_xml.write(self.strings_xml_path)
        """

    def _write_intent_to_extra_keys_xml(self, intent_name, key):
        """
        Checks if `intent_name` is name of a `string-array`, if it does not exist it creates a new
        element and appends it to the XML tree and then updates the file, if it exists it updates the existing element.

        :param intent_name:
        :param value:
        """
        try:
            strings_xml = ElementTree.parse(self.extra_keys_xml_path)
        except IOError:
            log.exception("Extra keys file for exploit APK does not exist")
            raise SystemExit("Extra keys file for exploit APK does not exist")

        # attempt to update the intent if it exists
        for string_array in strings_xml.findall("string-array"):
            if string_array.attrib.get("name") == intent_name:
                sub_element_item = ElementTree.SubElement(string_array, "item")
                sub_element_item.text = key

                strings_xml.write(self.strings_xml_path)
                return

        # write the intent as it does not exist
        new_string_array = ElementTree.SubElement(strings_xml.getroot(), "string-array", attrib={"name": intent_name})
        sub_element_item = ElementTree.SubElement(new_string_array, "item")
        sub_element_item.text = key

        strings_xml.write(self.strings_xml_path)

    def _build_apk(self):
        current_directory = os.getcwd()
        try:
            os.chdir(self.exploit_apk_path)
            write_key_value_to_xml('packageName', self.package_name, self.strings_xml_path)
            self._write_properties_file({"sdk.dir": self.sdk_path})
            command = "./gradlew assembleDebug"
            try:
                subprocess.call(shlex.split(command))
            except Exception:
                log.exception("Error running command %s")
                raise  # raise here as we can still make the report for the user
        except Exception:
            raise
        finally:
            os.chdir(current_directory)

    def _write_properties_file(self, dict_to_write, append=True):
        """
        Write each key and value into the properties file, dictionary should be simple as complex types won't
        be able to be written to properties file.

        :param dict dict_to_write: Dictionary of key=value pairs to write to properties file
        :param append: if the properties file should be appended to or not (if False, write over the file)
        """
        mode = "a" if append else "w"
        with open(self.properties_file_path, mode) as properties_file:
            for key, value in dict_to_write.items():
                properties_file.write("{key}={value}".format(key=key, value=value))

    def _read_properties_file(self):
        """
        Reads the local.properties file. Converts the file from .properties to a .ini by adding
        a dummy header, the header

        :return: dictionary of values in key, value pairs
        :rtype: dict
        """
        with open(self.properties_file_path, "r") as properties_file:
            config = StringIO()
            config.write('[dummy_header]\n')

            # escape percentages found in properties file (ini file they are special characters)
            config.write(properties_file.read().replace('%', '%%'))
            config.seek(0, os.SEEK_SET)

            cp = configparser.SafeConfigParser()
            cp.readfp(config)

            return dict(cp.items('dummy_section'))
