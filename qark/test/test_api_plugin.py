from plugins import PluginUtil
from plugins.api_plugin import HardcodedAPIIssuesPlugin

plugin = HardcodedAPIIssuesPlugin()


def test_regex1():
    text = 'public static final String API_TOKEN = "Nti4kWY-qRHTYq3dsbeip0P1tbGCzs2BAY163ManCAb"'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex2():
    text = '"NtY163ManCAb"'
    assert not PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex3():
    text = 'public static final = "Nti4kWY-qRHTYq3dsbeip0P1tbGCzs2BAY163ManCAb"'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex4():
    text = 'public static final String API_TOKEN = "1234thisisaninvalidapitoken937235"'
    assert PluginUtil.contains(plugin.API_KEY_REGEX, text)


def test_regex5():
    text = 'public static final String API_TOKEN = "$%#%~!^"'
    assert PluginUtil.contains(plugin.SPECIAL_CHAR_REGEX, text)


if __name__ == '__main__':
    test_regex1()
    test_regex2()
    test_regex3()
    test_regex4()
    test_regex5()
