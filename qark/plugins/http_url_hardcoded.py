import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')
from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj


class HardcodedHTTPUrl(IPlugin):

    http_url_regex = r'http://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def __init__(self):
        self.name = 'Hardcoded HTTP url'

    def target(self, queue):
        files = common.java_files
        global parser
        parser = plyj.Parser()
        global tree
        global fileName
        tree = ''
        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            fileName = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception:
                continue

            try:
                global url
                url = []
                for import_decl in tree.import_declarations:
                    if 'HttpURLConnection' in import_decl.name.value or 'URL' in import_decl.name.value:
                        textfile = str(open(fileName, 'r').read())
                        search = "http://"
                        http_result = re.findall('\\b'+search+'\\b', textfile)
                        if http_result:
                            url = re.findall(self.http_url_regex, textfile)
                            http_url_list = " \n".join(url)
                            PluginUtil.reportInfo(fileName, self.HardcodedHTTPUrlsIssueDetails((fileName, http_url_list)), res)
                            break
                        else:
                            continue
            except Exception:
                continue
        queue.put(res)

    def HardcodedHTTPUrlsIssueDetails(self, (fileName, http_url_list)):
        return 'Application contains hardcoded http url \n%s. \n%s \n' \
               'Ignore if HSTS is implemented \n' \
                % (fileName, http_url_list)

    def getName(self):
        return "Hardcoded HTTP url"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target