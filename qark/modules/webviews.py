from __future__ import absolute_import
'''
Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
'''
import zipfile
import os
from genericpath import isdir
import subprocess
import logging
import shlex
import re
from .IssueType import IssueType, IssueSeverity
from .report import ReportIssue
from .common import Severity, ReportIssue
from .createExploit import ExploitType
from lib.pubsub import pub
from . import common
from .common import terminalPrint

common.logger = logging.getLogger()
logger = logging.getLogger(__name__)

IS_JS_ENABLED = "isjsenabled"
IS_FILE_ACCESS_ENABLED = "isfileaccessenabled"
IS_ADD_JS_INTERFACT_ENABLED = "isaddjsinterfaceenabled"
IS_DOM_STORAGE_ENABLED = "isdomstorageenabled"
IS_BASE_URL_DEFINED = "isbaseurldefined"
IS_CP_ACCESS_ENABLED = "iscpaccessenabled"
IS_UNIVERSAL_FILE_ACCESS_ENABLED = "isuniversalfileaccessenabled"

#TODO - This needs to be reworked as tokens for better accuracy, but so far it seems to work really consistently and well
#TODO - Need to separate checks for Chrome and Android clients

#Validate
def validate(queue):
    results = []
    wv_dec_list=find_webviews()
    #remove empty list items
    wv_dec_list=filter(None,wv_dec_list)
    #remove duplicates
    #Need to check why duplicates would even occur, may lead to false negatives
    wv_dec_list=common.dedup(wv_dec_list)

    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData("FOUND " + str(len(wv_dec_list)) + " WEBVIEWS:")
    results.append(issue)
    #BUG IN OUTPUT
    for p in wv_dec_list:
        issue = terminalPrint()
        issue.setLevel(Severity.INFO)
        issue.setData(str(p))
        results.append(issue)
        #logger.info(str(p))
    #print "\n"
    #search for WebView configuration settings
    wv_decs=find_wv_settings_dec(wv_dec_list, results)
    queue.put(results)
    return

#find webviews
def wv_config(file, rex_n):
    """
    Finds if webviews are defined in a file
    """
    found=False
    result=common.read_files(file,rex_n)
    if len(result)>0:
        found=True
    return found

def default_wv_config(wv, srcfile, sdk_ver,results):
    """
    Finds default webview configurations
    """
    #BUG - I believe we can remove the sdk_ver parameter here and use common.minSdk
    #BUG - Using common.minSdkVersion in comparisons fails to be evaluated properly

    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData("WEBVIEW DEFAULTS DO NOT APPEAR TO BE OVERRIDDEN-DISPLAYING DEFAULTS:")
    results.append(issue)
    if sdk_ver<19:
        issue = terminalPrint()
        issue.setLevel(Severity.WARNING)
        issue.setData(common.config.get('qarkhelper','WEBVIEW_SOP_WARNING'))
        results.append(issue)
    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData(common.config.get('qarkhelper', 'JS_OK'))
    results.append(issue)

    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData(common.config.get('qarkhelper', 'BURL_OK'))
    results.append(issue)

    issue = terminalPrint()
    issue.setLevel(Severity.WARNING)
    issue.setData(common.config.get('qarkhelper', 'FILE_SYS_WARN1') + common.config.get('qarkhelper', 'FILE_SYS_WARN2') + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/FILE_SYS_WARN.html." + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html")
    results.append(issue)

    issue = terminalPrint()
    issue.setLevel(Severity.WARNING)
    issue.setData(common.config.get('qarkhelper', 'WV_CPA_WARNING') + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/WV_CPA_WARNING.html" + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html")
    results.append(issue)
    if sdk_ver < 16:
        #minSdk <= 15 default is true; minSdk > 16 default is false
        issue = terminalPrint()
        issue.setLevel(Severity.WARNING)
        issue.setData(common.config.get('qarkhelper', 'UNIV_FILE_WARNING') + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/UNIV_FILE_WARNING.html" + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html")
        results.append(issue)
        #BUG - Need to double-check this, it doesn't appear to follow the same logic as the non-default checks
        if sdk_ver <16:
            issue = terminalPrint()
            issue.setLevel(Severity.WARNING)
            issue.setData(common.config.get('qarkhelper', 'FURL_FILE_WARNING') + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/FURL_FILE_WARNING.html" + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FURL_FILE_WARNING.html")
            results.append(issue)
        else:
            issue = terminalPrint()
            issue.setLevel(Severity.INFO)
            issue.setData(common.config.get('qarkhelper', 'FURL_FILE_OK'))
            results.append(issue)
    else:
        issue = terminalPrint()
        issue.setLevel(Severity.INFO)
        issue.setData(common.config.get('qarkhelper', 'UNIV_FILE_OK'))
        results.append(issue)
        skip_next=False
    #checking previous value above, as this is ignored if the above is true
    if sdk_ver < 18:
        issue = terminalPrint()
        issue.setLevel(Severity.INFO)
        issue.setData(common.config.get('qarkhelper', 'DEPRECATED_SINCE_9'))
        results.append(issue)
    else:
        issue = terminalPrint()
        issue.setLevel(Severity.INFO)
        issue.setData(common.config.get('qarkhelper', 'REMOVED_IN_18'))
        results.append(issue)

    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData(common.config.get('qarkhelper', 'NO_JS_INT'))
    results.append(issue)

    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData(common.config.get('qarkhelper', 'DOM_STORAGE_DIS'))
    results.append(issue)
    # TODO - Am I missing anything???
    return

