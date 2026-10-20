from __future__ import annotations

from dataclasses import dataclass

from heartopia_trainer.models.entity import Entity
from heartopia_trainer.models.player_state import Vec3
from heartopia_trainer.services.memory_service import MemoryService

MAX_ENTITIES = 256


@dataclass(slots=True)
class EspConfig:
    show_npcs: bool = True
    show_items: bool = True
    max_distance: float = 200.0


class EspService:
    def __init__(self, memory: MemoryService, config: EspConfig | None = None) -> None:
        self.memory = memory
        self.config = config or EspConfig()

    def _read_entity(self, address: int, origin: Vec3) -> Entity | None:
        try:
            pos = Vec3(
                self.memory.read_float(address + 0x10),
                self.memory.read_float(address + 0x14),
                self.memory.read_float(address + 0x18),
            )
        except Exception:
            return None
        dx, dy, dz = pos.x - origin.x, pos.y - origin.y, pos.z - origin.z
        dist = (dx * dx + dy * dy + dz * dz) ** 0.5
        if dist > self.config.max_distance:
            return None
        return Entity(address=address, name="", kind="npc", position=pos, distance=dist)

    def scan(self, origin: Vec3) -> list[Entity]:
        root = self.memory.abs("entity_list")
        found: list[Entity] = []
        for i in range(MAX_ENTITIES):
            ent = self._read_entity(root + i * 0x40, origin)
            if ent is not None:
                found.append(ent)
        return found