from __future__ import annotations

import time

try:
    import keyboard
except ImportError:  # pragma: no cover
    keyboard = None  # type: ignore[assignment]


class InputDriver:
    """Thin wrapper around global hotkeys / synthetic key events."""

    def __init__(self) -> None:
        self._bound: list[str] = []

    def bind_toggle(self, combo: str, callback) -> None:
        if keyboard is None:
            return
        keyboard.add_hotkey(combo, callback)
        self._bound.append(combo)

    def press(self, key: str, hold_ms: int = 40) -> None:
        if keyboard is None:
            return
        keyboard.press(key)
        time.sleep(hold_ms / 1000)
        keyboard.release(key)

    def unbind_all(self) -> None:
        if keyboard is None:
            return
        for combo in self._bound:
            keyboard.remove_hotkey(combo)
        self._bound.clear()