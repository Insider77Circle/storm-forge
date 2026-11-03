"""Safety Filter — the load-bearing gate.

Rules (non-negotiable):
- Labs run in a sandbox only. `sandbox_only` must be True.
- No real hostnames, IPs, domains, or credentials in a lab spec.
- Red-team content is SIMULATED OFFENSE: adversary emulation against
  the sandbox, never instructions or tooling aimed at a real system.
- Anything that fails returns BLOCKED and the lab never builds.

TODO (owner): extend the denylist with your own patterns and wire this
into the build step so a BLOCKED verdict short-circuits the pipeline
(the CLI already refuses to print a blocked lab).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from storm_forge.engine.simulator_builder import Lab

_DENY_PATTERNS = [
    r"\b\d{1,3}(\.\d{1,3}){3}\b",  # raw IPv4 in spec text
    r"password\s*[:=]\s*\S+",  # embedded credential
    r"api[_-]?key\s*[:=]\s*\S+",
    r"\b(real|production|corp|internal)\.(com|net|local)\b",
]


@dataclass
class SafetyVerdict:
    allowed: bool
    reasons: list[str] = field(default_factory=list)


def check_lab(lab: Lab) -> SafetyVerdict:
    """Vet a lab spec. BLOCKED unless sandbox-only and clean."""
    reasons: list[str] = []
    if not lab.sandbox_only:
        reasons.append("lab is not marked sandbox-only")
    blob = " ".join([lab.title] + lab.services + lab.artifacts)
    for pattern in _DENY_PATTERNS:
        if re.search(pattern, blob, re.IGNORECASE):
            reasons.append(f"denied pattern matched: {pattern}")
    return SafetyVerdict(allowed=not reasons, reasons=reasons)
