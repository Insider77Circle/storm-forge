"""MITRE ATT&CK — labs mapped to techniques.

TODO (owner): import the real ATT&CK dataset (STIX/TAXII or the JSON
release) and replace this demo table. The function shape — technique
id -> lab focus — is the contract.
"""

from __future__ import annotations

_TECHNIQUES = {
    "T1003.001": "OS Credential Dumping: LSASS Memory",
    "T1566.001": "Phishing: Spearphishing Attachment",
    "T1486": "Data Encrypted for Impact",
    "T1021.002": "Remote Services: SMB/Windows Admin Shares",
    "T1053.005": "Scheduled Task/Job: Scheduled Task",
}


def describe(technique_id: str) -> str:
    """Return the ATT&CK name for a technique id (demo table)."""
    return _TECHNIQUES.get(technique_id, f"Unknown technique {technique_id}")


def lab_for(technique_id: str) -> str:
    """Return a one-line lab focus for a technique id."""
    return f"Lab: {describe(technique_id)} — sandbox-only emulation."
