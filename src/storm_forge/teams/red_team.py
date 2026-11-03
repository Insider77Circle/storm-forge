"""RED TEAM // SIMULATED OFFENSE — adversary emulation, sandbox only.

Nothing in this module targets a real system. Every preset runs through
the Safety Filter, which blocks any lab not marked sandbox-only.
"""

from __future__ import annotations

PRESETS = [
    "simulate LSASS credential dumping in the sandbox",
    "simulate lateral movement with SMB admin shares",
    "simulate persistence with a scheduled task",
]


def preset(index: int = 0) -> str:
    """Return a simulated-offense lab objective by index."""
    return PRESETS[index % len(PRESETS)]
