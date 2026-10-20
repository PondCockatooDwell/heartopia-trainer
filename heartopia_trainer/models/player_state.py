from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Vec3:
    x: float
    y: float
    z: float


@dataclass(slots=True)
class PlayerState:
    health: float
    max_health: float
    stamina: float
    speed: float
    position: Vec3
    godmode: bool = False
    speed_multiplier: float = 1.0

    @property
    def alive(self) -> bool:
        return self.health > 0.0