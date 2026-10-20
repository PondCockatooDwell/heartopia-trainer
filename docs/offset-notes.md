# Offset notes — Heartopia 1.5.0

Pointer chain for `player_base`:
`module + 0x02F4A1C0 -> +0x30 -> player struct`

Confirmed on build 1722 (Steam). The `entity_list` is a fixed array of
256 slots, stride 0x40, terminated by a null vtable pointer.

**Warning:** offsets shift on every minor patch. Always re-run the
signature scanner (`python -m heartopia_trainer.utils.pattern_scan`)
before shipping a build.