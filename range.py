"""Live cyber-range orchestration — provider interface + dry-run only.

The skeleton NEVER provisions real infrastructure by default. The
provider interface is the contract; DryRunProvider prints the plan and
provisions nothing. A real backend (Docker/KVM) must implement this
interface plus the guards below:

- Isolated private network only (compiler already enforces RFC1918).
- No egress from the range to the internet or the host LAN.
- Red-team sandboxes get no credentials and no outbound paths.
- Every provision is paired with a teardown; ranges are ephemeral.
- Provisioning is opt-in and explicit — never a side effect of
  generating a lab.

TODO (owner): implement DockerProvider behind these guards.
"""

from __future__ import annotations

from dataclasses import dataclass

from storm_forge.compiler import EnvironmentSpec


@dataclass
class RangeHandle:
    id: str
    spec_objective: str
    status: str  # "planned" | "running" | "torn-down"
    host_count: int


class RangeProvider:
    """Interface a real range backend must implement."""

    def provision(self, spec: EnvironmentSpec) -> RangeHandle:
        raise NotImplementedError

    def teardown(self, handle: RangeHandle) -> RangeHandle:
        raise NotImplementedError

    def status(self, handle: RangeHandle) -> str:
        raise NotImplementedError


class DryRunProvider(RangeProvider):
    """Prints the provisioning plan. Provisions nothing."""

    def provision(self, spec: EnvironmentSpec) -> RangeHandle:
        hosts = sum(len(n.hosts) for n in spec.networks)
        print(f"[dry-run] would provision {hosts} host(s) on isolated net(s):")
        for net in spec.networks:
            print(f"  net {net.name} {net.cidr}")
            for host in net.hosts:
                svcs = ", ".join(s.name for s in host.services) or "none"
                print(f"    {host.name} ({host.os}, {host.role}) services: {svcs}")
        print("[dry-run] egress: DENIED, teardown: REQUIRED, status: planned")
        return RangeHandle(
            id="dryrun-0001",
            spec_objective=spec.objective,
            status="planned",
            host_count=hosts,
        )

    def teardown(self, handle: RangeHandle) -> RangeHandle:
        handle.status = "torn-down"
        print(f"[dry-run] tore down {handle.id} (nothing was provisioned)")
        return handle

    def status(self, handle: RangeHandle) -> str:
        return handle.status