def show_wv_vulns(s_list,i,results):
    """
    Shows all identified web view vulnerabilities
    """
    #BUG - This sometimes prints twice, successively which shouldn't happen
    #print "#"*100
    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData("WebView: " +str(i[0]))
    results.append(issue)
    #logger.info("WebView: " +str(i[0]))
    issue = terminalPrint()
    issue.setLevel(Severity.INFO)
    issue.setData("File: " + str(i[1]) +"\n")
    results.append(issue)
    #logger.info("File: " + str(i[1]) +"\n")

    if len(s_list)==0:
        default_wv_config(i[0], i[1], int(common.minSdkVersion), results)
        return

    for f in s_list:
        sl=re.sub(r'WebSettings\s*','',f)
        sl=re.sub(r'\s*[;=].*$','',sl)
        sl=re.sub(r'final\s','',sl)
        #strip string whitespace out
        sl=re.sub(r'^\W+','',sl)
        sl=re.sub(r'\.\w+\(\w+\)$','',sl)
        sl=sl.rstrip()
#Regex to look for javascript being enabled
#BUG I can reduce the number of files checked to only those that have the name / import WebViews
#Probably need to check for alternative true/false value representations
        wv_js_check=sl +'.setJavaScriptEnabled(true)'
        wv_js_check=re.escape(wv_js_check)
#check if webview JS in enabled
#BUG - THis can run twice, perhaps it is an artifact of an empty first element?
        if wv_config(i[1],wv_js_check):
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'JS_WARNING'))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.WARNING)
            issue.setExtras(IS_JS_ENABLED, True)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.WARNING)
            issue.setData(common.config.get('qarkhelper', 'TERMINAL_JS_WARNING') +" "+str(i[0]) +" "+common.config.get('qarkhelper', 'TERMINAL_JS_WARNING1') + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/JS_WARNING.html" + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/JS_WARNING.html\n")
            results.append(issue)
        else:
            issue = terminalPrint()
            issue.setLevel(Severity.INFO)
            issue.setData(common.config.get('qarkhelper', 'JS_OK') + " "+str(i[0]) + str(i[1]))
            results.append(issue)
