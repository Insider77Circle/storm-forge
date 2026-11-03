"""Engine package: the six panels of the FRONTIER AI LESSON ENGINE."""

from storm_forge.engine.parser import parse
from storm_forge.engine.scenario_gen import generate_scenario
from storm_forge.engine.simulator_builder import build_lab
from storm_forge.engine.safety_filter import check_lab
from storm_forge.engine.adaptive_diff import next_difficulty
from storm_forge.engine.analyst_mode import debrief

__all__ = [
    "parse",
    "generate_scenario",
    "build_lab",
    "check_lab",
    "next_difficulty",
    "debrief",
]
