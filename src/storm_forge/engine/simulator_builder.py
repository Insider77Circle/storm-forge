"""Simulator Builder — scenario -> sandbox spec.

This module produces a SPEC, not infrastructure. Nothing here provisions
a host, touches a network, or runs an exploit — the backend that
materializes the spec is a TODO for the owner. Keeping the spec pure
data is what lets the Safety Filter vet a lab before anything runs.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from storm_forge.engine.scenario_gen import Scenario


@dataclass
class Lab:
    id: str
    title: str
    hosts: list[dict] = field(default_factory=list)
    services: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    telemetry: list[str] = field(default_factory=list)
    sandbox_only: bool = True


def build_lab(scenario: Scenario) -> Lab:
    """Build a sandbox spec for a scenario."""
    lab_id = f"lab-{abs(hash(scenario.title)) % 100000}"
    return Lab(
        id=lab_id,
        title=scenario.title,
        hosts=[
            {"name": "workstation-01", "os": "windows-11", "role": "target"},
            {"name": "dc-01", "os": "windows-server", "role": "domain-controller"},
        ],
        services=["sysmon", "windows-event-log", "zeek"],
        artifacts=["process-tree", "auth-logs", "network-flows"],
        telemetry=["sysmon", "security-event-log"],
        sandbox_only=True,
    )
