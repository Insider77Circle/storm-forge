"""Adaptive Diff — difficulty follows performance.

Simple rule, easy to replace: two clean passes in a row step the level
up, two misses step it down, clamped to 1-5. Feed it Analyst Mode
results, not vibes.
"""

from __future__ import annotations


def next_difficulty(current: int, passes: int, misses: int) -> int:
    """Return the next difficulty level (1-5) from recent results."""
    level = current
    if passes >= 2:
        level += 1
    elif misses >= 2:
        level -= 1
    return max(1, min(5, level))
