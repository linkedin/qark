from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
'''
import logging

from modules import common
from modules import IssueType
from modules import report
from modules.IssueType import IssueType, IssueSeverity

common.logger = logging.getLogger()
logger = logging.getLogger(__name__)

def verify_allow_backup(app):
    """
    Check if AllowBackup option is enabled in manifest.xml
    """
    try:
        if 'android:allowBackup' in app[0].attributes.keys():
            if app[0].attributes['android:allowBackup'].value == 'true':
                report.write_badger("manifest-issues", common.Severity.WARNING, common.config.get('qarkhelper', 'WARN_BACK'))

                logger.warn(common.config.get('qarkhelper', 'WARN_BACK'))
            else:
                report.write_badger("manifest-issues", common.Severity.INFO, common.config.get('qarkhelper', 'BACK_OK'))
                logger.info(common.config.get('qarkhelper', 'BACK_OK'))
        else:
            report.write_badger("manifest-issues", common.Severity.INFO, common.config.get('qarkhelper', 'WARN_BACK_MISSING'))
            logger.warn(common.config.get('qarkhelper', 'WARN_BACK_MISSING'))
        return
    except Exception as e:
        print e.message

def verify_custom_permissions():
    """
    Verify if the application defines any custom permissions
    """
    #check for custom permissions and protection level
    for node in common.xmldoc.getElementsByTagName('permission'):
        if 'android:protectionLevel' in node.attributes.keys():
            if (node.attributes['android:protectionLevel'].value == 'signature' or node.attributes['android:protectionLevel'].value == 'signatureOrSystem'):
                #TODO - Add API check to ignore this for unaffected versions
                if common.minSdkVersion<21:
                    report.write_badger("manifest-issues", common.Severity.WARNING,  "Permission: " + node.attributes['android:name'].value + common.config.get('qarkhelper', 'PERM_SNATCH_SIG'))
                    logger.warn("Permission: " + node.attributes['android:name'].value + " " + common.config.get('qarkhelper', 'PERM_SNATCH_SIG') )
        else:
            #need to research if this represents some type of error condition
            report.write_badger("manifest-issues", common.Severity.INFO, common.config.get('qarkhelper', 'NO_PERM_PROT'))
            logger.debug(common.config.get('qarkhelper', 'NO_PERM_PROT'))
    return

def verify_debuggable(app):
    '''
    Verify whether the debuggable flag is set in the manifest
    '''
    if 'android:debuggable' in app[0].attributes.keys():
        if app[0].attributes['android:debuggable'].value == 'true':
            report.write_badger("manifest-issues", common.Severity.VULNERABILITY,  "The android:debuggable flag is manually set to true in the AndroidManifest.xml. This will cause your application to be debuggable in production builds and can result in data leakage and other security issues. It is not necessary to set the android:debuggable flag in the manifest, it will be set appropriately automatically by the tools. More info: http://developer.android.com/guide/topics/manifest/application-element.html#debug")
            common.logger.log(common.VULNERABILITY_LEVEL, "The android:debuggable flag is manually set to true in the AndroidManifest.xml. This will cause your application to be debuggable in production builds and can result in data leakage and other security issues. It is not necessary to set the android:debuggable flag in the manifest, it will be set appropriately automatically by the tools. More info: http://developer.android.com/guide/topics/manifest/application-element.html#debug")

    return
        
