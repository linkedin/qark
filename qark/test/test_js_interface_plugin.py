from plugins.js_interface_plugin import JsInterfacePlugin

manifest_loc = './fixtures/decompiledFile'
jsInterfacePlugin = JsInterfacePlugin()


def testGetWebViewArgNames():
    fileBody = 'void test(WebView webView) {}\n ' \
               'void test2(WebView w, Class a) {}\n ' \
               'void test3(android.webkit.WebView w2)'
    names = jsInterfacePlugin.getWebViewArgNames(fileBody)
    assert len(names) == 3
    assert names[0] == 'webView'
    assert names[1] == 'w'
    assert names[2] == 'w2'


def testGetWebViewDeclNames():
    fileBody = 'String a = ""; WebView w; android.webkit.WebView w2; WebView w3 = new WebView();'
    names = jsInterfacePlugin.getWebViewDeclarationNames(fileBody)
    assert len(names) == 3
    assert names[0] == 'w'
    assert names[1] == 'w2'
    assert names[2] == 'w3'


def testContainsInlineJavascriptInterfaceCall():
    fileBody1 = 'new WebView(c).addJavascriptInterface(d)'
    fileBody2 = 'new android.webkit.WebView(c).addJavascriptInterface(d)'
    assert jsInterfacePlugin.containsInlineJavascriptInterfaceCall(fileBody1) is True
    assert jsInterfacePlugin.containsInlineJavascriptInterfaceCall(fileBody2) is True


def testDoesNotContainInlineJavascriptInterfaceCall():
    fileBody1 = 'new WebView(c).method(d)'
    fileBody2 = 'new android.webkit.WebView(c).method(d)'
    assert jsInterfacePlugin.containsInlineJavascriptInterfaceCall(fileBody1) is False
    assert jsInterfacePlugin.containsInlineJavascriptInterfaceCall(fileBody2) is False


def testContainsJavascriptInterfaceCall():
    fileBody = 'webView.addJavascriptInterface(d)'
    assert jsInterfacePlugin.containsJavascriptInterfaceCall(fileBody, 'webView') is True


def testDoesNotContainWebViewNameInJavascriptInterfaceCall():
    fileBody = 'WebView localWebView = new WebView(paramContext);\n' \
               'localWebView.addJavascriptInterface(new JsObject(null), "name");\n' \
               'System.out.println(localWebView.getOriginalUrl());'
    b = jsInterfacePlugin.containsJavascriptInterfaceCall(fileBody, 'local')
    assert b is False


if __name__ == '__main__':
    testGetWebViewArgNames()
    testGetWebViewDeclNames()
    testContainsInlineJavascriptInterfaceCall()
    testDoesNotContainInlineJavascriptInterfaceCall()
    testContainsJavascriptInterfaceCall()
    testDoesNotContainWebViewNameInJavascriptInterfaceCall()
