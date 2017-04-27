from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''


import os, platform
import urllib2
import sys
import zipfile
import logging
import subprocess
import shlex
import stat
from subprocess import Popen, PIPE, STDOUT
import re,shutil, tarfile

from modules import common

common.logger = logging.getLogger()
logger = logging.getLogger(__name__)

def is_android_sdk_installed():
    """
    Verify if Android SDK is installed and available for use by QARK
    """
    if common.getConfig('AndroidSDKPath'):
        os.environ["PATH"] += os.pathsep + common.getConfig('AndroidSDKPath') +'/tools' + os.pathsep + common.getConfig('AndroidSDKPath') +'/platform-tools' + os.pathsep + common.getConfig('AndroidSDKPath') +'/tools/lib'
        os.environ["ANDROID_HOME"] = common.getConfig('AndroidSDKPath')
        return True
    else:
        return False

def get_android_sdk_manager():
    """
    Gets the location of SDK manager through CLI while in interactive mode, or via settings.properties if running headlessly
    """
    print common.term.yellow + str(common.config.get('qarkhelper','ANDROID_SDK_INFO')).decode('string-escape').format(t=common.term)
    print common.term.cyan
    choice=raw_input(common.config.get('qarkhelper','GET_ANDROID_SDK_MANAGER_PROMPT'))
    if str(choice).lower()=='y':
        download_sdk()
    else:
        AndroidSDKPath=raw_input(common.config.get('qarkhelper','ANDROID_SDK_MANAGER_PATH_PROMPT'))
        if not str(AndroidSDKPath).endswith("/"):
            AndroidSDKPath = str(AndroidSDKPath).strip() + "/"
        #common.writeKey('AndroidSDKPath', AndroidSDKPath)
        while not (os.path.exists(AndroidSDKPath + "tools")):
            logger.error(str(common.config.get('qarkhelper','ANDROID_SDK_MANAGER_PATH_PROMPT_AGAIN')).decode('string-escape'))
            print common.term.cyan
            AndroidSDKPath=raw_input(common.config.get('qarkhelper','ANDROID_SDK_MANAGER_PATH_PROMPT'))
            if not str(AndroidSDKPath).endswith("/"):
                AndroidSDKPath = str(AndroidSDKPath).strip() + "/"
        common.writeKey('AndroidSDKPath', AndroidSDKPath)
        common.AndroidSDKPath = AndroidSDKPath
    common.logger.debug("Located SDK")

def extract(tar_url, extract_path):
    print tar_url
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])

