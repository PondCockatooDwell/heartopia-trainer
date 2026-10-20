from __future__ import annotations

from dataclasses import dataclass

PATTERN_CHUNK = 0x10000


@dataclass(slots=True)
class Pattern:
    bytes_: bytes
    mask: bytes  # b"\x01" for fixed, b"\x00" for wildcard

    @classmethod
    def parse(cls, sig: str) -> "Pattern":
        parts = sig.split()
        raw = bytearray()
        mask = bytearray()
        for p in parts:
            if p in ("??", "?"):
                raw.append(0)
                mask.append(0)
            else:
                raw.append(int(p, 16))
                mask.append(1)
        return cls(bytes(raw), bytes(mask))


def scan(data: bytes, pattern: Pattern) -> int:
    n = len(pattern.bytes_)
    for i in range(len(data) - n):
        ok = True
        for j in range(n):
            if pattern.mask[j] and data[i + j] != pattern.bytes_[j]:
                ok = False
                break
        if ok:
            return i
    return -1