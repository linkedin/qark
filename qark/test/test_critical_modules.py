import pdb
import sys
import os
import mock
import pytest
from Queue import Queue
import ConfigParser

from modules import common
from modules import  filePermissions
from modules import  webviews
from modules import  cryptoFlaws
from modules import  certValidation
from modules import  findPending
from modules import  findBroadcasts
from modules import report


def get_all_java_files():
    return ['./testData/goatdroid/classes_dex2jar/android/support/v4/app/TaskStackBuilder.java', 
            './testData/goatdroid/classes_dex2jar/android/support/v4/app/TaskStackBuilderHoneycomb.java', 
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/BuildConfig.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/R.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/About.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/AddVenue.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/AdminHome.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/AdminOptions.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/Checkins.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/DestinationInfo.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/DoAdminDeleteUser.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/DoAdminPasswordReset.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/DoComment.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/Friends.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/GenericWebViewActivity.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/Home.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/Login.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/Main.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/Preferences.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/Register.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/Rewards.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/SendSMS.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/SocialAPIAuthentication.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewFriendRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewProfile.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/adapter/AvailableRewardsAdapter.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/adapter/SearchForFriendsAdapter.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/base/BaseActivity.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/base/BaseFragmentActivity.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/base/BaseTabsViewPagerActivity.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/base/BaseUnauthenticatedActivity.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/base/RequestBase.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/base/ResponseBase.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/broadcastreceivers/SendSMSNowReceiver.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/db/CheckinDBHelper.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/db/UserInfoDBHelper.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/AvailableRewards.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/DeleteUsers.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/DoCheckin.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/MyFriends.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/MyRewards.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/PendingFriendRequests.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/ResetUserPasswords.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/SearchForFriends.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/javascriptinterfaces/SmsJSInterface.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/javascriptinterfaces/ViewCheckinJSInterface.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/javascriptinterfaces/WebViewJSInterface.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/misc/Constants.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/misc/Utils.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/AuthenticatedRestClient.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/CustomSSLSocketFactory.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/RequestMethod.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/ResponseBase.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/RestClient.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/addvenue/AddVenueRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/addvenue/AddVenueResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/admin/AdminRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/admin/AdminResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/checkin/CheckinRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/checkin/CheckinResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/comments/CommentsRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/comments/CommentsResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/friends/FriendRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/friends/FriendResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/history/HistoryRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/history/HistoryResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/login/LoginRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/login/LoginResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/preferences/PreferencesRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/preferences/PreferencesResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/register/RegisterRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/register/RegisterResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/rewards/RewardsRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/rewards/RewardsResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/searchforfriends/SearchForFriendsRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/searchforfriends/SearchForFriendsResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/viewcheckin/ViewCheckinRequest.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/rest/viewcheckin/ViewCheckinResponse.java',
            './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/services/LocationService.java']

rootGoatdroidDir = ('./testData/goatdroid')

@pytest.fixture
def findAllJavaFiles():
    return common.find_java(rootGoatdroidDir)

def findAllXmlFiles():
    return common.find_xml(rootGoatdroidDir)

def setup():
    common.java_files = get_all_java_files()
    config = ConfigParser.RawConfigParser()
    script_location=os.path.dirname(os.path.abspath(__file__))
    script_location+='/../modules/config.properties'
    with open(script_location,'r') as f:
        body = f.read()
    config.read(script_location)
    common.config = config

