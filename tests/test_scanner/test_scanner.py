from qark.scanner.scanner import Scanner

import os
import shutil


def test_run(scanner, decompiler):
    decompiler.decompile()

    scanner.issues = []
    scanner.decompiler = decompiler
    scanner.run()
    assert 0 < len(scanner.issues)


def test_run_manifest_checks(scanner):
    scanner.issues = []
    scanner._run_checks("manifest")
    assert 7 == len(scanner.issues)

    # this should hit the other code path where
    #   manifest_path is already set
    scanner.issues = []
    scanner._run_checks("manifest")
    assert 7 == len(scanner.issues)


def test_run_broadcast_checks(scanner):
    scanner.issues = []
    scanner._run_checks("broadcast")
    assert 0 < len(scanner.issues)


def test_run_file_checks(scanner):
    scanner.issues = []
    scanner._run_checks("file")
    assert 0 == len(scanner.issues)


def test_run_intent_checks(scanner):
    scanner.issues = []
    scanner._run_checks("intent")
    assert 0 == len(scanner.issues)  # goatdroid doesnt have any of these vulnerabilities


def test_scanner_singleton(decompiler):
    s1 = Scanner(decompiler=decompiler)
    s1.issues = []
    s1.issues.append("new_issue")

    s2 = Scanner(decompiler=decompiler)
    assert s2 is s1
    assert len(s2.issues) == 1
    assert s2.issues.pop() == "new_issue"
