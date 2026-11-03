"""STORM FORGE (skeleton).

Pipeline: objective -> Parser -> Scenario Gen -> Simulator Builder
-> Safety Filter -> Lab -> Analyst Mode -> Adaptive Diff -> next Lab.

Red-team tracks are SIMULATED OFFENSE inside a sandbox only. The safety
filter is load-bearing: anything that points at a real system never builds.
"""

from storm_forge.engine.parser import ParsedObjective, parse
from storm_forge.engine.scenario_gen import Scenario, generate_scenario
from storm_forge.engine.simulator_builder import Lab, build_lab
from storm_forge.engine.safety_filter import SafetyVerdict, check_lab

__version__ = "0.1.0"
__all__ = [
    "ParsedObjective",
    "Scenario",
    "Lab",
    "SafetyVerdict",
    "parse",
    "generate_scenario",
    "build_lab",
    "check_lab",
]
