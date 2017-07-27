from plugins import PluginUtil
from plugins.access_control import AccessControlCheckPlugin

plugin = AccessControlCheckPlugin()

def test_check_perm_regex():
    assert PluginUtil.contains(plugin.CHECK_PERMISSION, 'checkCallingOrSelfPermission') is True

def test_check_perm_regex1():
    assert PluginUtil.contains(plugin.CHECK_PERMISSION, 'checkCallingOrSelfUriPermission') is True

def test_check_perm_regex2():
    assert PluginUtil.contains(plugin.CHECK_PERMISSION, 'checkPermission') is True

def test_check_perm_regex3():
    assert PluginUtil.contains(plugin.CHECK_PERMISSION, 'checkCallingPermission') is False

def test_check_perm_regex4():
    assert PluginUtil.contains(plugin.CHECK_PERMISSION, 'check_Permission') is False

def test_check_perm_regex5():
    assert PluginUtil.contains(plugin.CHECK_PERMISSION, 'CheckPermission') is False

def test_check_perm_regex6():
    assert PluginUtil.contains(plugin.CHECK_PERMISSION, 'checkCalling') is False

def test_check_perm_regex7():
    assert PluginUtil.contains(plugin.CHECK_PERMISSION, 'SelfUriPermission') is False

def test_enforce_perm_regex():
    text = 'enforceCallingOrSelfPermission'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is True

def test_enforce_perm_regex1():
    text = 'enforceCallingOrSelfUriPermission'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is True

def test_enforce_perm_regex2():
    text = 'enforcePermission'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is True

def test_enforce_perm_regex3():
    text = 'EnforceCallingOrSelfPermission'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is False

def test_enforce_perm_regex4():
    text = 'enforceCalling'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is False

def test_enforce_perm_regex5():
    text = 'enforceCallingOrSelfPermission("santos.benign.permission","Not allowed to start MyService")'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is True

def test_enforce_perm_regex6():
    text = 'enforceCallingPermission'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is False

def test_enforce_perm_regex7():
    text = 'enforceCallingOrSelfUriPermission("santos.benign.permission","Not allowed to start MyService")'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is True

def test_enforce_perm_regex8():
    text = 'enforcePermission("santos.benign.permission","Not allowed to start MyService")'
    assert PluginUtil.contains(plugin.ENFORCE_PERMISSION, text) is True


if __name__ == '__main__':
    test_check_perm_regex()
    test_check_perm_regex1()
    test_check_perm_regex2()
    test_check_perm_regex3()
    test_check_perm_regex4()
    test_check_perm_regex5()
    test_check_perm_regex6()
    test_check_perm_regex7()
    test_enforce_perm_regex()
    test_enforce_perm_regex1()
    test_enforce_perm_regex2()
    test_enforce_perm_regex3()
    test_enforce_perm_regex4()
    test_enforce_perm_regex5()
    test_enforce_perm_regex6()
    test_enforce_perm_regex7()
    test_enforce_perm_regex8()
