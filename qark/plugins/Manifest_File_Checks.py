from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import sys
import os
import re
import qarkMain

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')


def ordered_broadcast(list_orderedBR):
    STRING = ("Data Injection due to exported Broadcast Receiver.\n"
              "Default priority of exported receiver is 0. Since, the higher priority receivers respond first"
              " and forward it to lower priority receivers, a malicious receiver with high priority can intercept the "
              "message change it and forward it to lower priority receivers.\n{}\n")
    return STRING.format(list_orderedBR)


def google_safe_browsing(fileName):
    STRING = ("To provide users with a safer browsing experience, you can configure your apps"
              "WebView objects to verify URLs using Google Safe Browsing.\nWhen this security measure is enabled,"
              " your app shows users a warning when they attempt to navigate to a potentially unsafe website.\n{}\n")
    return STRING.format(fileName)


def task_launch_mode(line):
    STRING = ("Use of android:launchMode=singleTask is found\n"
              "This results in AMS either resuming the earlier activity or loads it in a task with same affinity or"
              " the activity is started as a new task. This may result in Task Poisoning.\n"
              "https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf\n{}\n")
    return STRING.format(line)


def task_reparenting(line):
    STRING = ("Use of android:allowTaskReparenting='true' is found\n"
              "This allows an existing activity to be reparented to a new native task"
              " i.e task having the same affinity as the activity.\n"
              "This may lead to UI spoofing attack on this application.\n"
              "https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf\n{}\n")
    return STRING.format(line)


def path_usage(line):
    STRING = ("Be careful with the use of android:path in the <path-permission> tag\n"
              "android:path means that the permission applies to the exact path declared"
              " in android:path. This expression does not protect the sub-directories\n{}\n")
    return STRING.format(line)


def hardcoded_api_key(api_key_variable):
    STRING = "API Key Found\n{}"
    return STRING.format(api_key_variable)


class ManifestFilePlugin(IPlugin):
    PATH_USAGE = r'android:path='
    # Regex to check the launch mode of activity and task
    LAUNCH_MODE = r'android:launchMode=[\'\"]singleTask[\'\"]'
    TASK_REPARENTING = r'android:allowTaskReparenting=[\'\"]true[\'\"]'
    RECEIVER_REGEX = r'<receiver.*?>'
    PRIORITY_REGEX = r'priority'
    HARDCODED_API_KEY = r'API_KEY|api_key|API|api|key'
    # Regex to check for API Keys containing atleast one uppercase, lowercase chracters and number
    API_KEY_REGEX = r'^.+(?=.{20,})(?=.+\d)(?=.+[a-z])(?=.+[A-Z]).+$'
    # Regex which is used to ignore few special characters in api keys to prevent false positives
    SPECIAL_CHAR_REGEX = r'^.+(?=.+[!$%^~]).+$'

    def __init__(self):
        self.name = 'Manifest File Checks'

    def UserCreatedReceivers(self):
        return re.findall(self.RECEIVER_REGEX, common.manifest)

    def target(self, queue):
        raw_file = str(common.manifest)
        count = 0
        ordered_broadcast, path_variable_list, launch_mode_list, api_key_list, res = ([] for _ in xrange(5))
        global file_name
        # full path to app manifest
        file_name = qarkMain.find_manifest_in_source()

        receivers = self.UserCreatedReceivers()
        for receiver in receivers:
            if "exported" and "true" in str(receiver):
                if not any(re.findall(self.PRIORITY_REGEX, str(receiver))):
                    ordered_broadcast.append(str(receiver))

        # Arrange exported broadcast receiver without priority set in column format
        list_orderedBR = " \n".join(ordered_broadcast)
        if ordered_broadcast:
            PluginUtil.reportWarning(file_name, ordered_broadcast(list_orderedBR), res)

        for line in raw_file.splitlines():
            count += 1
            # update progress bar
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(raw_file.splitlines())))

            if any(re.findall(self.PATH_USAGE, line)):
                path_variable_list.append(line)

            if any(re.findall(self.LAUNCH_MODE, line)):
                launch_mode_list.append(line)

            if any(re.findall(self.TASK_REPARENTING, line)):
                PluginUtil.reportInfo(file_name, task_reparenting(file_name), res)

            if re.match(self.API_KEY_REGEX, line):
                # Check if special character is present in the line. If "Yes, then ignore.
                if re.match(self.SPECIAL_CHAR_REGEX, line):
                    pass
                else:
                    if line not in api_key_list:
                        api_key_list.append(line)

            # Additional check for hardcoded api keys which matches the syntax most commonly used with google API_KEY
            if any(re.findall(self.HARDCODED_API_KEY, line)):
                if line not in api_key_list:
                    api_key_list.append(line)

        # Arrange identified path variable and launch mode usage in column format
        path_variable = " \n".join(path_variable_list)
        launch_mode_variable = "\n".join(launch_mode_list)
        api_key_variable = "\n".join(api_key_list)

        if path_variable_list:
            PluginUtil.reportWarning(file_name, path_usage(path_variable), res)

        if launch_mode_list:
            PluginUtil.reportInfo(file_name, task_launch_mode(launch_mode_variable), res)

        if api_key_list:
            PluginUtil.reportInfo(file_name, hardcoded_api_key(api_key_variable), res)

        # Check for google safe browsing API
        if "WebView" in raw_file.splitlines():
            if "EnableSafeBrowsing" and "true" not in raw_file.splitlines():
                PluginUtil.reportInfo(file_name, google_safe_browsing(file_name), res)

        # send all results back to main thread
        queue.put(res)

    @staticmethod
    def getName():
        return "Manifest File Checks"

    @staticmethod
    def getCategory():
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
