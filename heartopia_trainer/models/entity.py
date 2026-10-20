from __future__ import annotations

from dataclasses import dataclass

from heartopia_trainer.models.player_state import Vec3


@dataclass(slots=True)
class Entity:
    address: int
    name: str
    kind: str  # "npc" | "item" | "resource" | "player"
    position: Vec3
    distance: float = 0.0