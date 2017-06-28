import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')
from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj

class HarcodedHTTPUrl(IPlugin):

    def target(self, queue):
        # get all decompiled files that contains usage of WebView
        files = common.java_files
        parser = plyj.Parser()
        global parser
        global tree
        global fileName
        tree = ''
        res = []
        results = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.getName(), percent=round(count * 100 / len(files)))
            fileName = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception as e:
                continue

            try:
                global url
                url = []
                for import_decl in tree.import_declarations:
                    if 'HttpURLConnection' in import_decl.name.value or 'URL' in import_decl.name.value:
                        textfile = open(fileName, 'r').read()
                        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', textfile)
                        url_string = " \n".join(url)
                        PluginUtil.reportIssue(fileName, self.createIssueDetails((fileName, url_string)), res)
                        break
            except Exception as e:
                continue
        queue.put(res)

    def createIssueDetails(self, (fileName, url_string)):
        return 'Application contains hardcoded http url %s. \n %s \n' \
               'Does not matter if HSTS is implemented \n' \
                % (fileName, url_string)

    def getName(self):
        # The name to be displayed against the progressbar
        return "Hardcoded HTTP url"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target