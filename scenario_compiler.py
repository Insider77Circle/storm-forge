"""Scenario compiler — natural-language objective -> structured,
technically realistic environment spec.

This is the v2 path over Parser + Scenario Gen + Simulator Builder:
instead of a narrative lab plus a loose host list, the compiler emits a
full environment: private networks, hosts with OS/services/vulns, users,
and telemetry. The spec is still pure data — nothing is provisioned
here. See orchestration/ for the provider that materializes it.
"""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field

from storm_forge.engine import generate_scenario, parse

_PRIVATE_NETS = ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")


@dataclass
class ServiceSpec:
    name: str
    port: int
    version: str = ""


@dataclass
class VulnSpec:
    id: str  # CVE or technique-linked weakness id
    technique_id: str
    severity: str = "medium"  # low | medium | high | critical


@dataclass
class HostSpec:
    name: str
    os: str
    role: str
    services: list[ServiceSpec] = field(default_factory=list)
    vulnerabilities: list[VulnSpec] = field(default_factory=list)
    users: list[str] = field(default_factory=list)


@dataclass
class NetworkSpec:
    name: str
    cidr: str
    hosts: list[HostSpec] = field(default_factory=list)


@dataclass
class EnvironmentSpec:
    objective: str
    track: str
    difficulty: int
    mitre_techniques: list[str]
    networks: list[NetworkSpec] = field(default_factory=list)
    telemetry: list[str] = field(default_factory=list)


# Demo catalog: skill -> topology fragment. Replace with a real
# vulnerability/service dataset when the compiler grows up.
_CATALOG = {
    "credential-access": {
        "hosts": [
            HostSpec(
                name="workstation-01",
                os="windows-11",
                role="target",
                services=[ServiceSpec("smb", 445, "3.1.1")],
                vulnerabilities=[VulnSpec("LSASS-memory", "T1003.001", "high")],
                users=["analyst", "helpdesk"],
            ),
            HostSpec(
                name="dc-01",
                os="windows-server-2022",
                role="domain-controller",
                services=[
                    ServiceSpec("kerberos", 88),
                    ServiceSpec("ldap", 389),
                ],
                users=["administrator"],
            ),
        ],
        "telemetry": ["sysmon", "security-event-log", "zeek"],
    },
}


def _check_private(cidr: str) -> None:
    net = ipaddress.ip_network(cidr)
    if not any(net.subnet_of(ipaddress.ip_network(p)) for p in _PRIVATE_NETS):
        raise ValueError(f"refusing non-private range in lab spec: {cidr}")


def compile_objective(objective: str) -> EnvironmentSpec:
    """Compile a plain-English objective into an environment spec."""
    parsed = parse(objective)
    scenario = generate_scenario(parsed)
    fragment = _CATALOG.get(
        parsed.skill,
        {
            "hosts": [
                HostSpec(name="workstation-01", os="windows-11", role="target")
            ],
            "telemetry": ["sysmon"],
        },
    )
    network = NetworkSpec(name="lab-net", cidr="10.20.0.0/24", hosts=fragment["hosts"])
    _check_private(network.cidr)
    return EnvironmentSpec(
        objective=parsed.raw,
        track=parsed.track,
        difficulty=parsed.difficulty,
        mitre_techniques=parsed.mitre_techniques,
        networks=[network],
        telemetry=fragment["telemetry"],
    )
