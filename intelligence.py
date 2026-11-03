"""Learner intelligence — track decision-making across exercises.

Records every attempt (skill, detected or missed, response time,
mistakes) in SQLite and derives the profile the recursive generator
reads: detection rate, mean time to detect/respond, mistake taxonomy,
and a weakness ranking. This is the loop's memory — without it,
recursive generation has nothing to aim at.

Mistake taxonomy (keep it small and stable; the generator keys off it):
- MISSED_TELEMETRY: the signal was there, the learner didn't look
- WRONG_RULE: detection written, but it doesn't fire (or misfires)
- SLOW_TRIAGE: right call, too slow
- FALSE_POSITIVE: benign traffic called malicious
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

MISTAKES = ("MISSED_TELEMETRY", "WRONG_RULE", "SLOW_TRIAGE", "FALSE_POSITIVE")


@dataclass
class AttemptRecord:
    skill: str
    detected: bool
    response_time_s: float
    mistakes: list[str]
    success: bool


class LearnerStore:
    """SQLite-backed attempt log + weakness ranking."""

    def __init__(self, path: str = ":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS attempts ("
            "skill TEXT, detected INTEGER, response_time_s REAL, "
            "mistakes TEXT, success INTEGER)"
        )

    def record(self, attempt: AttemptRecord) -> None:
        self.db.execute(
            "INSERT INTO attempts VALUES (?, ?, ?, ?, ?)",
            (
                attempt.skill,
                int(attempt.detected),
                attempt.response_time_s,
                ",".join(attempt.mistakes),
                int(attempt.success),
            ),
        )
        self.db.commit()

    def summary(self, skill: str) -> dict:
        rows = self.db.execute(
            "SELECT detected, response_time_s, mistakes, success "
            "FROM attempts WHERE skill = ?",
            (skill,),
        ).fetchall()
        if not rows:
            return {"skill": skill, "attempts": 0}
        mistakes: dict[str, int] = {}
        for _, _, m, _ in rows:
            for item in filter(None, m.split(",")):
                mistakes[item] = mistakes.get(item, 0) + 1
        return {
            "skill": skill,
            "attempts": len(rows),
            "detection_rate": sum(r[0] for r in rows) / len(rows),
            "mean_response_time_s": sum(r[1] for r in rows) / len(rows),
            "success_rate": sum(r[3] for r in rows) / len(rows),
            "top_mistakes": sorted(mistakes.items(), key=lambda kv: -kv[1]),
        }

    def weaknesses(self) -> list[str]:
        """Skills ranked weakest-first (lowest detection, then slowest)."""
        skills = [
            r[0]
            for r in self.db.execute("SELECT DISTINCT skill FROM attempts")
        ]
        scored = []
        for skill in skills:
            s = self.summary(skill)
            scored.append(
                (s["detection_rate"], -s["mean_response_time_s"], skill)
            )
        scored.sort()
        return [skill for _, _, skill in scored]
