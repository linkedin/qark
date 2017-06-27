from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import re,sys
import logging
from multiprocessing import Process

from modules import common
from modules import report
import lib.plyj.parser as plyj
import lib.plyj.model as m
from lib.progressbar import *
from modules.report import ReportIssue
from modules.common import Severity, ReportIssue
from modules.createExploit import ExploitType
from lib.pubsub import pub
from modules.common import terminalPrint

parser = plyj.Parser()
tree=''
filename=''
sslSessions=[]
verifyIteration=0
warningGiven=False
#Checking whether x509 certitificates are properly validated

'''
There is still plenty of work to be done here to raise this to a "confirmed" vulnerability level, but we'll leave that for the roadmap as it at least raises the flag for now and is not part of the exploit APK
'''

def validate(queue,height):
    """
    Validates common pitfalls for certificate validation logic
    """
    #writer1 = common.Writer((0, height))
    results = []
    global tree
    global parser
    global filename
    global warningGiven
    global sslSessions
    count = 0

    for j in common.java_files:
        sslSessions=[]
        count = count + 1
        pub.sendMessage('progress', bar='X.509 Validation', percent=round(count*100/common.java_files.__len__()))
        filename=str(j)
        try:
            tree=parser.parse_file(j)
        except Exception as e:
            continue
            # No need to log this since we now warn potential parsing errors on screen and provide details in the report.
        if tree is None:
            results.append("Some files may not be parsed correctly. For a list of such files, please review the final report.")
        else:
            try:
                for type_decl in tree.type_declarations:
                    if type(type_decl) is m.ClassDeclaration:
                        for t in type_decl.body:
                            try:
                                recursive_insecure_trust_manager(t,j,results)
                            except Exception as e:
                                common.logger.error("Unable to run recursive_insecure_trust_manager in certValidation.py: " + str(e))
                            try:
                                recursive_insecure_ssl_error_handling(t, j, results)
                            except Exception as e:
                                common.logger.error(
                                    "Unable to run recursive_insecure_ssl_error_handling in certValidation.py " + str(e))
                            try:
                                recursive_allow_all_hostname_verifier(t,j,results)
                            except Exception as e:
                                common.logger.error("Unable to run recursive_allow_all_hostname_verifier in certValidation.py: " + str(e))
                            try:
                                recursive_ssl_session(t,j,results)
                            except Exception as e:
                                common.logger.error("Unable to run recursive_ssl_session in certValidation.py: " + str(e))
            except Exception as e:
                if common.source_or_apk==2:
                    common.logger.error("Error in validate function of certValidation.py: " + str(e))
                else:
                    common.logger.error("Bad file: " + str(j) + ", this is not uncommon")
            try:
                recursive_find_verify(None,j,results)
            except Exception as e:
                common.logger.error("Problem in findVerify function of certValidation.py: " + str(e))
        warningGiven=False
    unverified_sessions(results)
    queue.put(results)
    return