def test_certValidation():
    setup()

    output = Queue()
    certValidation.validate(output, 2)
    output = output.get()
    outputTups = [x if type(x) is str else terminalPrintToTuple(x) if x.__class__.__name__ == 'terminalPrint' else reportIssueToTuple(x) for x in output]

    assert outputTups == ['Some files may not be parsed correctly. For a list of such files, please review the final report.',
                          'Some files may not be parsed correctly. For a list of such files, please review the final report.',
                          (7, "Instance of checkServerTrusted, with no body found in: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/CustomSSLSocketFactory.java. This means this application is likely vulnerable to Man-In-The-Middle attacks. This can be confirmed using the free version of Burpsuite. Simply set the Android device's proxy to use Burpsuite via the network settings, but DO NOT install the Portswigger CA certificate on the device. If you still see traffic in the proxy, the app is vulnerable. Note: You need to ensure you exercise this code path. If you are unsure, make sure you click through each part of the application which makes network requests. You may need to toggle the proxy on/off to get past sections that do validate certificates properly in order to reach the vulnerable code. This proves that it will accept certificates from any CA. You should always validate your configuration by visiting an HTTPS site in the native browser and verifying you receive a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html", {},
                          './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/CustomSSLSocketFactory.java',
                          '', 1), 
                          ("Instance of checkServerTrusted, with no body found in: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/CustomSSLSocketFactory.java. This means this application is likely vulnerable to Man-In-The-Middle attacks. This can be confirmed using the free version of Burpsuite. Simply set the Android device's proxy to use Burpsuite via the network settings, but DO NOT install the Portswigger CA certificate on the device. If you still see traffic in the proxy, the app is vulnerable. Note: You need to ensure you exercise this code path. If you are unsure, make sure you click through each part of the application which makes network requests. You may need to toggle the proxy on/off to get past sections that do validate certificates properly in order to reach the vulnerable code. This proves that it will accept certificates from any CA. You should always validate your configuration by visiting an HTTPS site in the native browser and verifying you receive a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html", {}, 1), 
                          (7, "ALLOW_ALL_HOSTNAME_VERIFIER invoked : org.apache.http.conn.ssl.SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER in ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/CustomSSLSocketFactory.java. This can allow for impromper x.509 certificate validation wherein the DNS hostname does not match the Common or Subject Alternative Name(s) on the certificate, making the application vulnerable to Man-In-The-Middle attacks. This means the application may potentially accept a certificate from any trusted CA, regardless of the domain it was issued for. The can be validated using the free version of Burpsuite by installing the Portswigger CA certificate, thereby making it a trusted CA on the device. Set the device network settings to use the Burpsuite proxy, then go Proxy > Options > Edit the Proxy Listener by changing the Certificate tab to Generate a CA-signed certificate with a specific hostname and enter a domain like foobar.com which doesn't match the domain name(s) the app is connecting to normally. You should always verify your results by visiting an https site in the native browser and confirming you see a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html", {},
                          './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/CustomSSLSocketFactory.java',
                          '', 1), 
                          ("ALLOW_ALL_HOSTNAME_VERIFIER invoked : org.apache.http.conn.ssl.SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER in ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/requestresponse/CustomSSLSocketFactory.java. This can allow for impromper x.509 certificate validation wherein the DNS hostname does not match the Common or Subject Alternative Name(s) on the certificate, making the application vulnerable to Man-In-The-Middle attacks. This means the application may potentially accept a certificate from any trusted CA, regardless of the domain it was issued for. The can be validated using the free version of Burpsuite by installing the Portswigger CA certificate, thereby making it a trusted CA on the device. Set the device network settings to use the Burpsuite proxy, then go Proxy > Options > Edit the Proxy Listener by changing the Certificate tab to Generate a CA-signed certificate with a specific hostname and enter a domain like foobar.com which doesn't match the domain name(s) the app is connecting to normally. You should always verify your results by visiting an https site in the native browser and confirming you see a certificate warning. For details, please see: https://developer.android.com/training/articles/security-ssl.html", {}, 1),
                          'Some files may not be parsed correctly. For a list of such files, please review the final report.',
                          'Some files may not be parsed correctly. For a list of such files, please review the final report.']

