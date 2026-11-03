"""ONE-CLICK — the full pipeline in one call."""

from __future__ import annotations

from storm_forge.engine import (
    build_lab,
    check_lab,
    generate_scenario,
    parse,
)


def run(objective: str) -> dict:
    """Run parse -> scenario -> sandbox spec -> safety filter."""
    parsed = parse(objective)
    scenario = generate_scenario(parsed)
    lab = build_lab(scenario)
    verdict = check_lab(lab)
    return {
        "objective": parsed.raw,
        "track": parsed.track,
        "scenario": scenario,
        "lab": lab,
        "safety_allowed": verdict.allowed,
        "safety_reasons": verdict.reasons,
    }
