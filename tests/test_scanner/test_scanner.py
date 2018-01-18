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


def test_singleton(scanner):
    pass