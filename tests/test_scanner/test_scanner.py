SCANNER_ISSUES = 10


def test_run(scanner, decompiler):
    decompiler.decompile()

    scanner.issues = []
    scanner.decompiler = decompiler
    scanner.run()
    assert 0 < len(scanner.issues)

    scanner.issues = []
    scanner._run_checks("manifest")
    assert SCANNER_ISSUES == len(scanner.issues)
