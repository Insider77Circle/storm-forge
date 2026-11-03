"""Adaptive adversary engine — the simulated attacker reacts to the
defender.

Counterpart to Adaptive Diff (which tunes difficulty for the learner):
this tunes the ATTACKER. The engine watches defender events and changes
tactics:

- detected  -> go quiet, change technique, increase dwell
- blocked   -> pivot to a different technique at lower aggression
- missed    -> escalate: same technique, higher aggression

All of this plays out inside the sandbox. The engine outputs moves, not
exploits — the range provider decides what, if anything, executes.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DefenderEvent:
    kind: str  # "detected" | "blocked" | "missed"
    technique_id: str
    step: str = ""


@dataclass
class AdversaryEngine:
    technique_id: str
    aggression: int = 3  # 1-5
    dwell_minutes: int = 5
    history: list[str] = field(default_factory=list)

    def observe(self, event: DefenderEvent) -> str:
        """React to a defender event; return the next move description."""
        if event.kind == "detected":
            self.dwell_minutes *= 2
            self.aggression = max(1, self.aggression - 1)
            move = (
                f"Detected on {event.technique_id}: going quiet "
                f"({self.dwell_minutes} min dwell), switching technique."
            )
        elif event.kind == "blocked":
            self.aggression = max(1, self.aggression - 1)
            move = (
                f"Blocked on {event.technique_id}: pivoting to an "
                "alternate technique at lower aggression."
            )
        elif event.kind == "missed":
            self.aggression = min(5, self.aggression + 1)
            move = (
                f"Missed on {event.technique_id}: escalating, same "
                f"technique at aggression {self.aggression}."
            )
        else:
            move = f"Unknown event kind {event.kind!r}: holding position."
        self.history.append(move)
        return move
