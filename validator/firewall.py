"""The validation layer under study.

Returns a decision for each packet:
    ALLOW   nothing detected, packet forwarded
    BLOCK   detection, packet stopped (enforcing mode)
    FLAG    detection, packet forwarded anyway (LOG_ONLY mode)

Client guidance: the filter never edits a packet. Stripping the canary and
forwarding the remainder leaves the packet in an undefined state that the MCP
server would still act on. Block, or log and forward - never sanitize.
"""
import json, pathlib
from jsonschema import Draft202012Validator
from . import config, defenses

ROOT = pathlib.Path(__file__).resolve().parent.parent
_cache = {}


def load_schema(tool):
    key = (config.SCHEMA_SET, tool)
    if key not in _cache:
        base = ROOT / "schemas" / ("tight" if config.SCHEMA_SET == "tight" else "")
        _cache[key] = json.loads((base / f"{tool}.json").read_text())
    return _cache[key]


def detect(payload, tool):
    """Return a reason string if something was detected, else None."""
    if config.DEFENSES.get("schema", True):
        errors = sorted(Draft202012Validator(load_schema(tool)).iter_errors(payload),
                        key=lambda e: list(e.path))
        if errors:
            return f"schema[{config.SCHEMA_SET}]: {errors[0].message}"

    for name, enabled in config.DEFENSES.items():
        if name == "schema" or not enabled:
            continue
        reason = defenses.REGISTRY[name](payload, tool)
        if reason:
            return reason
    return None


def firewall(payload, tool):
    """Return (decision, reason, forwarded)."""
    reason = detect(payload, tool)
    if reason is None:
        return "ALLOW", "", True
    if config.LOG_ONLY:
        return "FLAG", reason, True        # detected, but still forwarded
    return "BLOCK", reason, False
