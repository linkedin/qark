import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')
from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj


class DynamicallyLoadingCodePlugin(IPlugin):
    DEX_CLASS_LOADER = r'DexClassLoader'
    CLASS_LOADER = r'loadClass'
    DYNAMIC_BROADCAST_RECEIVER = r'registerReceiver'

    def __init__(self):
        self.name = 'Dynamically loading code'

    def target(self, queue):
        files = common.java_files
        global parser, tree, fileName
        parser = plyj.Parser()
        tree = ''
        res = []

        #List of Broadcast Receiver
        list_BR = []
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
                for import_decl in tree.import_declarations:
                    if self.DEX_CLASS_LOADER in import_decl.name.value:
                        if self.CLASS_LOADER in str(tree):
                            PluginUtil.reportInfo(fileName, self.DexClassLoaderIssueDetails(fileName), res)

                # This will check if app register's a broadcast receiver dynamically
                if self.DYNAMIC_BROADCAST_RECEIVER in str(tree):
                    list_BR.append(fileName)

            except Exception:
                continue

        # Arrange the Broadcast Receivers created Dynamically in column format and store it in the variable -> Broadcast_Receiver
        Broadcast_Receiver = "\n".join(list_BR)

        if list_BR:
            PluginUtil.reportWarning(fileName, self.BroadcastReceiverIssueDetails(Broadcast_Receiver), res)

        queue.put(res)

    def DexClassLoaderIssueDetails(self, fileName):
        return 'Application dynamically load an external class through DexClassLoader\n%s\n' \
               'Even though this may not be a security issue always, be careful with what you are loading. \n' \
               'https://developer.android.com/reference/dalvik/system/DexClassLoader.html \n' \
               % fileName

    def BroadcastReceiverIssueDetails(self, Broadcast_Receiver):
        return 'Application dynamically registers a broadcast receiver\n' \
               'Application that register a broadcast receiver dynamically is vulnerable to granting unrestricted access to the broadcast receiver. \n' \
               'The receiver will be called with any broadcast Intent that matches filter.\n' \
               'https://developer.android.com/reference/android/content/Context.html#registerReceiver(android.content.BroadcastReceiver, android.content.IntentFilter)\n' \
               '%s\n' \
               % Broadcast_Receiver

    def getName(self):
        return "Dynamically loading code"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
