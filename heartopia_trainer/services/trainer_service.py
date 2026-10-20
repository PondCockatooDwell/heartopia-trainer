from __future__ import annotations

import logging
import time

from heartopia_trainer.models.player_state import PlayerState, Vec3
from heartopia_trainer.platform.input_driver import InputDriver
from heartopia_trainer.platform.win32_attach import HeartopiaProcess
from heartopia_trainer.services.aim_service import AimService
from heartopia_trainer.services.esp_service import EspService
from heartopia_trainer.services.memory_service import MemoryService
from heartopia_trainer.services.player_service import PlayerService

log = logging.getLogger(__name__)


class TrainerService:
    """Top-level coordinator — owns services, exposes a stable API for the UI."""

    def __init__(self, proc: HeartopiaProcess, dry_run: bool = False) -> None:
        self.proc = proc
        self.dry_run = dry_run
        self.memory = MemoryService(proc, dry_run=dry_run)
        self.player = PlayerService(self.memory)
        self.esp = EspService(self.memory)
        self.aim = AimService(self.memory, InputDriver())
        self._running = False

    def bootstrap(self) -> None:
        self.memory.load_offsets()
        state = self.player.read_state()
        log.info("attached pid=%s player_hp=%.1f pos=%s", self.proc.pid, state.health, state.position)

    def apply_cheats(self) -> None:
        self.player.enable_godmode()
        self.player.set_speed_multiplier(2.0)
        self.player.refill_stamina()

    def tick(self) -> PlayerState:
        state = self.player.read_state()
        if self.aim.enabled:
            self.aim.update(state)
        return state

    def run_cli_loop(self) -> None:
        self._running = True
        while self._running:
            try:
                self.tick()
            except Exception as exc:  # pragma: no cover - defensive loop
                log.exception("tick failed: %s", exc)
            time.sleep(0.05)