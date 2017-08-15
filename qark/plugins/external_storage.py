from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import sys
import os
import lib.plyj.parser as plyj

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')

STRING = ("Reading files stored on {} makes it vulnerable to data injection attacks\n"
          "Note that this code does no error checking and there is no security enforced with these files. \n"
          "For example, any application holding WRITE_EXTERNAL_STORAGE can write to these files.\nFilepath: {}\n"
          "Reference: https://developer.android.com/reference/android/content/Context.html#{}\n")


def check_media_directory(media):
    return STRING.format("External Media Directory", media, "getExternalMediaDir(java.lang.String)")


def check_public_directory(pub_dir):
    return STRING.format("External Storage Public Directory", pub_dir, "getExternalStoragePublicDirectory(java.lang.String)")


def check_external_storage(storage):
    return STRING.format("External Storage", storage, "getExternalFilesDir(java.lang.String)")


class ExternalStorageCheckPlugin(IPlugin):
    CHECK_EXTERNAL_STORAGE = r'getExternalFilesDir'
    CHECK_EXTERNAL_MEDIA = r'getExternalMediaDirs'
    CHECK_PUBLIC_DIR = r'getExternalStoragePublicDirectory'

    def __init__(self):
        self.name = 'External Storage Issues'

    def target(self, queue):
        global filepath, tree
        files = common.java_files
        parser = plyj.Parser()
        tree = ''
        external_pub_dir, external_media, external_storage, res = ([] for _ in xrange(4))
        count = 0
        for f in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            filepath = str(f)
            try:
                tree = parser.parse_file(f)
            except Exception as e:
                common.logger.exception(
                    "Unable to parse the file and generate as AST. Error: " + str(e))
                continue
            try:
                for import_decl in tree.import_declarations:
                    if 'File' in import_decl.name.value:
                        with open(filepath, 'r') as fr:
                            file_body = fr.read()
                        if PluginUtil.contains(self.CHECK_EXTERNAL_STORAGE, file_body):
                            external_storage.append(filepath)
                            break

                        if PluginUtil.contains(self.CHECK_EXTERNAL_MEDIA, file_body):
                            external_media.append(filepath)
                            break

                        if PluginUtil.contains(self.CHECK_PUBLIC_DIR, file_body):
                            external_pub_dir.append(filepath)
                            break

            except Exception as e:
                common.logger.debug("Plyj parser failed while parsing the file: " + filepath + "\nError" + str(e))
                continue

        # Store the content obtained above in a column format
        storage = "\n".join(external_storage)
        media = "\n".join(external_media)
        pub_dir = "\n".join(external_pub_dir)

        if external_storage:
            PluginUtil.reportWarning(filepath, check_external_storage(storage), res)

        if external_media:
            PluginUtil.reportWarning(filepath, check_media_directory(media), res)

        if external_pub_dir:
            PluginUtil.reportWarning(filepath, check_public_directory(pub_dir), res)

        queue.put(res)

    @staticmethod
    def getName():
        return "External Storage Issues"

    @staticmethod
    def getCategory():
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
