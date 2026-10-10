from __future__ import annotations

from .models import Criticality, SourceItem

_IMMUTABLE_KINDS = {
    "owner_instruction", "authorization", "governance", "execution_boundary", "legal_constraint",
    "stop_condition", "payment_limit", "security_constraint",
}
_CRITICAL_KINDS = {
    "constraint", "requirement", "evidence", "identifier", "current_state", "success_condition",
    "decision", "receipt",
}
_NOISE_KINDS = {"chitchat", "style", "boilerplate", "noise"}

_IMMUTABLE_TERMS = (
    "must not", "must never", "owner approval", "kill", "freeze", "pause", "authorization",
    "do not execute", "payment limit", "execution boundary", "darf nicht", "niemals", "freigabe",
)
_CRITICAL_TERMS = (
    "must", "required", "constraint", "evidence", "receipt", "deadline", "success condition",
    "stop condition", "requirement", "muss", "erforderlich", "beleg", "nachweis",
)


def classify(item: SourceItem) -> Criticality:
    if item.criticality is not None:
        return item.criticality

    kind = item.kind.strip().lower()
    text = item.text.lower()
    if kind in _IMMUTABLE_KINDS:
        return Criticality.C0_IMMUTABLE
    if kind in _CRITICAL_KINDS:
        return Criticality.C1_CRITICAL
    if kind in _NOISE_KINDS:
        return Criticality.C5_NOISE
    if kind in {"procedure", "workflow", "fact", "observation", "tool_state"}:
        return Criticality.C2_HIGH_VALUE
    if kind in {"background", "history", "supporting"}:
        return Criticality.C3_SUPPORTING
    if any(term in text for term in _IMMUTABLE_TERMS):
        return Criticality.C0_IMMUTABLE
    if any(term in text for term in _CRITICAL_TERMS):
        return Criticality.C1_CRITICAL
    return Criticality.C3_SUPPORTING
