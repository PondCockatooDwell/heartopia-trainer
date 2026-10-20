from __future__ import annotations

import argparse
import sys

from heartopia_trainer.platform.win32_attach import AttachError, attach_to_heartopia
from heartopia_trainer.services.trainer_service import TrainerService
from heartopia_trainer.ui.overlay_window import launch_overlay


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="heartopia-trainer")
    p.add_argument("--dry-run", action="store_true", help="scan offsets, do not write")
    p.add_argument("--no-overlay", action="store_true", help="headless / CLI mode")
    p.add_argument("--pid", type=int, default=None)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        proc = attach_to_heartopia(pid=args.pid)
    except AttachError as exc:
        print(f"[heartopia-trainer] attach failed: {exc}", file=sys.stderr)
        return 2

    service = TrainerService(proc, dry_run=args.dry_run)
    service.bootstrap()

    if args.no_overlay:
        service.run_cli_loop()
        return 0

    return launch_overlay(service)