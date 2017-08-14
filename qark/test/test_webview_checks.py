from plugins import PluginUtil
from plugins.webview_checks import WebViewChecksPlugin

plugin = WebViewChecksPlugin()

def test_regex1():
    text = 'setJavaScriptEnabled(false)'
    assert not PluginUtil.contains(plugin.JAVASCRIPT_ENABLED, text)

def test_regex2():
    text = 'setJavaScriptEnabled(true)'
    assert PluginUtil.contains(plugin.JAVASCRIPT_ENABLED, text)

def test_regex3():
    text = 'loadUrl("https:'
    assert not PluginUtil.contains(plugin.LOAD_URL_HTTP, text)

def test_regex4():
    text = 'loadUrl("http:'
    assert PluginUtil.contains(plugin.LOAD_URL_HTTP, text)

def test_regex5():
    text = 'setMixedContentMode'
    assert PluginUtil.contains(plugin.MIXED_CONTENT, text)

def test_regex6():
    text = 'SetMixedContentMode'
    assert not PluginUtil.contains(plugin.MIXED_CONTENT, text)

def test_regex7():
    text = "loadUrl('https:"
    assert not PluginUtil.contains(plugin.LOAD_URL_HTTP, text)

def test_regex8():
    text = "loadUrl('http:"
    assert PluginUtil.contains(plugin.LOAD_URL_HTTP, text)


if __name__ == '__main__':
    test_regex1()
    test_regex2()
    test_regex3()
    test_regex4()
    test_regex5()
    test_regex6()
    test_regex7()
    test_regex8()