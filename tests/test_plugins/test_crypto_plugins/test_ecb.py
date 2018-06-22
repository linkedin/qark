import os

import javalang

from qark.plugins.crypto.ecb_cipher_usage import ECBCipherCheck

curr_dir = os.path.dirname(__file__)
java_dir = os.path.join(curr_dir, 'java_files')


def test_ecb_cipher_usage():
    plugin = ECBCipherCheck()
    files_with_ecb = ['ecb1.java', 'ecb2.java']
    files_without_ecb = ['no_ecb1.java']

    for file in files_without_ecb:
        file = os.path.join(java_dir, file)
        plugin.update(file_path=file)
        plugin.run()

    assert not plugin.issues

    plugin.reset()

    for i, file in enumerate(files_with_ecb):
        file = os.path.join(java_dir, file)
        plugin.update(file_path=file)
        assert len(plugin.issues) == i
        plugin.run()
        assert len(plugin.issues) == i + 1