def test_findPending():   
    setup()

    output = Queue()
    findPending.start(output, 3) #2nd var doesn't do anything
    fpOut = output.get()
    fpTup = [x if type(x) is str else terminalPrintToTuple(x) if x.__class__.__name__ == 'terminalPrint' else reportIssueToTuple(x) for x in fpOut]
    assert fpTup == [(2, 'Implicit Intent: localIntent used to create instance of PendingIntent. A malicious application could potentially intercept, redirect and/or modify (in a limited manner) this Intent. Pending Intents retain the UID of your application and all related permissions, allowing another application to act as yours.  File: ./testData/goatdroid/classes_dex2jar/android/support/v4/app/TaskStackBuilder.java More details: https://www.securecoding.cert.org/confluence/display/android/DRD21-J.+Always+pass+explicit+intents+to+a+PendingIntent', {}, './testData/goatdroid/classes_dex2jar/android/support/v4/app/TaskStackBuilder.java', '', 3), ('Implicit Intent: localIntent used to create instance of PendingIntent. A malicious application could potentially intercept, redirect and/or modify (in a limited manner) this Intent. Pending Intents retain the UID of your application and all related permissions, allowing another application to act as yours.  File: ./testData/goatdroid/classes_dex2jar/android/support/v4/app/TaskStackBuilder.java More details: https://www.securecoding.cert.org/confluence/display/android/DRD21-J.+Always+pass+explicit+intents+to+a+PendingIntent', {}, 3)]



# currently doesn't turn up anything in the interactive version
def test_filePermissions():
    setup()

    output = Queue()
    height = 2
    filePermissions.start(output, height)
    a = []
    while not output.empty():
        a.append(output.get())
    assert a == [[]]

def reportIssueToTuple(aReportIssue):
    return (aReportIssue.getCategory(), aReportIssue.getDetails(), aReportIssue.getExtras(), aReportIssue.getFile(), aReportIssue.getName(), aReportIssue.getSeverity())


def terminalPrintToTuple(aTerminalPrint):
    return (aTerminalPrint.getData(), aTerminalPrint.getExtras(), aTerminalPrint.getLevel())


