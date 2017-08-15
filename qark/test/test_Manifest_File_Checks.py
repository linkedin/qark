from plugins import PluginUtil
from plugins.Manifest_File_Checks import ManifestFilePlugin

plugin = ManifestFilePlugin()


def test_regex():
    assert PluginUtil.contains(plugin.PATH_USAGE, 'android:path=')


def test_regex1():
    assert not PluginUtil.contains(plugin.PATH_USAGE, 'android:pathPrefix=')


def test_regex2():
    assert not PluginUtil.contains(plugin.PATH_USAGE, 'android:pathPattern')


def test_regex3():
    text = "android:launchMode='singleTask'"
    assert PluginUtil.contains(plugin.LAUNCH_MODE, text)


def test_regex4():
    text = 'android:launchMode="singleTask"'
    assert PluginUtil.contains(plugin.LAUNCH_MODE, text)


def test_regex5():
    text = "android:allowTaskReparenting='true'"
    assert PluginUtil.contains(plugin.TASK_REPARENTING, text)


def test_regex6():
    text = 'android:allowTaskReparenting="true"'
    assert PluginUtil.contains(plugin.TASK_REPARENTING, text)


def test_regex7():
    text = '<receiver android:name=".FormatOutgoingCallReceiver" android:enabled="true" android:exported="false">'
    assert PluginUtil.contains(plugin.RECEIVER_REGEX, text)


def test_regex8():
    text = '<receiver android:name=".FormatOutgoingCallReceiver" android:enabled="true" android:exported="true"'
    assert not PluginUtil.contains(plugin.RECEIVER_REGEX, text)


def test_regex11():
    text = 'Priority'
    assert not PluginUtil.contains(plugin.PRIORITY_REGEX, text)


def test_regex12():
    text = 'priority'
    assert PluginUtil.contains(plugin.PRIORITY_REGEX, text)


def test_regex13():
    text = '<meta-data android:name="com.google.android.geo.API_KEY" android:value="AIzaSyBdVl-cTICSwYKrZ95SuvNw7dbMuDt1KG0"/>'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex14():
    text = '<meta-data android:name="com.google.android.geo.api_key" android:value="AIzaSyBdVl-cTICSwYKrZ95SuvNw7dbMuDt1KG0"/>'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex15():
    text = '<meta-data android:name="com.google.android.geo.apiKey" android:value="AIzaSyBdVl-cTICSwYKrZ95SuvNw7dbMuDt1KG0"/>'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex16():
    text = '<meta-data android:name="com.google.android.geo" android:value="AIzaSyBdVl-cTICSwYKrZ95SuvNw7dbMuDt1KG0'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex17():
    text = '<meta-data android:name="com.google.android.geo" android:value="AIzaSy-cKG0"/>'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex18():
    text = '<string name="google_crash_reporting_api_key">ASy34FDEgGSh34sWbRTE53bSG5c</string>'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex19():
    text = '<meta-data android:name="com.google.android.geo" android:value="AI#%$zaSy-cK+_^%$G"/>'
    assert not PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex20():
    text = '<meta-data android:name="com.google.android.geo" android:value="a1234567890"/>'
    assert not PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex21():
    text = '<path-permission android:path="/" android:readPermission="com.xyz.example.READ_KEYS" android:writePermission="com.xyz.example.WRITE_KEYS"/>'
    assert not PluginUtil.contains(plugin.HARDCODED_API_KEY, text)


def test_regex22():
    text = '<meta-data android:name="com.google.android.geo.API_KEY" android:value="AIzaSyBdVl-cTICSwYKrZ95SuvNw7dbMuDt1KG0"/>'
    assert PluginUtil.contains(plugin.HARDCODED_API_KEY, text)


def test_regex23():
    text = '<meta-data android:name="com.google.android.geo" android:value="AI#%$zaSy-cK+_^%$G"/>'
    assert PluginUtil.contains(plugin.SPECIAL_CHAR_REGEX, text)


def test_regex24():
    text = '<meta-data android:name="com.google.android.geo.API_KEY" android:value="AIzaSyBdVl-cTICSwYKrZ95SuvNw7dbMuDt1KG0"/'
    assert not PluginUtil.contains(plugin.SPECIAL_CHAR_REGEX, text)


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
    test_regex13()
    test_regex14()
    test_regex15()
    test_regex16()
    test_regex17()
    test_regex18()
    test_regex19()
    test_regex20()
    test_regex21()
    test_regex22()
    test_regex23()
    test_regex24()
