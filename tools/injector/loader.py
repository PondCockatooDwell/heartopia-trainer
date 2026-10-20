"""DLL loader used by the overlay to inject the ESP renderer."""
from __future__ import annotations

import ctypes
from pathlib import Path

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)


def inject(pid: int, dll_path: Path) -> int:
    dll = str(dll_path.resolve())
    if not Path(dll).is_file():
        raise FileNotFoundError(dll)

    PROCESS_ALL_ACCESS = 0x1F0FFF
    handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not handle:
        raise OSError(f"OpenProcess failed: {ctypes.get_last_error()}")

    try:
        size = len(dll) + 1
        addr = kernel32.VirtualAllocEx(handle, None, size, 0x3000, 0x04)
        kernel32.WriteProcessMemory(handle, addr, dll.encode(), size, None)
        h_thread = kernel32.CreateRemoteThread(
            handle, None, 0, kernel32.GetProcAddress(
                kernel32.GetModuleHandleW("kernel32.dll"), b"LoadLibraryA"
            ), addr, 0, None,
        )
        if not h_thread:
            raise OSError("CreateRemoteThread failed")
        kernel32.WaitForSingleObject(h_thread, 5000)
    finally:
        kernel32.CloseHandle(handle)
    return 0