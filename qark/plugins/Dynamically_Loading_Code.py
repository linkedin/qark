import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')
from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj
import lib.plyj.model as m


class DynamicallyLoadingCodePlugin(IPlugin):
    DEX_CLASS_LOADER = r'DexClassLoader'
    CLASS_LOADER = r'loadClass'
    DYNAMIC_BROADCAST_RECEIVER = r'registerReceiver'
    global list_BR
    list_BR = []

    def __init__(self):
        self.name = 'Dynamically loading code'

    # recursive function to find the loadclass function name by traversing down the AST
    def recursive_classloader_function(self, t, filename, res):
        if type(t) is m.MethodDeclaration:
            if str(t.name) == self.CLASS_LOADER:
                PluginUtil.reportInfo(fileName, self.DexClassLoaderIssueDetails(fileName), res)
            # if the function name is not found this might give a try to search the content of the method to avoid false neagtive
            elif self.CLASS_LOADER in str(t):
                PluginUtil.reportInfo(fileName, self.DexClassLoaderIssueDetails(fileName), res)

        elif type(t) is list:
            for x in t:
                self.recursive_classloader_function(x, filename, res)
        elif hasattr(t, '_fields'):
            for f in t._fields:
                self.recursive_classloader_function(getattr(t, f), filename, res)
        return

    # recursive function to find the register receiver function name by traversing down the AST
    def recursive_register_receiver_function(self, t, filename, res):

        if type(t) is m.MethodDeclaration:
            if str(t.name) == self.DYNAMIC_BROADCAST_RECEIVER:
                list_BR.append(fileName)

        elif type(t) is list:
            for x in t:
                self.recursive_register_receiver_function(x, filename, res)
        elif hasattr(t, '_fields'):
            for f in t._fields:
                self.recursive_register_receiver_function(getattr(t, f), filename, res)
        return

    def target(self, queue):
        files = common.java_files
        global parser, tree, fileName
        parser = plyj.Parser()
        tree = ''
        res = []

        #List of Broadcast Receiver

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
                        for type_decl in tree.type_declarations:
                            if type(type_decl) is m.ClassDeclaration:
                                for t in type_decl.body:
                                    try:
                                        self.recursive_classloader_function(t, f, res)
                                    except Exception as e:
                                        common.logger.error(
                                            "Unable to run class loader plugin " + str(e))

                # This will check if app register's a broadcast receiver dynamically
                if self.DYNAMIC_BROADCAST_RECEIVER in str(tree):
                    list_BR.append(fileName)

            except Exception:
                continue

            try:
                for type_decl in tree.type_declarations:
                    if type(type_decl) is m.ClassDeclaration:
                        for t in type_decl.body:
                            try:
                                self.recursive_register_receiver_function(t, f, res)
                            except Exception as e:
                                common.logger.error(
                                    "Unable to run register receiver function plugin " + str(e))

            # This will check if app register's a broadcast receiver dynamically
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
