from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import re

from modules import common

def find_content_providers():
    """
    Find all content providers and return the list
    """
    cp_list=common.find_ext('ContentProvider')

    growing=1
    #TODO - This is ugly and needs to be re-written
    #The intention here is to loop endlessly until all extensions are found
    while growing:
        cp_list_count_old=len(cp_list)
        cp_list+=common.tree(cp_list)
        if len(cp_list) == cp_list_count_old:
            growing=0

    cp_list.append(['ContentProvider',''])

    cp_decs=[]
    cp_decs.append([])
    for x in cp_list:
        if len(x)>0:
            tmp=r''+re.escape(str(x[0]))+r'\s\w+[;=]'
            cp_decs+=common.text_scan(common.java_files,tmp)
            tmp=r'(private .*|protected.*)'+ re.escape(str(x[0]))+r'\s\w+;'
            cp_decs+=common.text_scan(common.java_files,tmp)
            tmp=r'\w+\s[;=]\snew\s'+re.escape(str(x[0]))+r'\('
            cp_decs+=common.text_scan(common.java_files,tmp)
            tmp=r'\(.*'+re.escape(str(x[0]))+r'\s\w+.*\)' # Need to ensure this is working properly

    tmp_list2=[]
    tmp_list2.append([])
    for z in cp_decs:
        if len(z)>0:
            #conditional declarations will cause conditional positives
            #BUG sometimes Z[0] is a list, rather than just a list element. Need to separate, remove and re-parse
            if (len(z[0])>1 and not isinstance(z[0],str)):
                for x in z[0]:
                    foo=[x,z[1]]
                    tmp_list2.append(foo)
                cp_decs.pop()
                continue
            else:
                tmp_list2.append(z)
        else:
            tmp_list2.append(z)

    tmp_list2=filter(None,tmp_list2)

    for y in tmp_list2:
        if len(y)>0:
            y[0]=re.sub(r';\\n','',str(y[0]).strip('[]\''))
            y[0]=re.sub(r'\\t*','',y[0])
            y[0]=re.sub(r'\s*private\b','',y[0])
            y[0]=re.sub(r'\s*protected\b','',y[0])
            y[0]=re.sub(r'\s*static\b','',y[0])
            y[0]=re.sub(r'^\s*ContentProvider\b','',y[0])
            y[0]=re.sub(r'\s*[;=]\s*new\sContentProvider\s.*','',y[0])
            y[0]=re.sub(r'\s*[;=]\s*new\s\w+\(.*\)','',y[0])
            y[0]=re.sub(r'^\s*','',y[0])
            y[0]=re.sub(r'\s*$','',y[0])
            y[0]=re.sub(r'^\w+\s','',y[0])
            y[0]=re.sub(r';$','',y[0])
            #remove whitespace
            y[0]=y[0].strip(' \t\r\n')

    tmp_list2=common.dedup(tmp_list2)
    return tmp_list2

def content_provider_uri_permissions():
    cpName=""
    #TODO - Need to rectify this with the exported/non-exported providers
    for node in common.xmldoc.getElementsByTagName('provider'):
        if 'android:name' in node.attributes.keys():
            cpName=node.attributes['android:name'].value
        if 'android:grantUriPermissions' in node.attributes.keys():
            if (node.attributes['android:grantUriPermissions'].value == 'true'):
                common.logger.warning("Permission can be granted to any of the Content Provider "+str(cpName)+"'s data, this is probably not intentional and could potentially lead to information disclosure. Please review AndroidManifest.xml. More details: http://developer.android.com/guide/topics/manifest/provider-element.html")
            else:
                for x in node.getElementsByTagName('grant-uri-permission'):
                    if 'android:path' in x.attributes.key():
                        if x.attributes['android:path'].value=='/':
                            if 'android:pathPrefix' not in x.attributes.keys():
                                common.logger.warning("This application appears to allow granting access to the root path / of the ContentProvider " + str(cpName)+ ", which could lead to information disclosure, due to the use of an / as the path value, with no pathPrefix specified in the grant-uri-permission element. Please review AndroidManifest.xml. More details: http://developer.android.com/guide/topics/manifest/provider-element.html")
    return
