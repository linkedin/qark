from plugins import PluginUtil
from plugins.Dynamically_Loading_Code import DynamicallyLoadingCodePlugin

plugin = DynamicallyLoadingCodePlugin()

def test_regex():
    assert PluginUtil.contains(plugin.DEX_CLASS_LOADER, 'DexClassLoader') is True

def test_regex1():
    assert PluginUtil.contains(plugin.DEX_CLASS_LOADER, 'ClassLoader') is False

def test_regex2():
    assert PluginUtil.contains(plugin.CLASS_LOADER, 'loadClass') is True

def test_regex3():
    assert PluginUtil.contains(plugin.CLASS_LOADER, 'Classload') is False

def test_regex4():
    assert PluginUtil.contains(plugin.DYNAMIC_BROADCAST_RECEIVER, 'registerReceiver') is True

def test_regex5():
    assert PluginUtil.contains(plugin.DYNAMIC_BROADCAST_RECEIVER, 'RegisterReceiver') is False



if __name__ == '__main__':
    test_regex()
    test_regex1()
    test_regex2()
    test_regex3()
    test_regex4()
    test_regex5()