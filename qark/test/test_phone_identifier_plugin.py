from plugins import PluginUtil
from plugins.phone_identifier_plugin import PhoneIdentifierPlugin

plugin = PhoneIdentifierPlugin()


def testTelephonyManagerRegex():
    assert PluginUtil.contains(plugin.telephonyManagerRegex, 'import android.telephony.TelephonyManager') is True


def testInlineWithPackageName():
    text = '((android.telephony.TelephonyManager)paramContext.getSystemService("phone")).getLine1Number();'
    assert PluginUtil.contains(plugin.inlineRegex, text) is True


def testInlineWithoutPackageName():
    text = '((TelephonyManager)paramContext.getSystemService("phone")).getLine1Number();'
    assert PluginUtil.contains(plugin.inlineRegex, text) is True


def testInlineGetDeviceId():
    text = '((android.telephony.TelephonyManager)paramContext.getSystemService("phone")).getDeviceId();'
    assert PluginUtil.contains(plugin.inlineRegex, text) is True


def testGetVarNameWithPackageName():
    text = 'android.telephony.TelephonyManager paramContext;'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'paramContext'


def testGetVarNameWithoutPackageName():
    text = 'TelephonyManager paramContext;'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'paramContext'


def testGetVarNameMiddleArgument():
    text = 'void func(int i, TelephonyManager paramContext, int j)'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'paramContext'


def testGetVarNameLastArgument():
    text = 'void func(int i, TelephonyManager paramContext)'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'paramContext'


def testGetVarNameInstantiation():
    text = 'TelephonyManager paramContext = (TelephonyManager)paramContext.getSystemService("phone"));'
    res = PluginUtil.returnGroupMatches(plugin.varNameRegex, 2, text)
    assert len(res) == 1
    assert res[0] == 'paramContext'


if __name__ == '__main__':
    testTelephonyManagerRegex()
    testInlineWithPackageName()
    testInlineWithoutPackageName()
    testInlineGetDeviceId()
    testGetVarNameWithPackageName()
    testGetVarNameWithoutPackageName()
    testGetVarNameMiddleArgument()
    testGetVarNameLastArgument()
    testGetVarNameInstantiation()
