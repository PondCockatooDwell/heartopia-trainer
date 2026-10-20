from __future__ import annotations

import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from heartopia_trainer.services.trainer_service import TrainerService


class OverlayWindow(QWidget):
    def __init__(self, service: TrainerService) -> None:
        super().__init__()
        self.service = service
        self.setWindowTitle("Heartopia Trainer — overlay")
        self.setAttribute(self.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(self.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.resize(280, 120)

        self.status = QLabel("attached")
        layout = QVBoxLayout(self)
        layout.addWidget(self.status)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(100)

    def _tick(self) -> None:
        try:
            state = self.service.tick()
            self.status.setText(f"hp={state.health:.0f} spd={state.speed:.1f}")
        except Exception as exc:
            self.status.setText(f"err: {exc}")


def launch_overlay(service: TrainerService) -> int:
    app = QApplication(sys.argv)
    win = OverlayWindow(service)
    win.show()
    return app.exec()