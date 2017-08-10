from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj
import lib.plyj.model as m
import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')


def broadcast_receiver(br_list):
    string = ("Application dynamically registers a broadcast receiver\nApplication that register a broadcast receiver "
              "dynamically is vulnerable to granting unrestricted access to the broadcast receiver.\nThe receiver will "
              "be called with any broadcast Intent that matches filter.\n https://developer.android.com/reference/android/"
              "content/Context.html#registerReceiver(android.content.BroadcastReceiver, android.content.IntentFilter)\n{}\n")
    return string.format(br_list)


def class_loader(file_name):
    string = ("Application dynamically loads an external class through DexClassLoader\n{}\n"
              "Even though this may not be a security issue always, be careful with what you are loading.\n"
              "https://developer.android.com/reference/dalvik/system/DexClassLoader.html \n")
    return string.format(file_name)


class DynamicallyLoadingCodePlugin(IPlugin):
    DEX_CLASS_LOADER = r'DexClassLoader'
    CLASS_LOADER = r'loadClass'
    DYNAMIC_BROADCAST_RECEIVER = r'registerReceiver'
    global receivers_list
    receivers_list = []

    def __init__(self):
        self.name = 'Dynamically loading code'

    # recursive function to find the loadclass function name by traversing down the AST
    def recursive_classloader_function(self, fields, f, res):
        if type(fields) is m.MethodDeclaration:
            if str(fields.name) == self.CLASS_LOADER:
                PluginUtil.reportInfo(file_name, class_loader(file_name), res)
            elif self.CLASS_LOADER in str(fields):
                PluginUtil.reportInfo(file_name, class_loader(file_name), res)
        elif type(fields) is list:
            for tree_object_fields in fields:
                self.recursive_classloader_function(tree_object_fields, f, res)
        elif hasattr(fields, '_fields'):
            for values in fields._fields:
                self.recursive_classloader_function(getattr(fields, values), f, res)
        return

    # recursive function to find the register receiver function name by traversing down the AST
    def recursive_register_receiver_function(self, fields, f, res):
        if type(fields) is m.MethodDeclaration:
            if str(fields.name) == self.DYNAMIC_BROADCAST_RECEIVER:
                receivers_list.append(file_name)
            elif self.DYNAMIC_BROADCAST_RECEIVER in str(fields):
                if file_name not in receivers_list:
                    receivers_list.append(file_name)
        elif type(fields) is list:
            for tree_object_fields in fields:
                self.recursive_register_receiver_function(tree_object_fields, f, res)
        elif hasattr(fields, '_fields'):
            for values in fields._fields:
                self.recursive_register_receiver_function(getattr(fields, values), f, res)
        return

    def target(self, queue):
        files = common.java_files
        global parser, tree, file_name
        parser = plyj.Parser()
        tree = ''
        res = []
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            file_name = str(f)
            try:
                # Parse the java file to an AST
                tree = parser.parse_file(f)
            except Exception as e:
                common.logger.exception(
                    "Unable to parse the file and generate as AST. Error: " + str(e))

            try:
                for import_decl in tree.import_declarations:
                    # Check if DexClassLoader is called in the import statement; example import dalvik.system.DexClassLoader
                    if self.DEX_CLASS_LOADER in import_decl.name.value:
                        for type_decl in tree.type_declarations:
                            # Check class declaration within the java source code
                            if type(type_decl) is m.ClassDeclaration:
                                # Traverse through every field declared in the class
                                for fields in type_decl.body:
                                    try:
                                        self.recursive_classloader_function(fields, f, res)
                                    except Exception as e:
                                        common.logger.error(
                                            "Unable to run class loader plugin " + str(e))
            except Exception:
                pass

            try:
                for type_decl in tree.type_declarations:
                    # Check class declaration within the java source code
                    if type(type_decl) is m.ClassDeclaration:
                        # Traverse through every field declared in the class
                        for fields in type_decl.body:
                            try:
                                self.recursive_register_receiver_function(fields, f, res)
                            except Exception as e:
                                common.logger.error(
                                    "Unable to run register receiver function plugin " + str(e))

            except Exception:
                pass

        # Arrange the Broadcast Receivers created Dynamically in column format and store it in the variable -> Broadcast_Receiver
        br_list = "\n".join(receivers_list)

        if receivers_list:
            # Report the issue in the file and display it on the terminal
            PluginUtil.reportWarning(file_name, broadcast_receiver(br_list), res)

        queue.put(res)

    def getName(self):
        return "Dynamically loading code"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
