from plugins import PluginUtil
from plugins.http_url_hardcoded import HardcodedHTTPUrl

plugin = HardcodedHTTPUrl()

def testuri_regex():
    assert PluginUtil.contains(plugin.http_url_regex, 'http://stackoverflow.com/questions') is True

def testuri_regex1():
    assert PluginUtil.contains(plugin.http_url_regex, 'http://www.linkedin.com/') is True

def testuri_regex2():
    assert PluginUtil.contains(plugin.http_url_regex, 'www.xyz.in') is False

def testuri_regex3():
    assert PluginUtil.contains(plugin.http_url_regex, 'https://www.linkedin.com/') is False

def testuri_regex4():
    assert PluginUtil.contains(plugin.http_url_regex, 'HTTP://www.linkedin.com/') is False

def testuri_regex5():
    assert PluginUtil.contains(plugin.http_url_regex, 'http://example.com/') is True

def testuri_regex6():
    assert PluginUtil.contains(plugin.http_url_regex, '(http|https)://www.linkedin.com/profile/view[?]id=([^&]+)') is False

if __name__ == '__main__':
    testuri_regex()
    testuri_regex1()
    testuri_regex2()
    testuri_regex3()
    testuri_regex4()
    testuri_regex5()
    testuri_regex6()
