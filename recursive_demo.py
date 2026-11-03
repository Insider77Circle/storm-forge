"""Recursive demo — the full loop in one run.

Lab -> attempts -> learner profile -> weakest skill -> recursive next
lab, with the adaptive adversary reacting to each defender event.
"""

from storm_forge.adversary import AdversaryEngine, DefenderEvent
from storm_forge.compiler import compile_objective
from storm_forge.learner import AttemptRecord, LearnerStore
from storm_forge.orchestration import DryRunProvider
from storm_forge.recursion import next_lab

if __name__ == "__main__":
    spec = compile_objective("detect LSASS credential dumping")
    print(f"Lab 1: {spec.objective} (difficulty {spec.difficulty})")
    print(f"  hosts: {[h.name for n in spec.networks for h in n.hosts]}")

    handle = DryRunProvider().provision(spec)

    store = LearnerStore()
    store.record(
        AttemptRecord("credential-access", False, 420.0, ["MISSED_TELEMETRY"], False)
    )
    store.record(
        AttemptRecord("credential-access", False, 380.0, ["SLOW_TRIAGE"], False)
    )
    print(f"Profile: {store.summary('credential-access')}")
    print(f"Weaknesses: {store.weaknesses()}")

    lab2 = next_lab(store, current_difficulty=spec.difficulty)
    print(f"Lab 2 (recursive): {lab2['objective']}")
    print(f"  rationale: {lab2['rationale']}")

    adversary = AdversaryEngine("T1003.001")
    for event in (
        DefenderEvent("detected", "T1003.001"),
        DefenderEvent("blocked", "T1003.001"),
        DefenderEvent("missed", "T1003.001"),
    ):
        print(f"Adversary: {adversary.observe(event)}")

    DryRunProvider().teardown(handle)
