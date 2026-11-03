"""TOOL EDGE — tool-first drills: one tool, one technique, timed.

TODO (owner): wire each drill to a real sandbox tool run and a timer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Drill:
    tool: str
    technique_id: str
    time_limit_seconds: int = 600


def drill_for(tool: str, technique_id: str) -> Drill:
    """Build a timed drill for one tool and one technique."""
    return Drill(tool=tool, technique_id=technique_id)
