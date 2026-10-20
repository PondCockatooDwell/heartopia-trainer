from __future__ import annotations

import struct

from heartopia_trainer.services.memory_service import MemoryService
from heartopia_trainer.services.player_service import PlayerService


class FakeProc:
    def __init__(self, blob: bytes) -> None:
        self.blob = bytearray(blob)
        self.base_address = 0x1000
        self.pid = 4242
        self.handle = self

    def read_bytes(self, addr: int, size: int) -> bytes:
        off = addr - self.base_address
        return bytes(self.blob[off : off + size])

    def write_bytes(self, addr: int, data: bytes) -> None:
        off = addr - self.base_address
        self.blob[off : off + len(data)] = data


def _make_memory() -> tuple[MemoryService, FakeProc]:
    blob = bytearray(0x4000)
    proc = FakeProc(blob)
    mem = MemoryService(proc, dry_run=False)  # type: ignore[arg-type]
    mem.offsets = {"health": 0x100, "stamina": 0x110, "speed_stat": 0x120,
                   "position_x": 0x200, "position_y": 0x204, "position_z": 0x208}
    mem.offsets_abs = {"player_base": 0x1000}
    return mem, proc


def test_read_and_write_health():
    mem, proc = _make_memory()
    struct.pack_into("<f", proc.blob, 0x100, 42.5)
    svc = PlayerService(mem)
    assert svc.read_state().health == 42.5
    svc.enable_godmode()
    assert struct.unpack_from("<f", proc.blob, 0x100)[0] == 9999.0