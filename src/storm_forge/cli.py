"""STORM FORGE CLI — one-click labs from plain-English objectives.

Usage:
    python -m storm_forge.cli one-click "detect LSASS credential dumping"
    python -m storm_forge.cli narrate "detect LSASS credential dumping"
    python -m storm_forge.cli teleprompter "detect LSASS credential dumping"

The pipeline runs fully offline in skeleton form: parse -> scenario ->
sandbox spec -> safety filter -> JSON. A BLOCKED safety verdict refuses
to print the lab.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from storm_forge.engine import (
    build_lab,
    check_lab,
    generate_scenario,
    parse,
)
from storm_forge.modules import lab_teleprompter, video_narrate


def _run_pipeline(objective: str) -> dict:
    parsed = parse(objective)
    scenario = generate_scenario(parsed)
    lab = build_lab(scenario)
    verdict = check_lab(lab)
    if not verdict.allowed:
        raise SystemExit(f"BLOCKED by safety filter: {'; '.join(verdict.reasons)}")
    return {
        "objective": parsed.raw,
        "skill": parsed.skill,
        "track": parsed.track,
        "mitre_techniques": parsed.mitre_techniques,
        "difficulty": parsed.difficulty,
        "scenario": asdict(scenario),
        "lab": asdict(lab),
        "safety": "ALLOWED (sandbox-only)",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="storm-forge")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("one-click", "narrate", "teleprompter"):
        p = sub.add_parser(name)
        p.add_argument("objective")
    args = parser.parse_args(argv)

    if args.command == "one-click":
        print(json.dumps(_run_pipeline(args.objective), indent=2))
    elif args.command == "narrate":
        print(video_narrate.script(args.objective))
    elif args.command == "teleprompter":
        print(lab_teleprompter.cues(args.objective))
    return 0


if __name__ == "__main__":
    sys.exit(main())
