"""LAB TELEPROMPTER — step-by-step on-screen cues while you run a lab.

TODO (owner): render as an overlay UI with next/previous and a timer.
"""

from __future__ import annotations

from storm_forge.engine import generate_scenario, parse


def cues(objective: str) -> str:
    """Return numbered teleprompter cues for a lab."""
    scenario = generate_scenario(parse(objective))
    lines = [f"TELEPROMPTER — {scenario.title}", ""]
    for i, step in enumerate(scenario.steps, 1):
        lines.append(f"[CUE {i}] {step}")
    lines.append("")
    lines.append("Hold for questions, then advance.")
    return "\n".join(lines)
