from __future__ import annotations

import math

from heartopia_trainer.models.player_state import PlayerState, Vec3
from heartopia_trainer.platform.input_driver import InputDriver
from heartopia_trainer.services.memory_service import MemoryService


class AimService:
    """Soft-aim helper — nudges the camera toward the closest target entity."""

    def __init__(self, memory: MemoryService, input_driver: InputDriver) -> None:
        self.memory = memory
        self.input_driver = input_driver
        self.enabled = False

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        return self.enabled

    def _angle_to(self, origin: Vec3, target: Vec3) -> float:
        return math.degrees(math.atan2(target.y - origin.y, target.x - origin.x))

    def update(self, state: PlayerState) -> None:
        if not self.enabled:
            return
        root = self.memory.abs("entity_list")
        try:
            target = Vec3(
                self.memory.read_float(root + 0x10),
                self.memory.read_float(root + 0x14),
                self.memory.read_float(root + 0x18),
            )
        except Exception:
            return
        angle = self._angle_to(state.position, target)
        if abs(angle) < 2.0:
            self.input_driver.press("space")