def recursive_insecure_trust_manager(t,filename,results):
    if type(t) is m.MethodDeclaration:
        if str(t.name)=='checkServerTrusted':
            if len(t.body)==0:
                issue = ReportIssue()
                issue.setCategory(ExploitType.CERTIFICATE)
                issue.setDetails("Instance of checkServerTrusted, with no body found in: " + str(filename) +". This means this application is likely vulnerable to Man-In-The-Middle attacks. This can be confirmed using the free version of Burpsuite. Simply set the Android device's proxy to use Burpsuite via the network settings, but DO NOT install the Portswigger CA certificate on the device. If you still see traffic in the proxy, the app is vulnerable. Note: You need to ensure you exercise this code path. If you are unsure, make sure you click through each part of the application which makes network requests. You may need to toggle the proxy on/off to get past sections that do validate certificates properly in order to reach the vulnerable code. This proves that it will accept certificates from any CA. You should always validate your configuration by visiting an HTTPS site in the native browser and verifying you receive a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html")
                issue.setFile(filename)
                issue.setSeverity(Severity.WARNING)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.WARNING)
                issue.setData("Instance of checkServerTrusted, with no body found in: " + str(filename) +". This means this application is likely vulnerable to Man-In-The-Middle attacks. This can be confirmed using the free version of Burpsuite. Simply set the Android device's proxy to use Burpsuite via the network settings, but DO NOT install the Portswigger CA certificate on the device. If you still see traffic in the proxy, the app is vulnerable. Note: You need to ensure you exercise this code path. If you are unsure, make sure you click through each part of the application which makes network requests. You may need to toggle the proxy on/off to get past sections that do validate certificates properly in order to reach the vulnerable code. This proves that it will accept certificates from any CA. You should always validate your configuration by visiting an HTTPS site in the native browser and verifying you receive a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html")
                results.append(issue)
            else:
                for b in t.body:
                    if type(b) is m.Return:
                        #TODO - This needs to be fleshed out more, but it will have to wait due to time constraints
                        issue = terminalPrint()
                        issue.setLevel(Severity.WARNING)
                        issue.setData("Instance of checkServerTrusted, which only returns " + str(filename) +". This means this application is likely vulnerable to Man-In-The-Middle attacks. This can be confirmed using the free version of Burpsuite. Simply set the Android device's proxy to use Burpsuite via the network settings, but DO NOT install the Portswigger CA certificate on the device. If you still see traffic in the proxy, the app is vulnerable. Note: You need to ensure you excercise this code path. If you are unsure, make sure you click through each part of the application which makes network requests. You may need to toggle the proxy on/off to get past sections that do validate certificates properly in order to reach the vulnerable code. This proves that it will accept certitificates from any CA. You should always validate your configuration by visiting an HTTPS site in the native browser and verifying you receive a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html")
                        results.append(issue)

                        issue = ReportIssue()
                        issue.setCategory(ExploitType.CERTIFICATE)
                        issue.setDetails("Instance of checkServerTrusted, which only returns " + str(filename) +". This means this application is likely vulnerable to Man-In-The-Middle attacks. This can be confirmed using the free version of Burpsuite. Simply set the Android device's proxy to use Burpsuite via the network settings, but DO NOT install the Portswigger CA certificate on the device. If you still see traffic in the proxy, the app is vulnerable. Note: You need to ensure you excercise this code path. If you are unsure, make sure you click through each part of the application which makes network requests. You may need to toggle the proxy on/off to get past sections that do validate certificates properly in order to reach the vulnerable code. This proves that it will accept certitificates from any CA. You should always validate your configuration by visiting an HTTPS site in the native browser and verifying you receive a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html")
                        issue.setFile(filename)
                        issue.setSeverity(Severity.WARNING)
                        results.append(issue)
                    else:
                        break #TODO - only want to check once, to see if it's only a return, can probably be replaced by len()
    elif type(t) is list:
        for x in t:
            recursive_insecure_trust_manager(x,filename,results)
    elif hasattr(t,'_fields'):
        for f in t._fields:
            recursive_insecure_trust_manager(getattr(t,f),filename,results)
    return

# onReceivedSSLError check
def recursive_insecure_ssl_error_handling(t, filename, results):
    if type(t) is m.MethodDeclaration:
        if str(t.name) == 'onReceivedSslError':
            if "proceed" in str(t.body):
                issue = ReportIssue()
                issue.setCategory(ExploitType.CERTIFICATE)
                issue.setDetails("Unsafe implementation of onReceivedSslError handler found in: " + str(
                    filename) + ". Specifically, the implementation ignores all SSL certificate validation errors, making your app vulnerable to man-in-the-middle attacks. To properly handle SSL certificate validation, change your code to invoke SslErrorHandler.cancel(). For details, please see: https://developer.android.com/reference/android/webkit/WebViewClient.html")
                issue.setFile(filename)
                issue.setSeverity(Severity.WARNING)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.WARNING)
                issue.setData("Unsafe implementation of onReceivedSslError handler found in: " + str(
                    filename) + ". Specifically, the implementation ignores all SSL certificate validation errors, making your app vulnerable to man-in-the-middle attacks. To properly handle SSL certificate validation, change your code to invoke SslErrorHandler.cancel(). For details, please see: https://developer.android.com/reference/android/webkit/WebViewClient.html")
                results.append(issue)

    elif type(t) is list:
        for x in t:
            recursive_insecure_ssl_error_handling(x, filename, results)
    elif hasattr(t, '_fields'):
        for f in t._fields:
            recursive_insecure_ssl_error_handling(getattr(t, f), filename, results)
    return

