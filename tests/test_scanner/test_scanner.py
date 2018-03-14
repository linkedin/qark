def test_run(scanner, decompiler):
    decompiler.decompile()

    scanner.issues = []
    scanner.decompiler = decompiler
    scanner.run()
    assert 0 < len(scanner.issues)

    scanner.issues = []
    scanner._run_checks("manifest")
    assert 7 == len(scanner.issues)

    # this should hit the other code path where
    #   manifest_path is already set
    scanner.issues = []
    scanner._run_checks("manifest")
    assert 10 == len(scanner.issues)

    scanner.issues = []
    scanner._run_checks("broadcast")
    assert 0 < len(scanner.issues)

    scanner.issues = []
    scanner._run_checks("file")
    assert 0 == len(scanner.issues)

    scanner.issues = []
    scanner._run_checks("intent")
    assert 0 == len(scanner.issues)  # goatdroid doesnt have any of these vulnerabilities
