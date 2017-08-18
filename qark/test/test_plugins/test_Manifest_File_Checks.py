from plugins import PluginUtil
from plugins.Manifest_File_Checks import ManifestFilePlugin

plugin = ManifestFilePlugin()

def test_regex():
    assert PluginUtil.contains(plugin.PATH_USAGE, 'android:path=') is True

def test_regex1():
    assert PluginUtil.contains(plugin.PATH_USAGE, 'android:pathPrefix=') is False

def test_regex2():
    assert PluginUtil.contains(plugin.PATH_USAGE, 'android:pathPattern') is False

def test_regex3():
    text = "android:launchMode='singleTask'"
    assert PluginUtil.contains(plugin.LAUNCH_MODE, text) is True

def test_regex4():
    text = 'android:launchMode="singleTask"'
    assert PluginUtil.contains(plugin.LAUNCH_MODE, text) is True

def test_regex5():
    text = "android:allowTaskReparenting='true'"
    assert PluginUtil.contains(plugin.TASK_REPARENTING, text) is True

def test_regex6():
    text = 'android:allowTaskReparenting="true"'
    assert PluginUtil.contains(plugin.TASK_REPARENTING, text) is True

def test_regex7():
    text = '<receiver android:name=".FormatOutgoingCallReceiver" android:enabled="true" android:exported="false">'
    assert PluginUtil.contains(plugin.RECEIVER_REGEX, text) is True

def test_regex8():
    text = '<receiver android:name=".FormatOutgoingCallReceiver" android:enabled="true" android:exported="true"'
    assert PluginUtil.contains(plugin.RECEIVER_REGEX, text) is False


def test_regex11():
    text = 'Priority'
    assert PluginUtil.contains(plugin.PRIORITY_REGEX, text) is False

def test_regex12():
    text = 'priority'
    assert PluginUtil.contains(plugin.PRIORITY_REGEX, text) is True


if __name__ == '__main__':
    test_regex()
    test_regex1()
    test_regex2()
    test_regex3()
    test_regex4()
    test_regex5()
    test_regex6()
    test_regex7()
    test_regex8()
    test_regex11()
    test_regex12()