def recursive_allow_all_hostname_verifier(t,filename,results):
    #TODO - This can be fleshed out to be more of an accurate, exhaustive check, but will suffice for now
    if type(t) is m.Assignment:
        if type(t.rhs) is m.InstanceCreation:
            if hasattr(t.rhs,'type'):
                if hasattr(t.rhs.type,'name'):
                    if hasattr(t.rhs.type.name,'value'):
                        if str(t.rhs.type.name.value)=='AllowAllHostnameVerifier':
                            #TODO - The list below will eventually be used to check the code for bad verifiers, but will wait for now, due to time constraints
                            if hasattr(t.lhs,'value'):
                                issue = ReportIssue()
                                issue.setCategory(ExploitType.CERTIFICATE)
                                issue.setDetails("AllowAllHostnameVerifier: " + str(t.lhs.value) + " found in " + str(filename) + ". This can allow for impromper x.509 certificate validation wherein the DNS hostname does not match the Common or Subject Alternative Name(s) on the certificate, making the application vulnerable to Man-In-The-Middle attacks. This means the application may potentially accept a certificate from any trusted CA, regardless of the domain it was issued for. The can be validated using the free version of Burpsuite by installing the Portswigger CA certificate, thereby making it a trusted CA on the device. Set the device network settings to use the Burpsuite proxy, then go Proxy > Options > Edit the Proxy Listener by changing the Certificate tab to Generate a CA-signed certificate with a specific hostname and enter a domain like foobar.com which doesn't match the domain name(s) the app is connecting to normally. You should always verify your results by visiting an https site in the native browser and confirming you see a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html")
                                issue.setFile(filename)
                                issue.setSeverity(Severity.WARNING)
                                results.append(issue)

                                issue = terminalPrint()
                                issue.setLevel(Severity.WARNING)
                                issue.setData("AllowAllHostnameVerifier: " + str(t.lhs.value) + " found in " + str(filename) + ". This can allow for impromper x.509 certificate validation wherein the DNS hostname does not match the Common or Subject Alternative Name(s) on the certificate, making the application vulnerable to Man-In-The-Middle attacks. This means the application may potentially accept a certificate from any trusted CA, regardless of the domain it was issued for. The can be validated using the free version of Burpsuite by installing the Portswigger CA certificate, thereby making it a trusted CA on the device. Set the device network settings to use the Burpsuite proxy, then go Proxy > Options > Edit the Proxy Listener by changing the Certificate tab to Generate a CA-signed certificate with a specific hostname and enter a domain like foobar.com which doesn't match the domain name(s) the app is connecting to normally. You should always verify your results by visiting an https site in the native browser and confirming you see a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html")
                                results.append(issue)

    elif type(t) is m.MethodInvocation:
        if hasattr(t,'name'):
            if str(t.name) == 'setHostnameVerifier':
                if hasattr(t,'arguments'):
                    for a in t.arguments:
                        if type(a) is m.Name:
                            if hasattr(a,'value'):
                                if re.search(r'\.ALLOW_ALL_HOSTNAME_VERIFIER$',str(a.value)):
                                    issue = ReportIssue()
                                    issue.setCategory(ExploitType.CERTIFICATE)
                                    issue.setDetails("ALLOW_ALL_HOSTNAME_VERIFIER invoked : " + str(a.value) + " in " + str(filename) + ". This can allow for impromper x.509 certificate validation wherein the DNS hostname does not match the Common or Subject Alternative Name(s) on the certificate, making the application vulnerable to Man-In-The-Middle attacks. This means the application may potentially accept a certificate from any trusted CA, regardless of the domain it was issued for. The can be validated using the free version of Burpsuite by installing the Portswigger CA certificate, thereby making it a trusted CA on the device. Set the device network settings to use the Burpsuite proxy, then go Proxy > Options > Edit the Proxy Listener by changing the Certificate tab to Generate a CA-signed certificate with a specific hostname and enter a domain like foobar.com which doesn't match the domain name(s) the app is connecting to normally. You should always verify your results by visiting an https site in the native browser and confirming you see a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html")
                                    issue.setFile(filename)
                                    issue.setSeverity(Severity.WARNING)
                                    results.append(issue)

                                    issue = terminalPrint()
                                    issue.setLevel(Severity.WARNING)
                                    issue.setData("ALLOW_ALL_HOSTNAME_VERIFIER invoked : " + str(a.value) + " in " + str(filename) + ". This can allow for impromper x.509 certificate validation wherein the DNS hostname does not match the Common or Subject Alternative Name(s) on the certificate, making the application vulnerable to Man-In-The-Middle attacks. This means the application may potentially accept a certificate from any trusted CA, regardless of the domain it was issued for. The can be validated using the free version of Burpsuite by installing the Portswigger CA certificate, thereby making it a trusted CA on the device. Set the device network settings to use the Burpsuite proxy, then go Proxy > Options > Edit the Proxy Listener by changing the Certificate tab to Generate a CA-signed certificate with a specific hostname and enter a domain like foobar.com which doesn't match the domain name(s) the app is connecting to normally. You should always verify your results by visiting an https site in the native browser and confirming you see a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html")
                                    results.append(issue)
    elif type(t) is list:
        for x in t:
            recursive_allow_all_hostname_verifier(x,filename,results)
    elif hasattr(t,'_fields'):
        for f in t._fields:
            recursive_allow_all_hostname_verifier(getattr(t,f),filename,results)
    return

