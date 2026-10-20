"""CLI: scan a memory dump for the Heartopia player_base signature."""
from __future__ import annotations

import argparse
from pathlib import Path

from heartopia_trainer.utils.pattern_scan import Pattern, scan

SIG_150 = "48 8B 05 ?? ?? ?? ?? 48 8B 88 ?? ?? ?? ?? 48 85 C9 74"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dump", type=Path)
    args = ap.parse_args()
    data = args.dump.read_bytes()
    hit = scan(data, Pattern.parse(SIG_150))
    print(f"signature offset: {hit:#x}" if hit >= 0 else "not found")
    return 0 if hit >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())