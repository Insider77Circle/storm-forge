"""STORM FORGE quickstart — one objective through the whole pipeline."""

import json

from storm_forge.modules import one_click
from storm_forge.teams import blue_team

if __name__ == "__main__":
    result = one_click.run(blue_team.preset(0))
    print(f"Objective: {result['objective']}")
    print(f"Track: {result['track']}")
    print(f"Scenario: {result['scenario'].title}")
    print(f"Lab: {result['lab'].id} (sandbox-only: {result['lab'].sandbox_only})")
    print(f"Safety: {'ALLOWED' if result['safety_allowed'] else 'BLOCKED'}")
    print(json.dumps(result["lab"].__dict__, indent=2, default=str))
