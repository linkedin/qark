import os

from qark.plugins.crypto.ecb_cipher_usage import ECBCipherCheck
from qark.plugins.crypto.packaged_private_keys import PackagedPrivateKeys
from qark.plugins.crypto.setting_secure_random_seed import SeedWithSecureRandom

import javalang

curr_dir = os.path.dirname(__file__)
java_dir = os.path.join(curr_dir, 'java_files')


def test_blank_file():
    files = ('invalid.java', 'blank.java')
    files = tuple([os.path.join(java_dir, file) for file in files])
    plugins = (SeedWithSecureRandom(), ECBCipherCheck(), PackagedPrivateKeys())
    for plugin in plugins:
        for file in files:
            with open(file) as f:
                contents = f.read()
                try:
                    ast = javalang.parse.parse(contents)
                except javalang.parser.JavaSyntaxError:
                    ast = None

            plugin.run(file, java_ast=ast, file_contents=contents)
        assert plugin.issues == []


def test_seeding_secure_random():
    no_bug_files = ['secure_random_no_args1.java']
    buggy_files = ['secure_random_args1.java', 'secure_random_args2.java']
    plugin = SeedWithSecureRandom()
    for curr_file in no_bug_files:
        curr_file = os.path.join(java_dir, curr_file)

        with open(curr_file) as f:
            ast = javalang.parse.parse(f.read())

        plugin.run(curr_file, java_ast=ast)
        assert not plugin.issues

    for i, curr_file in enumerate(buggy_files):
        curr_file = os.path.join(java_dir, curr_file)

        with open(curr_file) as f:
            ast = javalang.parse.parse(f.read())

        assert i == len(plugin.issues)
        plugin.run(curr_file, java_ast=ast)
        assert i + 1 == len(plugin.issues)


def test_packaged_private_keys():
    key_dir = os.path.join(curr_dir, 'keys')
    plugin = PackagedPrivateKeys()
    assert 0 == len(plugin.issues)
    private_key_files = ['rsa-key', 'dsa-key', 'ed25519-key', 'ecdsa-key']
    for i, file_path in enumerate(private_key_files):
        absolute_path = os.path.join(key_dir, file_path)
        assert i == len(plugin.issues)
        with open(absolute_path) as f:
            contents = f.read()
        plugin.run(absolute_path, file_contents=contents)
        assert i + 1 == len(plugin.issues)
    public_key_files = [path + '.pub' for path in private_key_files]
    num_issues = len(plugin.issues)
    for file_path in public_key_files:
        with open(os.path.join(key_dir, file_path)) as f:
            contents = f.read()
        plugin.run(file_path, file_contents=contents)
        assert num_issues == len(plugin.issues)
