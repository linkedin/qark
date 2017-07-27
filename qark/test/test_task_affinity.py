from plugins import PluginUtil
from plugins.task_affinity import TaskAffinityPlugin

plugin = TaskAffinityPlugin()

def test_regex():
    text ='intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);'
    assert PluginUtil.contains(plugin.NEW_TASK, text) is True

def test_regex1():
    text = 'intent.setFlags(Intent.FLAGACTIVITYNEWTASK);'
    assert PluginUtil.contains(plugin.NEW_TASK, text) is False

def test_regex2():
    text = 'intent.setFlags(Intent.FLAG_ACTIVITY_MULTIPLE_TASK);'
    assert PluginUtil.contains(plugin.NEW_TASK, text) is False

def test_regex3():
    text = 'intent.setFlags(Intent.FLAG_ACTIVITY_MULTIPLE_TASK);'
    assert PluginUtil.contains(plugin.MULTIPLE_TASK, text) is True

def test_regex4():
    text = 'intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);'
    assert PluginUtil.contains(plugin.MULTIPLE_TASK, text) is False

def test_regex5():
    text = 'intent.setFlags(Intent.FLAG_ACTIVITY_MULTIPLE_TASK);'
    assert PluginUtil.contains(plugin.MULTIPLE_TASK, text) is False



if __name__ == '__main__':
    test_regex()
    test_regex1()
    test_regex2()
    test_regex3()
    test_regex4()
    test_regex5()