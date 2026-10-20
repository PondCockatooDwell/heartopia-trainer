from heartopia_trainer.utils.pattern_scan import Pattern, scan


def test_scan_finds_signature_with_wildcards():
    blob = b"\x00\x11\x22\x33\x44\x55\x66"
    pat = Pattern.parse("11 22 ?? 44")
    assert scan(blob, pat) == 1


def test_scan_returns_minus_one_when_absent():
    assert scan(b"\x00\x01\x02", Pattern.parse("aa bb cc")) == -1