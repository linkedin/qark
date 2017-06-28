from plugins import PluginUtil
from plugins.Dynamically_Loading_Code import DynamicallyLoadingCodePlugin

plugin = DynamicallyLoadingCodePlugin()

def testuri_regex():
    assert PluginUtil.contains(plugin.dex_class_loader, 'DexClassLoader') is True

def testuri_regex1():
    assert PluginUtil.contains(plugin.dex_class_loader, 'ClassLoader') is False

def testuri_regex2():
    assert PluginUtil.contains(plugin.class_loader, 'loadClass') is True

def testuri_regex3():
    assert PluginUtil.contains(plugin.class_loader, 'Classload') is False

if __name__ == '__main__':
    testuri_regex()
    testuri_regex1()
    testuri_regex2()
    testuri_regex3()