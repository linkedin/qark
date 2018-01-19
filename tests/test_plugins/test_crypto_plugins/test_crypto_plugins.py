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
    for file in no_bug_files:
        file = os.path.join(java_dir, file)
        plugin.run(file)
        assert not plugin.issues
    for i, file in enumerate(buggy_files):
        file = os.path.join(java_dir, file)
        assert len(plugin.issues) == i
        plugin.run(file)
        assert len(plugin.issues) == i + 1



def test_ecb_cipher_usage():
    plugin = ECBCipherCheck()


def test_packaged_private_keys():
    key_dir = os.path.join(curr_dir, 'keys')
    plugin = PackagedPrivateKeys()
    assert len(plugin.issues) is 0
    private_key_files = ['rsa-key', 'dsa-key', 'ed25519-key', 'ecdsa-key']
    for i, file in enumerate(private_key_files):
        absolute_path = os.path.join(key_dir, file)
        assert len(plugin.issues) == i
        plugin.run(absolute_path)
        assert len(plugin.issues) == i + 1
    public_key_files = [path + '.pub' for path in private_key_files]
    num_issues = len(plugin.issues)
    for file in public_key_files:
        plugin.run(file)
        assert len(plugin.issues) == num_issues

