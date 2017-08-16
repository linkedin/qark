from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

STRING = "API Key Found\n{}"


def hardcoded_api_key(api_key_variable):
    return STRING.format(api_key_variable)


class HardcodedAPIIssuesPlugin(IPlugin):
    # Regex to check for API Keys containing atleast one uppercase, lowercase chracters and number
    API_KEY_REGEX = r'^.+(?=.{20,})(?=.+\d)(?=.+[a-z])(?=.+[A-Z])(?=.+[-_]).+$'
    # Regex which is used to ignore few special characters in api keys
    # Except - " ' ; to prevent false positives
    SPECIAL_CHAR_REGEX = r'^.+(?=.+[!$%^&*()_+|~=`{}\[\]:<>?,.\/]).+$'

    def __init__(self):
        self.name = 'Hardcoded API Keys'

    def target(self, queue):
        files = common.java_files
        global file_path
        api_key_list = []
        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            file_path = str(f)
            with open(file_path, 'r') as fi:
                file_content = fi.read()
            # Split the file content in each individual line
            for line in file_content.splitlines():
                # Further split each line into words
                for word in line.split():
                    # Regex to check API value in work
                    if re.match(self.API_KEY_REGEX, word):
                        # Check if special character is present in the line. If "Yes, then ignore.
                        if not re.match(self.SPECIAL_CHAR_REGEX, word):
                            if file_path not in api_key_list and line not in api_key_list:
                                api_key_list.append("Line: " + line)
                                api_key_list.append("Filepath: " + file_path + "\n")

        api_key_variable = "\n".join(api_key_list)

        if api_key_list:
            PluginUtil.reportInfo(file_path, hardcoded_api_key(api_key_variable), res)

        queue.put(res)

    @staticmethod
    def getName():
        return "Hardcoded API Keys"

    @staticmethod
    def getCategory():
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
