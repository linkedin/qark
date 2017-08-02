import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub


class PhoneIdentifierPlugin(IPlugin):
    # regex to determine if file contains usage of TelephonyManager
    telephonyManagerRegex = r'android\.telephony\.TelephonyManager'

    # regex to extract TelephonyManager variable names in group 2
    varNameRegex = r'(android\.telephony\.)?TelephonyManager\s(\w*?)([,);]|(\s=))'

    # regex to match inline calls
    inlineRegex = r'\({2,}(android.telephony.)?TelephonyManager\)\w*?\.getSystemService\([\'\"]phone[\'\"]\){2,}\.' \
                  r'(getLine1Number|getDeviceId)'

    def target(self, queue):
        # get all decompiled files that contains usage of TelephonyManager
        files = common.text_scan(common.java_files, self.telephonyManagerRegex)

        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.getName(), percent=round(count * 100 / len(files)))

            # get decompiled file body
            fileName = f[1]
            with open(fileName, 'r') as fi:
                fileBody = fi.read()

            # report if file contains inline call
            if PluginUtil.contains(self.inlineRegex, fileBody):
                PluginUtil.reportInfo(fileName, self.PhoneIdentifierIssueDetails(fileName), res)
                break

            # report if any TelephonyManager variables invokes calls to get phone identifiers
            for varName in PluginUtil.returnGroupMatches(self.varNameRegex, 2, fileBody):
                if PluginUtil.contains(r'%s\.(getLine1Number|getDeviceId)\(.*?\)' % varName, fileBody):
                    PluginUtil.reportInfo(fileName, self.PhoneIdentifierIssueDetails(fileName), res)
                    break

        queue.put(res)

    def PhoneIdentifierIssueDetails(self, fileName):
        return 'Access of phone number or IMEI, is detected in file: %s.\n' \
               'Avoid storing or transmitting this data.' \
               % fileName

    def getName(self):
        # The name to be displayed against the progressbar
        return "Phone identifier access"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target

