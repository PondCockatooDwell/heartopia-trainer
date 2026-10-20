from __future__ import annotations

from heartopia_trainer.models.player_state import PlayerState, Vec3
from heartopia_trainer.services.memory_service import MemoryService


class PlayerService:
    def __init__(self, memory: MemoryService) -> None:
        self.memory = memory

    def _player_base(self) -> int:
        return self.memory.abs("player_base")

    def read_state(self) -> PlayerState:
        base = self._player_base()
        o = self.memory.offsets
        return PlayerState(
            health=self.memory.read_float(base + o["health"]),
            max_health=self.memory.read_float(base + o["health"] + 4),
            stamina=self.memory.read_float(base + o["stamina"]),
            speed=self.memory.read_float(base + o["speed_stat"]),
            position=Vec3(
                self.memory.read_float(base + o["position_x"]),
                self.memory.read_float(base + o["position_y"]),
                self.memory.read_float(base + o["position_z"]),
            ),
        )

    def enable_godmode(self) -> None:
        base = self._player_base()
        hp = base + self.memory.offsets["health"]
        self.memory.write_float(hp, 9999.0)

    def refill_stamina(self) -> None:
        base = self._player_base()
        self.memory.write_float(base + self.memory.offsets["stamina"], 100.0)

    def set_speed_multiplier(self, mult: float) -> None:
        base = self._player_base()
        self.memory.write_float(base + self.memory.offsets["speed_stat"], mult)

    def teleport(self, pos: Vec3) -> None:
        base = self._player_base()
        o = self.memory.offsets
        self.memory.write_float(base + o["position_x"], pos.x)
        self.memory.write_float(base + o["position_y"], pos.y)
        self.memory.write_float(base + o["position_z"], pos.z)