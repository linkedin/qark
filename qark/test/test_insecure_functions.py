from plugins import PluginUtil
from plugins.insecure_functions import InsecureFunctionsPlugin

plugin = InsecureFunctionsPlugin()

def test_regex():
    text = 'call'
    assert PluginUtil.contains(plugin.CALL_FUNCTION, text)

def test_regex1():
    text = 'call(String method, String args, Bundle extras)'
    assert PluginUtil.contains(plugin.CALL_FUNCTION, text)

def test_regex2():
    text = 'call()'
    assert PluginUtil.contains(plugin.CALL_FUNCTION, text)

if __name__ == '__main__':
    test_regex()
    test_regex1()
    test_regex2()