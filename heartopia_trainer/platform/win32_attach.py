from __future__ import annotations

import ctypes
from dataclasses import dataclass

try:
    import pymem
except ImportError:  # pragma: no cover - only on non-Windows dev boxes
    pymem = None  # type: ignore[assignment]

MODULE_NAME = "Heartopia.exe"
PROCESS_NAME = "Heartopia.exe"


class AttachError(RuntimeError):
    pass


@dataclass(slots=True)
class HeartopiaProcess:
    pid: int
    handle: object
    base_address: int
    module_size: int


def _enable_debug_privilege() -> None:
    if pymem is None:
        return
    try:
        pymem.process.process_from_name  # noqa: B018 - feature check
        ctypes.windll.advapi32  # type: ignore[attr-defined]
    except Exception:
        pass


def attach_to_heartopia(pid: int | None = None) -> HeartopiaProcess:
    if pymem is None:
        raise AttachError("pymem is required (Windows only)")

    _enable_debug_privilege()
    try:
        pm = pymem.Pymem(pid) if pid else pymem.Pymem(PROCESS_NAME)
    except pymem.exception.ProcessNotFound as exc:
        raise AttachError("Heartopia.exe is not running") from exc

    module = pymem.process.module_from_name(pm.process_handle, MODULE_NAME)
    if module is None:
        raise AttachError(f"{MODULE_NAME} module not loaded")

    return HeartopiaProcess(
        pid=pm.process_id,
        handle=pm,
        base_address=module.lpBaseOfDll,
        module_size=module.SizeOfImage,
    )