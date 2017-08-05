from plugins import PluginUtil
from plugins.external_storage import ExternalStorageCheckPlugin

plugin = ExternalStorageCheckPlugin()


def test_regex():
    assert PluginUtil.contains(plugin.CHECK_EXTERNAL_STORAGE, 'getExternalFilesDir')


def test_regex1():
    assert not PluginUtil.contains(plugin.CHECK_EXTERNAL_STORAGE, 'GetExternalFilesDir')


def test_regex2():
    assert PluginUtil.contains(plugin.CHECK_EXTERNAL_MEDIA, 'getExternalMediaDirs')


def test_regex3():
    assert not PluginUtil.contains(plugin.CHECK_EXTERNAL_MEDIA, 'GetExternalMediaDirs')


def test_regex4():
    assert PluginUtil.contains(plugin.CHECK_PUBLIC_DIR, 'getExternalStoragePublicDirectory')


def test_regex5():
    assert not PluginUtil.contains(plugin.CHECK_PUBLIC_DIR, 'GetExternalStoragePublicDirectory')


if __name__ == '__main__':
    test_regex()
    test_regex1()
    test_regex2()
    test_regex3()
    test_regex4()
    test_regex5()