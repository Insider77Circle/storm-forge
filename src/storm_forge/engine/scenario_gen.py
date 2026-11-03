"""Scenario Gen — structured intent -> narrative lab.

TODO (owner): plug a frontier model in here. The prompt contract is:
given a ParsedObjective, return title / narrative / steps / injects /
win conditions. Until then, the template below keeps the pipeline
runnable end to end.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from storm_forge.engine.parser import ParsedObjective


@dataclass
class Scenario:
    title: str
    narrative: str
    steps: list[str] = field(default_factory=list)
    injects: list[str] = field(default_factory=list)
    win_conditions: list[str] = field(default_factory=list)
    mitre_techniques: list[str] = field(default_factory=list)
    difficulty: int = 1


def generate_scenario(parsed: ParsedObjective) -> Scenario:
    """Generate a lab scenario from parsed intent (template fallback)."""
    skill = parsed.skill.replace("-", " ")
    title = f"{parsed.raw.strip().capitalize()} — {parsed.track} team lab"
    narrative = (
        f"A {parsed.track}-team exercise on {skill}. "
        "You are dropped into a sandbox network with telemetry on. "
        "Work the steps, watch the signals, and close the loop in Analyst Mode."
    )
    if parsed.track == "blue":
        steps = [
            "Collect the relevant telemetry (process, auth, network).",
            "Identify the anomalous event chain.",
            "Write a detection rule for it.",
            "Triage: true positive, false positive, or benign?",
        ]
        win = ["Detection rule fires on the injected event, not on benign traffic."]
    else:
        steps = [
            "Map the sandbox target (simulated hosts only).",
            "Run the adversary chain step by step.",
            "Observe which telemetry each step produces.",
            "Write up what a defender should have caught.",
        ]
        win = ["Full chain runs inside the sandbox; defender write-up filed."]
    return Scenario(
        title=title,
        narrative=narrative,
        steps=steps,
        injects=["Benign background traffic", "One anomalous event chain"],
        win_conditions=win,
        mitre_techniques=parsed.mitre_techniques,
        difficulty=parsed.difficulty,
    )
