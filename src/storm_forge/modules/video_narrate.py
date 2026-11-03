"""VIDEO NARRATE — narration script for a lab walkthrough video.

TODO (owner): pipe the script to a TTS voice and overlay it on the
lab recording.
"""

from __future__ import annotations

from storm_forge.engine import generate_scenario, parse


def script(objective: str) -> str:
    """Return a narration script for a lab walkthrough."""
    scenario = generate_scenario(parse(objective))
    lines = [
        f"Welcome to STORM FORGE. Today's lab: {scenario.title}.",
        "",
        scenario.narrative,
        "",
    ]
    for i, step in enumerate(scenario.steps, 1):
        lines.append(f"Step {i}: {step}")
    lines += [
        "",
        "Win condition: " + "; ".join(scenario.win_conditions),
    ]
    return "\n".join(lines)
