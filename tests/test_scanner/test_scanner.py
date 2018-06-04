import pytest

SCANNER_ISSUES = 10


@pytest.mark.long
def test_run(scanner, decompiler):
    decompiler.run()

    scanner.issues = []
    scanner.decompiler = decompiler
    scanner.run()
    assert 0 < len(scanner.issues)