#BUG - this is actually set on WebView
#Check whether webview sets arbitrary BaseURL
        wv_burl_check=re.escape(sl +'.loadDataWithBaseURL')
        if wv_config(i[1],wv_burl_check):
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'BURL_WARNING1'))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.WARNING)
            issue.setExtras(IS_BASE_URL_DEFINED, False)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.WARNING)
            issue.setData(common.config.get('qarkhelper', 'TERMINAL_BURL_WARNING1') + " "+str(i[0]) +" "+common.config.get('qarkhelper', 'TERMINAL_BURL_WARNING2') + "To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/BURL_WARNING.html " + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/BURL_WARNING.html\n")
            results.append(issue)
        else:
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'BURL_OK'))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.INFO)
            issue.setExtras(IS_BASE_URL_DEFINED, True)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.INFO)
            issue.setData(common.config.get('qarkhelper', 'BURL_OK'))
            results.append(issue)

    #Checks whether file URI can access filesystem
    #true by default, so the check is inverted
        wv_file_check=re.escape(sl+'.setAllowFileAccess(false)')
        if wv_config(i[1],wv_file_check):
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'FILE_SYS_OK'))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.WARNING)
            issue.setExtras(IS_FILE_ACCESS_ENABLED, False)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.INFO)
            issue.setData(common.config.get('qarkhelper', 'FILE_SYS_OK') + str(i[0]))
            results.append(issue)
        else:
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'FILE_SYS_WARN1'))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.WARNING)
            issue.setExtras(IS_FILE_ACCESS_ENABLED, True)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.WARNING)
            issue.setData(common.config.get('qarkhelper', 'TERMINAL_FILE_SYS_WARN1') + str(i[0]) +" "+ common.config.get('qarkhelper', 'TERMINAL_FILE_SYS_WARN2') + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/FILE_SYS_WARN.html " + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html\n")
            results.append(issue)
