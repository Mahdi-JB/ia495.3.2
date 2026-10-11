"""Semantic defenses layered on top of schema validation.

Each returns None (pass) or a reason string (detection).

NOTE on approach, from the 2026-10-09 client meeting: allow-listing beats
deny-listing. Specifying exactly what a field MAY contain (see schemas/tight/)
is the preferred direction. `instruction_screen` below is a DENY-LIST and is
kept deliberately, as the naive approach we measure and report the limits of.
"""
from . import config

FREE_TEXT_FIELDS = {"body", "text", "filter", "title", "subject"}


def _strings(payload):
    for field in FREE_TEXT_FIELDS:
        value = payload.get(field)
        if isinstance(value, str):
            yield field, value


def length_cap(payload, tool):
    for field, value in _strings(payload):
        if len(value) > config.MAX_FREE_TEXT:
            return f"length_cap: '{field}' is {len(value)} chars (max {config.MAX_FREE_TEXT})"
    return None


def allow_list(payload, tool):
    if tool == "send_email" and payload.get("to") not in config.APPROVED_RECIPIENTS:
        return f"allow_list: recipient {payload.get('to')!r} is not approved"
    if tool == "create_event":
        for a in payload.get("attendees", []):
            if a not in config.APPROVED_RECIPIENTS:
                return f"allow_list: attendee {a!r} is not approved"
    return None


def instruction_screen(payload, tool):
    """DENY-LIST. Measured, not recommended. Evadable by rephrasing or by
    inserting zero-width characters - which is the point we report."""
    for field, value in _strings(payload):
        low = value.lower()
        for pattern in config.INSTRUCTION_PATTERNS:
            if pattern in low:
                return f"instruction_screen: '{field}' contains {pattern!r}"
    return None


REGISTRY = {
    "length_cap": length_cap,
    "allow_list": allow_list,
    "instruction_screen": instruction_screen,
}
