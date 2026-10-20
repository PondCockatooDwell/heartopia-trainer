from __future__ import annotations

import struct
from pathlib import Path

import yaml

from heartopia_trainer.platform.win32_attach import HeartopiaProcess

OFFSETS_PATH = Path(__file__).resolve().parents[2] / "config" / "offsets.yaml"


class MemoryService:
    """Reads/writes Heartopia process memory via pymem. All writes are gated."""

    def __init__(self, proc: HeartopiaProcess, dry_run: bool = False) -> None:
        self.proc = proc
        self.dry_run = dry_run
        self.offsets: dict[str, int] = {}
        self.offsets_abs: dict[str, int] = {}

    def load_offsets(self) -> None:
        data = yaml.safe_load(OFFSETS_PATH.read_text(encoding="utf-8"))
        base = self.proc.base_address
        for name, raw in data["offsets"].items():
            val = int(raw, 16) if isinstance(raw, str) else int(raw)
            self.offsets[name] = val
            self.offsets_abs[name] = base + val if val > 0x1000 else val

    def read_float(self, address: int) -> float:
        buf = self.proc.handle.read_bytes(address, 4)
        return struct.unpack("<f", buf)[0]

    def write_float(self, address: int, value: float) -> None:
        if self.dry_run:
            return
        self.proc.handle.write_bytes(address, struct.pack("<f", value))

    def read_int(self, address: int) -> int:
        buf = self.proc.handle.read_bytes(address, 4)
        return struct.unpack("<i", buf)[0]

    def abs(self, key: str) -> int:
        return self.offsets_abs[key]