#Regex to determine if WebViews have Content Provider access (default = true)
    #Checks whether WebView can access Content Providers
    #true by default, so the check is inverted
    #BUG - This can run twice, perhaps due to an empty element
        wv_cpa_check=re.escape(sl+'.setAllowContentAccess(false)')
        if wv_config(i[1],wv_cpa_check):
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'WV_CPA_OK'))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.INFO)
            issue.setExtras(IS_CP_ACCESS_ENABLED, False)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.INFO)
            issue.setData(common.config.get('qarkhelper', 'WV_CPA_OK') + str(i[0]))
            results.append(issue)
        else:
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'WV_CPA_WARNING'))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.WARNING)
            issue.setExtras(IS_CP_ACCESS_ENABLED, True)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.WARNING)
            issue.setData(common.config.get('qarkhelper', 'TERMINAL_WV_CPA_WARNING') + str(i[0]) + "To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/WV_CPA_WARNING.html " + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html\n")
            results.append(issue)
    #check for JS access from file URL can access content from any origin
    #minSdk <= 15 default is true; minSdk > 16 default is false
    #BUG - This check is wrong on the second if; If set to false and not found, it prints OK
        if int(common.minSdkVersion) <16:
            wv_univ_file_access=re.escape(sl+'.setAllowUniversalAccessFromFileURLs(false)')
            if not wv_config(i[1],wv_univ_file_access):
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'UNIV_FILE_WARNING'))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.WARNING)
                issue.setExtras(IS_FILE_ACCESS_ENABLED, True)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.WARNING)
                issue.setData(common.config.get('qarkhelper', 'TERMINAL_UNIV_FILE_WARNING') +str(i[0]) + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/UNIV_FILE_WARNING.html " + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html\n")
                results.append(issue)
                skip_next=True
            else:
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'UNIV_FILE_OK'))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.INFO)
                issue.setExtras(IS_FILE_ACCESS_ENABLED, False)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.INFO)
                issue.setData(common.config.get('qarkhelper', 'UNIV_FILE_OK') + str(i[0]))
                results.append(issue)
                skip_next=False
    #checking previous value above, as this is ignored if the above is true
    #could I just put pass above?
            if skip_next:
                pass
            else:
                #minSdk <= 15 default is true; minSdk > 16 default is false
                wv_allow_file_access_furls=re.escape(sl+'.setAllowFileAccessFromFileURLs(false)')
                if wv_config(i[1],wv_allow_file_access_furls):
                    issue = terminalPrint()
                    issue.setLevel(Severity.INFO)
                    issue.setData("This WebView does not have access to File URLs - setAllowFileAccessFromFileURLs(false)" + str(i[0]))
                    results.append(issue)

                    issue = ReportIssue()
                    issue.setCategory(ExploitType.WEBVIEW)
                    issue.setDetails("This WebView does not have access to File URLs - setAllowFileAccessFromFileURLs(false)")
                    issue.setFile(str(i[1]))
                    issue.setSeverity(Severity.WARNING)
                    issue.setExtras(IS_FILE_ACCESS_ENABLED, False)
                    results.append(issue)
                else:
                    issue = ReportIssue()
                    issue.setCategory(ExploitType.WEBVIEW)
                    issue.setDetails(common.config.get('qarkhelper', 'UNIV_FILE_WARNING'))
                    issue.setFile(str(i[1]))
                    issue.setSeverity(Severity.WARNING)
                    results.append(issue)

                    issue = terminalPrint()
                    issue.setLevel(Severity.WARNING)
                    issue.setExtras(IS_FILE_ACCESS_ENABLED, True)
                    issue.setData(common.config.get('qarkhelper', 'TERMINAL_UNIV_FILE_WARNING') + str(i[0]) + "To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/UNIV_FILE_WARNING2.html "+ "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING2.html\n")
                    results.append(issue)

        else:
            wv_univ_file_access=re.escape(sl+'.setAllowUniversalAccessFromFileURLs(true)')
            if wv_config(i[1],wv_univ_file_access):
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'UNIV_FILE_WARNING'))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.WARNING)
                issue.setExtras(IS_UNIVERSAL_FILE_ACCESS_ENABLED, True)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.WARNING)
                issue.setData(common.config.get('qarkhelper', 'TERMINAL_UNIV_FILE_WARNING') + '1 '+str(i[0]) + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/UNIV_FILE_WARNING.html " + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html\n")
                results.append(issue)
                skip_next=True

            else:
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'UNIV_FILE_OK'))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.INFO)
                issue.setExtras(IS_UNIVERSAL_FILE_ACCESS_ENABLED, False)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.INFO)
                issue.setData(common.config.get('qarkhelper', 'UNIV_FILE_OK') + str(i[0]))
                results.append(issue)
                skip_next=False
    #checking previous value above, as this is ignored if the above is true
                if skip_next:
                    pass
                else:
                    #minSdk <= 15 default is true; minSdk > 16 default is false
                        wv_allow_file_access_furls=re.escape(sl+'.setAllowFileAccessFromFileURLs(true)')
                        if wv_config(i[1],wv_allow_file_access_furls):
                            issue = ReportIssue()
                            issue.setCategory(ExploitType.WEBVIEW)
                            issue.setDetails(common.config.get('qarkhelper', 'FURL_FILE_WARNING'))
                            issue.setFile(str(i[1]))
                            issue.setSeverity(Severity.WARNING)
                            issue.setExtras(IS_UNIVERSAL_FILE_ACCESS_ENABLED, True)
                            results.append(issue)

                            issue = terminalPrint()
                            issue.setLevel(Severity.WARNING)
                            issue.setData(common.config.get('qarkhelper', 'TERMINAL_FURL_FILE_WARNING') + str(i[0]) + "To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/FURL_FILE_WARNING.html " + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FURL_FILE_WARNING.html\n")
                            results.append(issue)
                        else:
                            issue = ReportIssue()
                            issue.setCategory(ExploitType.WEBVIEW)
                            issue.setDetails(common.config.get('qarkhelper', 'FURL_FILE_OK'))
                            issue.setFile(str(i[1]))
                            issue.setSeverity(Severity.INFO)
                            issue.setExtras(IS_UNIVERSAL_FILE_ACCESS_ENABLED, False)
                            results.append(issue)

                            issue = terminalPrint()
                            issue.setLevel(Severity.INFO)
                            issue.setData(common.config.get('qarkhelper', 'FURL_FILE_OK') + str(i[0]))
                            results.append(issue)

    #Checking whether plugins are enabled for WebViews
    #setPluginsEnabled deprecated in API 9, removed in API 18
    #setPluginState added in API 8, deprecated in API 18
        wv_plugsinenabled=re.escape(sl+'.setPluginsEnabled(true)')
        wv_pluginstate=re.escape(sl+'.setPluginState(WebSettings.PluginState.ON*')

        if wv_config(i[1],wv_plugsinenabled):
            if int(common.minSdkVersion) < 18:
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'DEPRECATED_SINCE_9') +str(i[0]) + "<br>FILE: " +str(i[1]))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.INFO)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.INFO)
                issue.setData(common.config.get('qarkhelper', 'DEPRECATED_SINCE_9') +str(i[0]))
                results.append(issue)
            else:
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'REMOVED_IN_18')+str(i[0]) + "<br>FILE: " +str(i[1]))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.INFO)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.INFO)
                issue.setData(common.config.get('qarkhelper', 'REMOVED_IN_18')+str(i[0]))
                results.append(issue)
                logger.info(common.config.get('qarkhelper', 'REMOVED_IN_18')+str(i[0]))
        if wv_config(i[1],wv_pluginstate):
            if int(common.minSdkVersion) < 8:
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'ADDED_IN_8')+str(i[0]) + "<br>FILE: " +str(i[1]))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.INFO)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.INFO)
                issue.setData(common.config.get('qarkhelper', 'ADDED_IN_8')+str(i[0]))
                results.append(issue)
                logger.info(common.config.get('qarkhelper', 'ADDED_IN_8')+str(i[0]))
            else:
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'DEPRECATED_IN_18')+str(i[0])
                + "<br>FILE: " +str(i[1]))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.INFO)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.INFO)
                issue.setData(common.config.get('qarkhelper', 'DEPRECATED_IN_18')+str(i[0]))
                results.append(issue)
    #Check if addJavascriptInterface is used in WebView
    #BUG - this is actually on WebView, not settings
        wv_ajs=re.escape(sl+'.addJavascriptInterface')
        if wv_config(i[1],wv_ajs):
            if int(common.minSdkVersion)<17:
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'BAD_JS_INT'))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.WARNING)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.WARNING)
                issue.setData(common.config.get('qarkhelper', 'TERMINAL_BAD_JS_INT') + " "+str(i[0]) + " To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/BAD_JS_INT.html " + "Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/BAD_JS_INT.html" +"\n")
                results.append(issue)
            else:
                issue = ReportIssue()
                issue.setCategory(ExploitType.WEBVIEW)
                issue.setDetails(common.config.get('qarkhelper', 'OK_JS_INT') + str(i[0])
                + "<br>FILE: " +str(i[1]))
                issue.setFile(str(i[1]))
                issue.setSeverity(Severity.INFO)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.INFO)
                issue.setData(common.config.get('qarkhelper', 'OK_JS_INT'))
                results.append(issue)
        else:
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'NO_JS_INT')
            + "<br>FILE: " +str(i[1]))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.INFO)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.INFO)
            issue.setData(common.config.get('qarkhelper', 'NO_JS_INT') + str(i[0]))
            results.append(issue)

    #Check if WebView has DOMStorage enabled
        wv_setdom=re.escape(sl+'.setDomStorageEnabled(true)')
        if wv_config(i[1],wv_setdom):
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'DOM_STORAGE_EN') + str(i[0])
            + "<br>FILE: " +str(i[1]))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.INFO)
            issue.setExtras(IS_DOM_STORAGE_ENABLED, True)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.INFO)
            issue.setData(common.config.get('qarkhelper', 'DOM_STORAGE_EN'))
            results.append(issue)
        else:
            issue = ReportIssue()
            issue.setCategory(ExploitType.WEBVIEW)
            issue.setDetails(common.config.get('qarkhelper', 'DOM_STORAGE_DIS')
            + "<br>FILE: " +str(i[1]))
            issue.setFile(str(i[1]))
            issue.setSeverity(Severity.INFO)
            issue.setExtras(IS_DOM_STORAGE_ENABLED, False)
            results.append(issue)

            issue = terminalPrint()
            issue.setLevel(Severity.INFO)
            issue.setData(common.config.get('qarkhelper', 'DOM_STORAGE_DIS') + str(i[0]))
            results.append(issue)

    return


