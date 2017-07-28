import sys, os, re
import qarkMain

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub


class ManifestFilePlugin(IPlugin):

    PATH_USAGE = r'android:path='
    # Regex to check the launch mode of activity and task
    LAUNCH_MODE = r'android:launchMode=[\'\"]singleTask[\'\"]'
    TASK_REPARENTING = r'android:allowTaskReparenting=[\'\"]true[\'\"]'
    RECEIVER_REGEX = r'<receiver.*?>'
    PRIORITY_REGEX = r'priority'

    def __init__(self):
        self.name = 'Manifest File Checks'

    def UserCreatedReceivers(self):
        return re.findall(self.RECEIVER_REGEX, common.manifest)

    def target(self, queue):
        f = str(common.manifest)
        res = []
        count = 0
        ordered_broadcast = []
        path_variable_list =[]
        launch_mode_list =[]
        global fileName
        # full path to app manifest
        fileName = qarkMain.find_manifest_in_source()

        receivers = self.UserCreatedReceivers()
        for receiver in receivers:
            if "exported" and "true" in str(receiver):
                if not any(re.findall(self.PRIORITY_REGEX, str(receiver))):
                    ordered_broadcast.append(str(receiver))

        # Arrange exported broadcast receiver without priority set in column format
        list_orderedBR = " \n".join(ordered_broadcast)
        if ordered_broadcast:
            PluginUtil.reportWarning(fileName, self.OrderedBroadcastIssueDetails(list_orderedBR), res)

        for line in f.splitlines():
            count += 1
            # update progress bar
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(f.splitlines())))

            if any(re.findall(self.PATH_USAGE, line)):
                path_variable_list.append(line)

            if any(re.findall(self.LAUNCH_MODE, line)):
                launch_mode_list.append(line)

            if any(re.findall(self.TASK_REPARENTING, line)):
                PluginUtil.reportInfo(fileName, self.TaskReparentingIssue(fileName), res)

        # Arrange identified path variable and launch mode usage in column format
        path_variable = " \n".join(path_variable_list)
        launch_mode_variable = "\n".join(launch_mode_list)

        if path_variable_list:
            PluginUtil.reportWarning(fileName, self.PathUsageIssue(path_variable), res)

        if launch_mode_list:
            PluginUtil.reportInfo(fileName, self.LaunchModeIssue(launch_mode_variable), res)

        # Check for google safebrowsing API
        if "WebView" in f.splitlines():
            if "EnableSafeBrowsing" and "true" not in f.splitlines():
                PluginUtil.reportInfo(fileName, self.SafebrowsingIssueDetails(fileName), res)

        # send all results back to main thread
        queue.put(res)

    def OrderedBroadcastIssueDetails(self, list_orderedBR):
        return 'Data Injection due to exported Broadcast Receiver. ' \
               'Default priority of exported receiver is 0. Since, the higher priority receivers respond first' \
               ' and forward it to lower priority receivers, a malicious receiver with high priority can intercept the ' \
               'message change it and forward it to lower priority receivers.\n%s\n' \
               % list_orderedBR

    def SafebrowsingIssueDetails(self, fileName):
        return 'To provide users with a safer browsing experience, you can configure your apps' \
                'WebView objects to verify URLs using Google Safe Browsing. \n When this security measure is enabled,'\
                'your app shows users a warning when they attempt to navigate to a potentially unsafe website. \n %s\n'\
               % fileName

    def LaunchModeIssue(self, fileName):
        return 'android:launchMode="singleTask". ' \
               'This results in AMS either resuming the earlier activity' \
               ' or loads it in a task with same affinity or' \
               'the activity is started as a new task. This may result in Task Poisoning. \n' \
               'https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf \n%s \n ' \
               % fileName

    def TaskReparentingIssue(self, line):
        return 'android:allowTaskReparenting="true".\n' \
               'This allows an existing activity to be reparented to a new native task' \
               ' i.e task having the same affinity as the activity.\n' \
               'This may lead to UI spoofing attack on this application. \n' \
               'https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-ren-chuangang.pdf \n%s \n ' \
               % fileName

    def PathUsageIssue(self, line):
        return 'Be careful with the use of android:path in the <path-permission> tag\n' \
               'android:path means that the permission applies to the exact path declared in android:path. This expression does not protect the sub-directories\n%s \n ' \
               % line

    def getName(self):
        return "Manifest File Checks"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target