def recursive_ssl_session(t,filename,results):
    '''
    Looks for use of a HostnameVerifier where no call to .verify is made
    '''
    #common.logger.info("We are still working on the check to verify that all invocations of a HostnameVerifier call the .verify method to catch any exceptions when validating X.509 certificates. Check for updates soon! In the meantime, please see this URL for further details: https://developer.android.com/training/articles/security-ssl.html")
    '''
    We need to find all uses of SSLSession
    '''
    global sslSessions

    try:
        if type(t) is m.VariableDeclaration:
            if hasattr(t,'type'):
                if type(t.type) is m.Type:
                    if re.search(r'SSLSession',str(t)):
                        if hasattr(t.type,'name'):
                            if hasattr(t.type.name,'value'):
                                if t.type.name.value=='SSLSession':
                                    if hasattr(t,'variable_declarators'):
                                        for d in t.variable_declarators:
                                            if type(d) is m.VariableDeclarator:
                                                if hasattr(d,'variable'):
                                                    sslSessions.append(str(d.variable.name))
        elif type(t) is list:
            for l in t:
                recursive_ssl_session(l,filename,results)
        elif hasattr(t,'_fields'):
            for f in t._fields:
                recursive_ssl_session(getattr(t,f),filename,results)
    except Exception as e:
        common.logger.debug("Something went wrong in certValidation.py's recursive_ssl_session: " + str(e))
        common.parsingerrors.add(str(filename))
    return