def test_webviews():
    setup()

    output = Queue()
    webviews.validate(output)
    output = output.get()

    outputTupsAndStrs = [x if type(x) is str else terminalPrintToTuple(x) if x.__class__.__name__ == 'terminalPrint' else reportIssueToTuple(x) for x in output]
    assert outputTupsAndStrs == [('FOUND 4 WEBVIEWS:', {}, 0), 
                                 ("['webview', './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java']", {}, 0), 
                                 ("['webview', './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java']", {}, 0), 
                                 ("['webview', './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java']", {}, 0), 
                                 ("['webview', './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java']", {}, 0), 
                                 ('WebView: webview', {}, 0), 
                                 ('File: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java\n', {}, 0), 
                                 ('JS not enabled on this webView. webview./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', {}, 0), 
                                 (8, 'BaseURL not redefined in this WebView.', {'isbaseurldefined': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', '', 0), 
                                 ('BaseURL not redefined in this WebView.', {}, 0), 
                                 (8, "File system access is enabled in this WebView. If untrusted data is used to specify the URL opened by this WebView, a malicious app or site may be able to read your app's private files, if it returns the response to them. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/FILE_SYS_WARN.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html", {'isfileaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', '', 1), 
                                 ("File system access is enabled in this WebView.webview If untrusted data is used to specify the URL opened by this WebView, a malicious app or site may be able to read your app's private files, if it returns the response to them. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/FILE_SYS_WARN.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html\n", {}, 1), 
                                 (8, 'While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access from WebViews. If the WebViews take in untrusted input, this can allow for data theft. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/WV_CPA_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html', {'iscpaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', '', 1), 
                                 ('While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access from WebViews. If the WebViews take in untrusted input, this can allow for data theft.webviewTo validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/WV_CPA_WARNING.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html\n', {}, 1), 
                                 (8, 'JavaScript running in a file scheme context can access content from any origin. This is an insecure default value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/UNIV_FILE_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html', {'isfileaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', '', 1), 
                                 ('JavaScript running in a file scheme context can access content from any origin. This is an insecure default value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions.webview To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/UNIV_FILE_WARNING.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html\n', {}, 1), 
                                 (8, 'addJavascriptInterface not used in this WebView.<br>FILE: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', {}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', '', 0), 
                                 ('addJavascriptInterface not used in this WebView.webview', {}, 0), 
                                 (8, 'DOM Storage not enabled for this WebView.<br>FILE: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', {'isdomstorageenabled': False}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/History.java', '', 0), 
                                 ('DOM Storage not enabled for this WebView.webview', {}, 0), 
                                 ('WebView: webview', {}, 0), 
                                 ('File: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java\n', {}, 0), 
                                 (8, 'While not a vulnerability by itself, it appears this app has JavaScript enabled in this WebView. If this is not expressly necessary, you should disable it, to prevent the possibility of XSS (cross-site scripting) attacks. More info: http://developer.android.com/guide/practices/security.html. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/JS_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/JS_WARNING.html', {'isjsenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', '', 1), 
                                 ('While not a vulnerability by itself, it appears this app has JavaScript enabled in this WebView: webview If this is not expressly necessary, you should disable it, to prevent the possibility of XSS (cross-site scripting) attacks. More info: http://developer.android.com/guide/practices/security.html To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/JS_WARNING.htmlNote: A local copy of this html file can also be found at <install_dir>/quark/poc/html/JS_WARNING.html\n', {}, 1), 
                                 (8, 'BaseURL not redefined in this WebView.', {'isbaseurldefined': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', '', 0), 
                                 ('BaseURL not redefined in this WebView.', {}, 0), 
                                 (8, "File system access is enabled in this WebView. If untrusted data is used to specify the URL opened by this WebView, a malicious app or site may be able to read your app's private files, if it returns the response to them. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/FILE_SYS_WARN.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html", {'isfileaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', '', 1), 
                                 ("File system access is enabled in this WebView.webview If untrusted data is used to specify the URL opened by this WebView, a malicious app or site may be able to read your app's private files, if it returns the response to them. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/FILE_SYS_WARN.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html\n", {}, 1), 
                                 (8, 'While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access from WebViews. If the WebViews take in untrusted input, this can allow for data theft. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/WV_CPA_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html', {'iscpaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', '', 1), 
                                 ('While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access from WebViews. If the WebViews take in untrusted input, this can allow for data theft.webviewTo validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/WV_CPA_WARNING.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html\n', {}, 1), 
                                 (8, 'JavaScript running in a file scheme context can access content from any origin. This is an insecure default value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/UNIV_FILE_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html', {'isfileaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', '', 1), 
                                 ('JavaScript running in a file scheme context can access content from any origin. This is an insecure default value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions.webview To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/UNIV_FILE_WARNING.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html\n', {}, 1), 
                                 (8, 'addJavascriptInterface not used in this WebView.<br>FILE: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', {}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', '', 0), 
                                 ('addJavascriptInterface not used in this WebView.webview', {}, 0), 
                                 (8, 'DOM Storage not enabled for this WebView.<br>FILE: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', {'isdomstorageenabled': False}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/activities/ViewCheckin.java', '', 0), 
                                 ('DOM Storage not enabled for this WebView.webview', {}, 0), 
                                 ('WebView: webview', {}, 0), 
                                 ('File: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java\n', {}, 0), 
                                 ('JS not enabled on this webView. webview./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', {}, 0), 
                                 (8, 'BaseURL not redefined in this WebView.', {'isbaseurldefined': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', '', 0), 
                                 ('BaseURL not redefined in this WebView.', {}, 0), 
                                 (8, "File system access is enabled in this WebView. If untrusted data is used to specify the URL opened by this WebView, a malicious app or site may be able to read your app's private files, if it returns the response to them. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/FILE_SYS_WARN.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html", {'isfileaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', '', 1), 
                                 ("File system access is enabled in this WebView.webview If untrusted data is used to specify the URL opened by this WebView, a malicious app or site may be able to read your app's private files, if it returns the response to them. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/FILE_SYS_WARN.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html\n", {}, 1), 
                                 (8, 'While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access from WebViews. If the WebViews take in untrusted input, this can allow for data theft. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/WV_CPA_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html', {'iscpaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', '', 1), 
                                 ('While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access from WebViews. If the WebViews take in untrusted input, this can allow for data theft.webviewTo validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/WV_CPA_WARNING.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html\n', {}, 1), 
                                 (8, 'JavaScript running in a file scheme context can access content from any origin. This is an insecure default value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/UNIV_FILE_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html', {'isfileaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', '', 1), 
                                 ('JavaScript running in a file scheme context can access content from any origin. This is an insecure default value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions.webview To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/UNIV_FILE_WARNING.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html\n', {}, 1), 
                                 (8, 'addJavascriptInterface not used in this WebView.<br>FILE: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', {}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', '', 0), 
                                 ('addJavascriptInterface not used in this WebView.webview', {}, 0), 
                                 (8, 'DOM Storage not enabled for this WebView.<br>FILE: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', {'isdomstorageenabled': False}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryDialogFragment.java', '', 0), 
                                 ('DOM Storage not enabled for this WebView.webview', {}, 0), 
                                 ('WebView: webview', {}, 0), 
                                 ('File: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java\n', {}, 0), 
                                 (8, 'While not a vulnerability by itself, it appears this app has JavaScript enabled in this WebView. If this is not expressly necessary, you should disable it, to prevent the possibility of XSS (cross-site scripting) attacks. More info: http://developer.android.com/guide/practices/security.html. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/JS_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/JS_WARNING.html', {'isjsenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', '', 1), 
                                 ('While not a vulnerability by itself, it appears this app has JavaScript enabled in this WebView: webview If this is not expressly necessary, you should disable it, to prevent the possibility of XSS (cross-site scripting) attacks. More info: http://developer.android.com/guide/practices/security.html To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/JS_WARNING.htmlNote: A local copy of this html file can also be found at <install_dir>/quark/poc/html/JS_WARNING.html\n', {}, 1), 
                                 (8, 'BaseURL not redefined in this WebView.', {'isbaseurldefined': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', '', 0), 
                                 ('BaseURL not redefined in this WebView.', {}, 0), 
                                 (8, "File system access is enabled in this WebView. If untrusted data is used to specify the URL opened by this WebView, a malicious app or site may be able to read your app's private files, if it returns the response to them. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/FILE_SYS_WARN.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html", {'isfileaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', '', 1), 
                                 ("File system access is enabled in this WebView.webview If untrusted data is used to specify the URL opened by this WebView, a malicious app or site may be able to read your app's private files, if it returns the response to them. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/FILE_SYS_WARN.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/FILE_SYS_WARN.html\n", {}, 1), 
                                 (8, 'While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access from WebViews. If the WebViews take in untrusted input, this can allow for data theft. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/WV_CPA_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html', {'iscpaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', '', 1), 
                                 ('While not a vulnerability by itself, it appears this app does not explicitly disable Content Provider access from WebViews. If the WebViews take in untrusted input, this can allow for data theft.webviewTo validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/WV_CPA_WARNING.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/WV_CPA_WARNING.html\n', {}, 1), 
                                 (8, 'JavaScript running in a file scheme context can access content from any origin. This is an insecure default value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions. To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/qark/poc/UNIV_FILE_WARNING.html. Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html', {'isfileaccessenabled': True}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', '', 1), 
                                 ('JavaScript running in a file scheme context can access content from any origin. This is an insecure default value for minSdkVersion < 16 or may have been overridden (setAllowUniversalAccessFromFileURLs) in later versions.webview To validate this vulnerability, load the following url in this WebView: http://www.secbro.com/poc/html/UNIV_FILE_WARNING.html Note: A local copy of this html file can also be found at <install_dir>/quark/poc/html/UNIV_FILE_WARNING.html\n', {}, 1), 
                                 (8, 'addJavascriptInterface not used in this WebView.<br>FILE: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', {}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', '', 0), 
                                 ('addJavascriptInterface not used in this WebView.webview', {}, 0), 
                                 (8, 'DOM Storage not enabled for this WebView.<br>FILE: ./testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', {'isdomstorageenabled': False}, './testData/goatdroid/classes_dex2jar/org/owasp/goatdroid/fourgoats/fragments/HistoryFragment.java', '', 0), 
                                 ('DOM Storage not enabled for this WebView.webview', {}, 0)]

def test_cryptoFlaws():
    setup()

    output = Queue()
    cryptoFlaws.main(output)
    output = output.get()
    assert output == []


def test_findBroadcasts():
    setup()

    output = Queue()
    findBroadcasts.main(output) #2nd var doesn't do anything
    fbOut = output.get()
    assert fbOut == []