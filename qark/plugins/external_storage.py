import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '../lib')
from yapsy.IPlugin import IPlugin
from plugins import PluginUtil
from modules import common
from lib.pubsub import pub
import lib.plyj.parser as plyj


class ExternalStorageCheckPlugin(IPlugin):

    CHECK_EXTERNAL_STORAGE = r'getExternalFilesDir'
    CHECK_EXTERNAL_MEDIA = r'getExternalMediaDirs'
    CHECK_PUBLIC_DIR = r'getExternalStoragePublicDirectory'

    def __init__(self):
        self.name = 'External Storage Issues'

    def target(self, queue):
        files = common.java_files
        global parser, tree, file_name
        parser = plyj.Parser()
        tree = ''
        res = []
        external_storage = []
        external_media = []
        external_pub_dir = []
        count = 0
        for file in files:
            count += 1
            pub.sendMessage('progress', bar=self.name, percent=round(count * 100 / len(files)))
            file_name = str(file)
            try:
                tree = parser.parse_file(file)
            except Exception:
                continue
            try:
                for import_decl in tree.import_declarations:
                    if 'File' in import_decl.name.value:
                        with open(file_name, 'r') as f:
                            file_body = f.read()
                        if PluginUtil.contains(self.CHECK_EXTERNAL_STORAGE, file_body):
                            external_storage.append(file_name)
                            break

                        if PluginUtil.contains(self.CHECK_EXTERNAL_MEDIA, file_body):
                            external_media.append(file_name)
                            break

                        if PluginUtil.contains(self.CHECK_PUBLIC_DIR, file_body):
                            external_pub_dir.append(file_name)
                            break

            except Exception:
                continue

        # Store the content obtained above in a column format
        storage = "\n".join(external_storage)
        media = "\n".join(external_media)
        pub_dir = "\n".join(external_pub_dir)

        if external_storage:
            PluginUtil.reportWarning(file_name, self.external_storage_issue(storage), res)

        if external_media:
            PluginUtil.reportWarning(file_name, self.media_directory_issue(media), res)

        if external_pub_dir:
            PluginUtil.reportWarning(file_name, self.public_directory_issue(pub_dir), res)

        queue.put(res)

    def external_storage_issue(self, storage):
        return 'Reading files stored on External Storage makes it vulnerable to data injection attacks\n' \
               'Note that this code does no error checking and there is no security enforced with these files. \n' \
               'For example, any application holding WRITE_EXTERNAL_STORAGE can write to these files.\n%s.\n' \
               'Reference: https://developer.android.com/reference/android/content/Context.html#getExternalFilesDir(java.lang.String)\n' \
               % storage

    def media_directory_issue(self, media):
        return 'Reading files stored on External Media Directory makes it vulnerable to data injection attacks\n ' \
               'Note that this code does no error checking and there is no security enforced with these files. \n' \
               'For example, any application holding WRITE_EXTERNAL_STORAGE can write to these files.\n%s.\n' \
               'Reference: https://developer.android.com/reference/android/content/Context.html#getExternalMediaDir(java.lang.String)\n' \
               % media

    def public_directory_issue(self, pub_dir):
        return 'Reading files stored on External Storage Public Directory makes it vulnerable to data injection attacks\n ' \
               'Note that this code does no error checking and there is no security enforced with these files. \n' \
               'For example, any application holding WRITE_EXTERNAL_STORAGE can write to these files. \n%s.\n' \
               'Reference: https://developer.android.com/reference/android/os/Environment.html#getExternalStoragePublicDirectory(java.lang.String)\n' \
               % pub_dir

    def getName(self):
        return "External Storage Issues"

    def getCategory(self):
        # Currently unused, but will be used later for clubbing issues from a specific plugin (when multiple plugins run at the same time)
        return "PLUGIN ISSUES"

    def getTarget(self):
        return self.target
