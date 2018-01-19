from qark.scanner.scanner import Scanner


def test_run(scanner):
    scanner.run()
    assert 0 < len(scanner.issues)


def test_run_manifest_checks(scanner):
    scanner._run_manifest_checks()
    assert 0 < len(scanner.issues)

    # this should hit the other code path where
    #   manifest_path is already set
    scanner._run_manifest_checks()
    assert 0 < len(scanner.issues)


def test_scanner_singleton(decompiler):
    s1 = Scanner(decompiler=decompiler)
    s1.issues = []
    s1.issues.append("new_issue")

    s2 = Scanner(decompiler=decompiler)
    assert s2 is s1
    assert len(s2.issues) == 1
    assert s2.issues.pop() == "new_issue"
