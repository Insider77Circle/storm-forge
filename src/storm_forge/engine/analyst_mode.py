"""Analyst Mode — attempts -> debrief report.

TODO (owner): grade against telemetry (which events fired, which
detections hit) instead of raw attempt counts once the sandbox
backend exists. The markdown shape below is the contract.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Attempt:
    step: str
    success: bool
    note: str = ""


def debrief(title: str, attempts: list[Attempt]) -> str:
    """Render a debrief report for a completed lab run."""
    passed = sum(1 for a in attempts if a.success)
    lines = [
        f"# Analyst debrief — {title}",
        "",
        f"Steps passed: {passed}/{len(attempts)}",
        "",
    ]
    for a in attempts:
        mark = "✅" if a.success else "❌"
        lines.append(f"- {mark} {a.step}" + (f" — {a.note}" if a.note else ""))
    lines += [
        "",
        "Next: raise difficulty if 2+ clean passes, or repeat the missed "
        "steps at the same level.",
    ]
    return "\n".join(lines)