#BUG - Probably need to copy the logic from the Content Provider here, although I haven't actually found
#BUG - A WebView that QARK actually missed yet, perhaps they were just not extended as deep
def find_webviews():
    """
    Finds all webviews in the decompiled source code
    """
    #1. Look for classes that extend WebView
    #Find classes that extend Web View
    wv_list=find_ext('WebView')
    #2. Look for classes that extend classes that extend WebView
    while len(common.tree(wv_list)) > 1:
        wv_list+=common.tree(wv_list)

    wv_list.append(['WebView','']) 
    #3. Cleanup?
    #4. Look for all declaration of WebViews using normal and extended class names
    #BUG sometimes multiple declarations are coming back for z[0], need to figure out what is going on there
    #Currently there may be false negatives
    #BUG - Need to review this for optional/multiple spaces
    wv_decs=[]
    wv_decs.append([])
    for x in wv_list:
        if len(x)>0:
            tmp=r''+re.escape(str(x[0]))+r'\s\w+[;=]'
            wv_decs+=common.text_scan(common.java_files,tmp)
            tmp=r'(private .*|protected.*)'+ re.escape(str(x[0]))+r'\s\w+;'
            wv_decs+=common.text_scan(common.java_files,tmp)
            tmp=r'\w+\s[;=]\snew\s'+re.escape(str(x[0]))+r'\('
            wv_decs+=common.text_scan(common.java_files,tmp)
            tmp=r'\(.*'+re.escape(str(x[0]))+r'\s\w+.*\)' # Need to ensure this is working properly

    tmp_list2=[]
    tmp_list2.append([])
    for z in wv_decs:
        if len(z)>0:
            #conditional declarations will cause conditional positives
            #BUG sometimes Z[0] is a list, rather than just a list element. Need to separate, remove and re-parse
            if (len(z[0])>1 and not isinstance(z[0],str)):
                for x in z[0]:
                    foo=[x,z[1]]
                    tmp_list2.append(foo)
                wv_decs.pop()
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
            y[0]=re.sub(r'^\s*WebView\b','',y[0])
            y[0]=re.sub(r'\s*[;=]\s*new\sWebView\s.*','',y[0])
            y[0]=re.sub(r'\s*[;=]\s*new\s\w+\(.*\)','',y[0])
            y[0]=re.sub(r'^\s*','',y[0])
            y[0]=re.sub(r'\s*$','',y[0])
            y[0]=re.sub(r'^\w+\s','',y[0])
            y[0]=re.sub(r';$','',y[0])
            #remove whitespace
            y[0]=y[0].strip(' \t\r\n')

    tmp_list2=common.dedup(tmp_list2)

    return tmp_list2


