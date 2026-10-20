# Security Policy

## Supported versions

| Trainer version | Heartopia build | Status |
|-----------------|-----------------|--------|
| 2.x             | 1.4.2 – 1.5.0   | Active |
| 1.x             | 1.2.x           | Legacy |

## Reporting a vulnerability

Heartopia Trainer is a local Windows desktop tool. The most relevant
classes of issues are:

- Memory-write routines that could corrupt save files.
- Loader / injector bugs causing game crashes.
- Privilege escalation from the overlay process.
- Any accidental network egress from the trainer process.

Please email **security@heartopia-trainer.dev** with a PoC. Do **not**
open a public issue for anything that can corrupt a user's save.

## Scope

In scope: the trainer process, its DLL loader, the overlay injector.
Out of scope: the Heartopia game client itself, third-party mods bundled
by users.

## Disclosure

We aim to acknowledge reports within 72 hours and ship a fix within
14 days for memory-corruption issues.