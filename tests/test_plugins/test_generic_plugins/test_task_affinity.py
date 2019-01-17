from qark.plugins.generic.task_affinity import TaskAffinity

import os

def test_task_affinity(test_java_files):
    plugin = TaskAffinity()
    path = os.path.join(test_java_files,
                        "task_affinity.java")
    plugin.update(file_path=path)
    plugin.run()
    assert 1 == len(plugin.issues)
