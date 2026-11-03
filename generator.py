"""Recursive scenario generation — the loop, closed.

Reads the learner profile, aims at the weakest skill, and compiles a
harder lab for exactly that weakness. Difficulty steps up by one per
recursion (capped at 5). If the store is empty, it falls back to a
default first lab — recursion needs data, and it says so.
"""

from __future__ import annotations

from storm_forge.compiler import compile_objective
from storm_forge.learner import LearnerStore

_FALLBACK = "detect LSASS credential dumping"


def next_lab(store: LearnerStore, current_difficulty: int = 1) -> dict:
    """Generate the next lab from learner weaknesses."""
    weak = store.weaknesses()
    if not weak:
        objective = _FALLBACK
        rationale = "No attempt data yet — starting with the default lab."
    else:
        skill = weak[0]
        objective = f"detect {skill.replace('-', ' ')} under time pressure"
        summary = store.summary(skill)
        top = summary["top_mistakes"][0][0] if summary["top_mistakes"] else "none"
        rationale = (
            f"Weakest skill: {skill} "
            f"(detection {summary['detection_rate']:.0%}, "
            f"top mistake {top})."
        )
    spec = compile_objective(objective)
    spec.difficulty = min(5, current_difficulty + 1)
    return {
        "objective": objective,
        "rationale": rationale,
        "difficulty": spec.difficulty,
        "networks": [
            {
                "name": n.name,
                "cidr": n.cidr,
                "hosts": [h.name for h in n.hosts],
            }
            for n in spec.networks
        ],
        "telemetry": spec.telemetry,
    }
