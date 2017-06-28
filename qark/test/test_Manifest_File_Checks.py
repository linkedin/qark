from plugins import PluginUtil
from plugins.Manifest_File_Checks import ManifestFilePlugin

plugin = ManifestFilePlugin()

def testuri_regex():
    assert PluginUtil.contains(plugin.uri_regex, 'android:path="/"') is True

def testuri_regex1():
    assert PluginUtil.contains(plugin.uri1_regex, 'android:pathPrefix="/"') is True

def testuri_regex2():
    assert PluginUtil.contains(plugin.uri1_regex, 'android:pathPrefix="/Keys"') is False


def test_permission1():
    text = '<provider android:authorities="com.mwr.example.sieve.DBContentProvider" android:exported="true" android:multiprocess="true" android:name=".DBContentProvider">'
    assert PluginUtil.contains(plugin.permission_regex1, text) is False

def test_permission2():
    text = '<path-permission android:path="/Keys" android:readPermission="com.mwr.example.sieve.READ_KEYS" android:writePermission="com.mwr.example.sieve.WRITE_KEYS"/>'
    assert PluginUtil.contains(plugin.permission_regex2, text) is True

if __name__ == '__main__':
    testuri_regex()
    testuri_regex1()
    testuri_regex2()
    test_permission1()
    test_permission2()