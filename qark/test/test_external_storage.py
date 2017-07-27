from plugins import PluginUtil
from plugins.external_storage import ExternalStorageCheckPlugin

plugin = ExternalStorageCheckPlugin()


def test_regex():
    assert PluginUtil.contains(plugin.CHECK_EXTERNAL_STORAGE, 'getExternalFilesDir') is True


def test_regex1():
    assert PluginUtil.contains(plugin.CHECK_EXTERNAL_STORAGE, 'GetExternalFilesDir') is False


def test_regex2():
    assert PluginUtil.contains(plugin.CHECK_EXTERNAL_MEDIA, 'getExternalMediaDirs') is True


def test_regex3():
    assert PluginUtil.contains(plugin.CHECK_EXTERNAL_MEDIA, 'GetExternalMediaDirs') is False


def test_regex4():
    assert PluginUtil.contains(plugin.CHECK_PUBLIC_DIR, 'getExternalStoragePublicDirectory') is True


def test_regex5():
    assert PluginUtil.contains(plugin.CHECK_PUBLIC_DIR, 'GetExternalStoragePublicDirectory') is False


if __name__ == '__main__':
    test_regex()
    test_regex1()
    test_regex2()
    test_regex3()
    test_regex4()
    test_regex5()