def find_wv_settings_dec(wv_list, results):
    """
    Deprecated code
    """
    for e in wv_list:
        if len(e)>0:
            settings_list=common.read_files(e[1],r'WebSettings\s*\w+\s*[;=]\s*\w+\.getSettings\(')
            settings_list+=common.read_files(e[1],r'WebSettings\s*\w+\s*[;=]\s*getSettings\(')
            wv_set_rex=r''+str(e[0])+r'\.getSettings\('
            settings_list+=common.read_files(e[1],wv_set_rex)
            show_wv_vulns(settings_list,e, results)
    return

#find clases that extend something
def find_ext(class_name):
    """
    Function to find if a class extends any other type and return the results in a list
    """
    extension_list=[]
    extension_list.append([])
    ext_string=r'class.*extends\s+'+re.escape(class_name)+r'\s*(<.*>)?(implements.*)?\s*{'
    extension_list=text_scan(common.java_files,ext_string)
    for y in extension_list:
        if len(y)>0:
            y[0]=re.sub(r';\\n','',str(y[0]).strip('[]\''))
            y[0]=re.sub(r'^.*\w+\sclass','',y[0])
            y[0]=re.sub(r'\sextends.*','',y[0])
            y[0]=re.sub(r'<.*>','',y[0])
            y[0]=str(y[0]).strip()
    return extension_list

#look for text
def text_scan(file_list,rex_n):
    """
    Given a list of files, search content of each file by the regular expression and return a list of matches
    """
    result_list=[]
    result_list.append([])
    count = 0
    for x in file_list:
        count = count + 1
        pub.sendMessage('progress', bar='Webview checks', percent=round(count*100/common.java_files.__len__()))
        result=common.read_files(x,rex_n)
        if len(result)>0:
            result_list.append([result,x])
    return result_list
