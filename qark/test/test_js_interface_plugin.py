from plugins import PluginUtil
from plugins.js_interface_plugin import JsInterfacePlugin

plugin = JsInterfacePlugin()


def testWebViewRegex():
    assert PluginUtil.contains(plugin.webViewRegex, 'import android.webkit.WebView') is True


def testInlineWithPackageName():
    text = 'new android.webkit.WebView().addJavascriptInterface();'
    assert PluginUtil.contains(plugin.inlineRegex, text) is True


def testInlineWithoutPackageName():
    text = 'new WebView().addJavascriptInterface();'
    assert PluginUtil.contains(plugin.inlineRegex, text) is True


def testGetVarNameWithPackageName():
    text = 'android.webkit.WebView webView;'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'webView'


def testGetVarNameWithoutPackageName():
    text = 'WebView webView;'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'webView'


def testGetVarNameMiddleArgument():
    text = 'void func(int i, WebView webView, int j)'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'webView'


def testGetVarNameLastArgument():
    text = 'void func(int i, WebView webView)'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'webView'


def testGetVarNameInstantiation():
    text = 'WebView webView = new WebView(context);'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'webView'


if __name__ == '__main__':
    testWebViewRegex()
    testInlineWithPackageName()
    testInlineWithoutPackageName()
    testGetVarNameWithPackageName()
    testGetVarNameWithoutPackageName()
    testGetVarNameMiddleArgument()
    testGetVarNameLastArgument()
    testGetVarNameInstantiation()
