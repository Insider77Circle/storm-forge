"""BLUE TEAM // DEFENSIVE — detect, triage, hunt, respond."""

from __future__ import annotations

PRESETS = [
    "detect LSASS credential dumping",
    "hunt phishing attachment execution",
    "triage a ransomware encryption chain",
]


def preset(index: int = 0) -> str:
    """Return a defensive lab objective by index."""
    return PRESETS[index % len(PRESETS)]
