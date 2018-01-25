from qark.scanner.scanner import Scanner

import os
import shutil


def test_run(scanner, build_directory, decompiler):
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    decompiler._run_dex2jar()
    decompiler.run_apktool()
    decompiler.decompile()

    scanner.issues = []
    scanner.decompiler = decompiler
    scanner.run()
    assert 0 < len(scanner.issues)


def test_run_manifest_checks(scanner):
    scanner.issues = []
    scanner._run_manifest_checks()
    assert 7 == len(scanner.issues)

    # this should hit the other code path where
    #   manifest_path is already set
    scanner.issues = []
    scanner._run_manifest_checks()
    assert 7 == len(scanner.issues)


def test_run_broadcast_checks(scanner):
    scanner.issues = []
    scanner._run_broadcast_checks()
    assert 0 == len(scanner.issues)  # goatdroid not using these methods


def test_run_file_checks(scanner):
    scanner.issues = []
    scanner._run_file_checks()
    assert 0 == len(scanner.issues)
    
    
def test_run_intent_checks(scanner):
    scanner.issues = []
    scanner._run_intent_checks()
    assert 0 == len(scanner.issues)  # goatdroid doesnt have any of these vulnerabilities


def test_scanner_singleton(decompiler):
    s1 = Scanner(decompiler=decompiler)
    s1.issues = []
    s1.issues.append("new_issue")

    s2 = Scanner(decompiler=decompiler)
    assert s2 is s1
    assert len(s2.issues) == 1
    assert s2.issues.pop() == "new_issue"
