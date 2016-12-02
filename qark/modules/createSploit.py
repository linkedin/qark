from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import shutil
import errno
import fileinput
import os

from modules import common
from modules.common import logger

class exploitType:
    """
    Enum type for exploitatin category
    """
    MANIFEST, ACTIVITY, INTENT, PERMISSION, SERVICE, RECEIVER, BROADCAST_INTENT = range(7)


def copy_template(src,dest):
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

def modify_template(path,filename,temp_text,repl_text):
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
    
def modify_template_2(filename,placeholder,replacement):
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
