# Contributing to Heartopia Trainer

Thanks for your interest in improving the trainer. This project is a
hobbyist / educational reverse-engineering effort for the single-player
Heartopia client. Please read the guidelines before opening a PR.

## Ground rules

- Heartopia Trainer is **single-player only**. Do not submit patches that
  target multiplayer sessions, online services, or other players.
- No telemetry, no remote payloads, no obfuscated blobs. Every binary
  read/write path must be reviewable.
- Cheat signatures, offsets and memory patterns belong in
  `heartopia-signatures/` — never hardcoded in services.

## Development setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m heartopia_trainer --dry-run
```

## Pull request checklist

1. `pytest tests/` passes locally.
2. New offsets include the game build number in
   `heartopia-signatures/builds.yaml`.
3. New features are gated behind `config/features.yaml` flags.
4. Update `docs/offset-notes.md` when touching the pointer scanner.

## Style

- Python 3.11+, type hints required for public functions.
- Ruff + black defaults, 100 char line length.
- Services return dataclasses, not dicts.