"""Parser — objective (plain English) -> structured intent.

TODO (owner): replace the demo keyword map with a frontier-model call
that returns skill / MITRE techniques / difficulty / prerequisites.
The dataclass shape is the contract; keep it stable when you swap the
implementation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Demo map only — lets the skeleton run offline. Real mapping belongs
# behind a model call or the MITRE ATT&CK dataset (see modules/mitre_attack).
_DEMO_MAP: list[tuple[str, str, list[str]]] = [
    (r"lsass|credential dump", "credential-access", ["T1003.001"]),
    (r"phish", "initial-access", ["T1566.001"]),
    (r"ransomware|encrypt", "impact", ["T1486"]),
    (r"lateral|psexec|wmi", "lateral-movement", ["T1021.002"]),
    (r"persist|registry|scheduled task", "persistence", ["T1053.005"]),
    (r"detect|hunt|triage", "detection", []),
]


@dataclass
class ParsedObjective:
    raw: str
    skill: str
    track: str  # "blue" or "red"
    mitre_techniques: list[str] = field(default_factory=list)
    difficulty: int = 1  # 1-5
    prerequisites: list[str] = field(default_factory=list)


def parse(objective: str) -> ParsedObjective:
    """Parse a plain-English lab objective into structured intent."""
    text = objective.lower()
    skill = "general"
    techniques: list[str] = []
    for pattern, mapped_skill, tids in _DEMO_MAP:
        if re.search(pattern, text):
            skill = mapped_skill
            techniques = tids
            break
    # Defensive intent wins: "detect LSASS dumping" is a blue lab even
    # though it names an attack technique.
    if re.search(r"detect|hunt|triage|defend", text):
        track = "blue"
    elif re.search(r"attack|exploit|dump|bypass", text):
        track = "red"
    else:
        track = "blue"
    difficulty = 2 if techniques else 1
    return ParsedObjective(
        raw=objective,
        skill=skill,
        track=track,
        mitre_techniques=techniques,
        difficulty=difficulty,
        prerequisites=["sandbox access"] if track == "red" else [],
    )
