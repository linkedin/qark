import os

from qark.plugins.crypto.ecb_cipher_usage import ECBCipherCheck

curr_dir = os.path.dirname(__file__)
java_dir = os.path.join(curr_dir, 'java_files')


def test_non_existent_file():
    """The scan should not throw exceptions on a non-existent file"""
    plugin = ECBCipherCheck()
    non_existent_files = ['----']
    try:
        plugin.run(non_existent_files)
    except Exception:
        assert False


def test_ecb_cipher_usage():
    plugin = ECBCipherCheck()
    files_with_ecb = ['ecb1.java', 'ecb2.java']
    files_without_ecb = ['blank.java', 'no_ecb1.java']

    for file in files_without_ecb:
        file = os.path.join(java_dir, file)
        plugin.run([file])
    assert not plugin.issues
    for i, file in enumerate(files_with_ecb):
        file = os.path.join(java_dir, file)
        assert len(plugin.issues) == i
        plugin.run([file])
        assert len(plugin.issues) == i + 1
