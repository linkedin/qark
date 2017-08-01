from plugins import PluginUtil
from plugins.logging_plugin import LoggingIssuesPlugin

plugin = LoggingIssuesPlugin()

def testlog_regex():
    assert PluginUtil.contains(plugin.debug_regex, 'Log.d') is True

def testlog_regex1():
    assert PluginUtil.contains(plugin.debug_regex, 'd') is False

def testlog_regex2():
    assert PluginUtil.contains(plugin.verbose_regex, 'Log.v') is True

def testlog_regex3():
    assert PluginUtil.contains(plugin.verbose_regex, 'v') is False

if __name__ == '__main__':
    testlog_regex()
    testlog_regex1()
    testlog_regex2()
    testlog_regex3()