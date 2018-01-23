import os

from qark.plugins.crypto.ecb_cipher_usage import ECBCipherCheck
from qark.plugins.crypto.packaged_private_keys import PackagedPrivateKeys
from qark.plugins.crypto.setting_secure_random_seed import SeedWithSecureRandom

curr_dir = os.path.dirname(__file__)
java_dir = os.path.join(curr_dir, 'java_files')


def test_blank_file():
    files = ('invalid.java', 'blank.java')
    files = tuple([os.path.join(java_dir, file) for file in files])
    plugins = (SeedWithSecureRandom(), ECBCipherCheck(), PackagedPrivateKeys())
    for plugin in plugins:
        for file in files:
            plugin.run(file)
        assert plugin.issues == []


def test_seeding_secure_random():
    no_bug_files = ['secure_random_no_args1.java']
    buggy_files = ['secure_random_args1.java', 'secure_random_args1.java']
    plugin = SeedWithSecureRandom()
    for curr_file in no_bug_files:
        curr_file = os.path.join(java_dir, curr_file)
        plugin.run([curr_file])
        assert not plugin.issues
    for i, curr_file in enumerate(buggy_files):
        curr_file = os.path.join(java_dir, curr_file)
        assert len(plugin.issues) == i
        plugin.run([curr_file])
        assert len(plugin.issues) == i + 1


def test_packaged_private_keys():
    key_dir = os.path.join(curr_dir, 'keys')
    plugin = PackagedPrivateKeys()
    assert len(plugin.issues) == 0
    private_key_files = ['rsa-key', 'dsa-key', 'ed25519-key', 'ecdsa-key']
    for i, file_path in enumerate(private_key_files):
        absolute_path = os.path.join(key_dir, file_path)
        assert len(plugin.issues) == i
        plugin.run([absolute_path])
        assert len(plugin.issues) == i + 1
    public_key_files = [path + '.pub' for path in private_key_files]
    num_issues = len(plugin.issues)
    for file_path in public_key_files:
        plugin.run([file_path])
        assert len(plugin.issues) == num_issues
