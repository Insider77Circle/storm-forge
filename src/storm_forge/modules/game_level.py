"""GAME LEVEL — XP, levels, streaks over lab completions.

TODO (owner): persist to SQLite; this in-memory version defines the
level curve (100 XP per level, compounding).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Player:
    xp: int = 0
    streak: int = 0

    @property
    def level(self) -> int:
        return self.xp // 100 + 1

    def complete_lab(self, difficulty: int) -> None:
        self.xp += 25 * difficulty
        self.streak += 1

    def miss_lab(self) -> None:
        self.streak = 0