def download_sdk():
    """
    Download the SDK from Google
    """

    url = ""
    url_macosx = "https://dl.google.com/android/android-sdk_r24.0.2-macosx.zip"
    url_linux = "https://dl.google.com/android/android-sdk_r24.3.4-linux.tgz"

    if sys.platform == "linux2":
        url = url_linux
    else:
        url = url_macosx

    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(common.getConfig("rootDir") + "/" + file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    common.logger.debug("Downloading: %s \r\n FileName: %s \r\n FileSize: \r\n %s" % (url, file_name, file_size))
    
    block_sz = file_size/100
    count = 0
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
        count = count + 1
        if count%10==0:
            sys.stdout.write('\r[{0}] {1}%'.format('#'*(count/10), count))
            sys.stdout.flush()
            
    f.close()
    androidSDKZIP = f.name
    print common.term.cyan + str(common.config.get('qarkhelper','FILE_DOWNLOADED_TO')) + androidSDKZIP.decode('string-escape').format(t=common.term)
    print common.term.cyan + str(common.config.get('qarkhelper','UNPACKING')) + androidSDKZIP.decode('string-escape').format(t=common.term)
    if sys.platform == "linux2":
        try:
            if not os.path.exists(androidSDKZIP.rsplit(".",1)[0]):
                os.makedirs(androidSDKZIP.rsplit(".",1)[0])
            extract(androidSDKZIP, androidSDKZIP.rsplit(".",1)[0])
        except Exception as e:
            logger.error(e.message)
        common.writeKey('AndroidSDKPath', androidSDKZIP.rsplit(".",1)[0] + "/android-sdk-linux/")
    else:
        zf = zipfile.ZipFile(androidSDKZIP)
        for filename in [ zf.namelist()]:
            try:
                if not os.path.exists(androidSDKZIP.rsplit(".",1)[0]):
                    os.makedirs(androidSDKZIP.rsplit(".",1)[0])
                zf.extractall(androidSDKZIP.rsplit(".",1)[0] + "/", zf.namelist(), )
            except Exception as e:
                logger.error(e.message)
            else:
                logger.info('Done')
        common.writeKey('AndroidSDKPath', androidSDKZIP.rsplit(".",1)[0] + "/android-sdk-macosx/")
    #We dont need the ZIP file anymore
    os.remove(androidSDKZIP)
    run_sdk_manager()
    
def run_sdk_manager():
    """
    Runs the SDK manager
    """
    flag_no_ui = " --no-ui"
    android = common.getConfig('AndroidSDKPath') + "tools/android"
    #need to have execute permission on the android executable
    st = os.stat(android)
    os.chmod(android, st.st_mode | stat.S_IEXEC)
    #Android list sdk
    android_cmd1= android + "list" + "sdk" + "-a"
    args1 = shlex.split(android_cmd1)
    p0 = Popen([android, 'list', 'sdk', '-a'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    #regexpattern = re.compile(r'Android SDK Platform-tools|Android SDK Build-tools|SDK Platform Android 5.0.1|Android Support Repository|Android Support Library')
    regexpattern = re.compile(r'SDK Platform Android 5.0.1, API 21, revision 2|Android SDK Build-tools, revision 21.1.2|Android Support Repository|Android Support Library|Android SDK Platform-tools')
    selected_filters_list = []
    for line in p0.stdout:
        if regexpattern.search(line):
            common.logger.debug('Selected the following packages for installation:\r\n')
            common.logger.debug(str(line.rstrip()))
            selected_filters_list.append(line.rstrip().split('-')[0].strip())
            if len(selected_filters_list)==5:
                # We have the basic filters needed to compile the exploit APL at this point.
                break
    #Android install build tools  with selected filters in headless mode
    selected_filters = myString = ",".join(selected_filters_list)
    print selected_filters
    p1 = Popen([android, 'update','sdk','-a','--filter',selected_filters,'--no-ui'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=1)
    if not common.interactive_mode:
        p1.stdin.write(common.args.acceptterms)
    else:
        p1.stdin.write("y\n")
    for line in iter(p1.stdout.readline, b''):
        print line,
        if "Do you accept the license" in line:
            p1.stdin.flush()
            p1.stdin.write("y\n")
    output, err = p1.communicate("y\n")
    common.set_environment_variables()





#build_apk takes in all paths relative to the '/build/' folder in QARK
def build_apk(path):
    """
    Builds the APK when path the the source is available
    """
    print "------------ Building Exploit APK ------------"
    currentDir = common.getConfig("rootDir") if common.buildLocation == '' else common.buildLocation
    os.chdir(currentDir + "/build/" + path)
    properties = open('local.properties','w+')
    os.chdir(currentDir)
    properties.write('sdk.dir='+common.getConfig('AndroidSDKPath'))
    properties.close()
    os.chdir(currentDir + "/build/" + path)
    if common.buildLocation != '':  # adb expects settings.properties. If building from a different directory, need to copy it over to the new build directory
        try:
            settings_properties_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../settings.properties'))
            destination = '{}/{}/{}'.format(os.path.abspath(currentDir), 'build/', path)
            shutil.copy(settings_properties_path, destination)
            shutil.copy(settings_properties_path, common.buildLocation)
            print('[INFO] - TRIED COPYING {} TO {}'.format(settings_properties_path, destination))
        except Exception as e:
            print('[ERROR] - COPYING SETTINGS.PROPERTIES FROM QARK DIRECTORY FAILED')
            settings_properties_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../settings.properties'))
            print('[ERROR] - TRIED COPYING {} TO {}'.format(settings_properties_path,os.path.join(currentDir, "/build/", path)))
            print('[ERROR] - currentDir: {}'.format(currentDir))
            print(e)
    p1 = Popen(['./gradlew',"assembleDebug"], stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=1)
    for line in iter(p1.stdout.readline, b''):
        print line,