def recursive_find_verify(q,filename,results):
    '''
    Find all .verify methods 
    '''
    global sslSessions
    global tree
    global verifyIteration
    global warningGiven

    if len(sslSessions)>0:
        if verifyIteration==0:
            try:
                for type_decl in tree.type_declarations:
                    if type(type_decl) is m.ClassDeclaration:
                        for t in type_decl.body:
                            if type(t) is m.MethodInvocation:
                                if hasattr(t,'name'):
                                    if str(t.name)=='verify':
                                        if hasattr(t,'arguments'):
                                            if len(t.arguments)!=2:
                                                if not warningGiven:
                                                    issue = ReportIssue()
                                                    issue.setCategory(ExploitType.CERTIFICATE)
                                                    issue.setDetails("Custom verify method used in " + str(filename) + ". You should manually review certificate validation here." )
                                                    issue.setFile(filename)
                                                    issue.setSeverity(Severity.WARNING)
                                                    results.append(issue)

                                                    issue = terminalPrint()
                                                    issue.setLevel(Severity.WARNING)
                                                    issue.setData("Custom verify method used in " + str(filename) + ". You should manually review certificate validation here." )
                                                    results.append(issue)
                                                    warningGiven=True
                                            else:
                                                for r in q.arguments:
                                                    continue
                            elif type(t) is m.MethodDeclaration:
                                if hasattr(t,'name'):
                                    if str(t.name)=='verify':
                                        if not warningGiven:
                                            issue = ReportIssue()
                                            issue.setCategory(ExploitType.CERTIFICATE)
                                            issue.setDetails("Custom verify method declared in " + str(filename) + ". You should manually review certificate validation here." )
                                            issue.setFile(filename)
                                            issue.setSeverity(Severity.WARNING)
                                            results.append(issue)

                                            issue = terminalPrint()
                                            issue.setLevel(Severity.WARNING)
                                            issue.setData("Custom verify method declared in " + str(filename) + ". You should manually review certificate validation here." )
                                            results.append(issue)
                                            warningGiven=True
                            elif type(t) is list:
                                for l in t:
                                    if type(l) is not None:
                                        verifyIteration=1
                                        recursive_find_verify(l,filename,results)
                            elif hasattr(t,'_fields'):
                                for f in t._fields:
                                    if type(getattr(t,f)) is not None:
                                        verifyIteration=1
                                        recursive_find_verify(getattr(t,f),filename,results)
                                    elif type(t) is list:
                                        for l in t:
                                            if type(l) is not None:
                                                verifyIteration=1
                                                recursive_find_verify(l,filename,results)
                                    elif hasattr(t,'_fields'):
                                        for f in t._fields:
                                            if type(getattr(t,f)) is not None:
                                                verifyIteration=1
                                                recursive_find_verify(getattr(t,f),filename,results)
            except Exception as e:
                common.logger.debug("Something went wrong in certValidation.py's findVerify: " + str(e))
                report.write("parsingerror-issues-list", "Something went wrong in certValidation.py's findVerify: " + str(e), "strong")
        else:
            if type(q) is m.MethodInvocation:
                if hasattr(q,'name'):
                    if str(q.name)=='verify':
                        if hasattr(q,'arguments'):
                            if len(q.arguments)!=2:
                                if not warningGiven:
                                    issue = ReportIssue()
                                    issue.setCategory(ExploitType.CERTIFICATE)
                                    issue.setDetails("Custom verify method used in " + str(filename) + ". You should manually review certificate validation here." )
                                    issue.setFile(filename)
                                    issue.setSeverity(Severity.WARNING)
                                    results.append(issue)

                                    issue = terminalPrint()
                                    issue.setLevel(Severity.WARNING)
                                    issue.setData("Custom verify method used in " + str(filename) + ". You should manually review certificate validation here." )
                                    results.append(issue)
                                    warningGiven=True
                            else:
                                common.logger.debug("sslSessions Before: " + str(sslSessions))
                                if str(q.arguments[1]) in sslSessions:
                                    sslSessions.remove(str(q.arguments[1]))
                                    common.logger.debug("sslSessions After: " + str(sslSessions))

                            #For each verify method, check whether the session being verified is in sslSessions and if so, remove it(considering it verified)
                            #This is not full proof at all, for several reasons, but we know it's definitely vulnerable if it's never verified, assuming no strange code
                            #TODO - check that the .verify actually belongs to a HostnameVerifier
                            #TODO - verify that .verify is not over ridden somewhere
            elif type(q) is m.MethodDeclaration:
                if hasattr(q,'name'):
                    if str(q.name)=='verify':
                        if not warningGiven:
                            issue = ReportIssue()
                            issue.setCategory(ExploitType.CERTIFICATE)
                            issue.setDetails("Custom verify method declared in " + str(filename) + ". You should manually review certificate validation here." )
                            issue.setFile(filename)
                            issue.setSeverity(Severity.WARNING)
                            results.append(issue)

                            issue = terminalPrint()
                            issue.setLevel(Severity.WARNING)
                            issue.setData("Custom verify method declared in " + str(filename) + ". You should manually review certificate validation here." )
                            results.append(issue)
                            warningGiven=True
            elif type(q) is list:
                for l in q:
                    if type(l) is not None:
                        recursive_find_verify(l,filename,results)
            elif hasattr(q,'_fields'):
                for f in q._fields:
                    if type(getattr(q,f)) is not None:
                        recursive_find_verify(getattr(q,f),filename,results)
                    elif type(q) is list:
                        for l in q:
                            if type(l) is not None:
                                recursive_find_verify(l,filename,results)
                    elif hasattr(q,'_fields'):
                        for f in q._fields:
                            if type(getattr(q,f)) is not None:
                                recursive_find_verify(getattr(q,f),filename,results)
        verifyIteration=1
        unverified_sessions(results)
    return

def unverified_sessions(results):
    global sslSessions
    #This is untested because I could not find a vulnerable app, which didn't have a custom .verify method
    for s in sslSessions:
        issue = ReportIssue()
        issue.setCategory(ExploitType.CERTIFICATE)
        issue.setDetails("Potential Man-In-The-Middle vulnerability - There appear to be SSLSession (boolean) objects which are not checked using the HostnameVerifier.verify method. You should manually inspect these in: " + str(filename) + ". Please see this URL for details: https://developer.android.com/training/articles/security-ssl.html")
        issue.setSeverity(Severity.WARNING)
        results.append(issue)

        issue = terminalPrint()
        issue.setLevel(Severity.WARNING)
        issue.setData("Potential Man-In-The-Middle vulnerability - There appear to be SSLSession (boolean) objects which are not checked using the HostnameVerifier.verify method. You should manually inspect these in: " + str(filename) + ". Please see this URL for details: https://developer.android.com/training/articles/security-ssl.html")
        results.append(issue)
    sslSessions=[]
    return
