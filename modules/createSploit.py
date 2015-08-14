'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import shutil
import errno
import os
from modules import common
from modules.common import logger
import fileinput

class exploitType:
    """
    Enum type for exploitatin category
    """
    MANIFEST, ACTIVITY, INTENT, PERMISSION, SERVICE, RECEIVER, BROADCAST_INTENT = range(7)


def copyTemplate(src,dest):
    """
    Given a source and destination, copy all files/folders under source to destination\n
    Overwrites destination if any files/folders already exists\n
    Used to copy the exploit template
    """
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
            status='ERROR'
        else:
            print('Directory not copied. Error: %s' % e)
            #TODO - give an option to specify a different dir, if the specified one already exists
            status='ERROR'
	return status
    
def addVulnerable(obj,key,value):
    """
    Common method to add a new vulnerability\n
    Takes common.exploitdata as the object, exploitType enum, string representation of the vulnerable code to be replaced in the exploit template
    """
    obj[key].append(value)
    

def modifyTemplate(path,filename,temp_text,repl_text):
    """
    Deprecated code
    """
    tmp=path+filename
    tmp2=path+filename+'_tmp'
    f1 = open(tmp, 'r')
    f2 = open(tmp2, 'w')
    for line in f1:
    		f2.write(line.replace(temp_text, repl_text))
    #putting back template text, for re-use
    f2.write('//REPLACEME-TT2')
    f1.close()
    f2.close()
    os.remove(tmp)
    os.rename(tmp2,tmp)
    return
    
def modifyTemplate2(filename,placeholder,replacement):
    """
    Takes a filename,placeholder value to be replaced and the actual replacement value\n
    Uncomments the commented out code from exploit template, replaces the placeholder with actual value and adds this content on the next line to facilitate multiple substitutions
    """
    flag = False
    for line in fileinput.input(filename, inplace=1):
        if placeholder in line:
            if str(line).strip().startswith("//"):
                line1 = str(line).split("//")[1]
                flag=True
            #print line1.replace(placeholder, replacement)
        print line,
        if flag:
            print line1.replace(placeholder, replacement),
            flag=False

def createUsing(replacementData):
    """
    Core of the exploit generation\n
    Takes in a dictionary with (exploittype,replacement value) data, processes them to find all substitutions, and looks up the config.properties to identify all applicable files that require substution
    """
    path = common.getConfig("rootDir") + '/build/qark'
    data = dict(replacementData)
    for key,value in data.iteritems():
        if key==exploitType.BROADCAST_INTENT:
            exploit_type="BROADCAST_INTENT"
        elif key==exploitType.ACTIVITY:
            exploit_type="ACTIVITY"
        elif key==exploitType.INTENT:
            exploit_type="INTENT"
        elif key==exploitType.MANIFEST:
            exploit_type="MANIFEST"
        elif key==exploitType.PERMISSION:
            exploit_type="PERMISSION"
        elif key==exploitType.RECEIVER:
            exploit_type="RECEIVER"
        elif key==exploitType.SERVICE:
            exploit_type="SERVICE"
        for instance in value:
            replacement_keys = dict(common.config.items('exploit'))
            for type_key,type_value in replacement_keys.iteritems():
                if exploit_type in str(type_key).upper():
                    replacement_files = dict(common.config.items(type_value))
                    for file_key,file_value in replacement_files.iteritems():
                        modifyTemplate2(path + file_value, type_value, instance)