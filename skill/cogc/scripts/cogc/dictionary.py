from __future__ import annotations

COGNITIVE_DICTIONARY: dict[str, tuple[str, tuple[str, ...]]] = {
    "CGC-001": ("REUSE_BEFORE_BUILD", ("reuse before build", "reuse-first", "reuse first")),
    "CGC-002": ("SOURCE_INSPECTION_REQUIRED", ("inspect source", "source inspection", "read the source")),
    "CGC-003": ("RUNTIME_PROOF_REQUIRED", ("runtime proof", "real verification", "runtime evidence")),
    "CGC-004": ("EXTERNAL_ACTION_RECEIPT_REQUIRED", ("external action receipt", "receipt required")),
    "CGC-005": ("OWNER_APPROVAL_REQUIRED", ("owner approval", "owner gate")),
    "CGC-006": ("CONTRADICTORY_EVIDENCE", ("contradictory evidence", "conflicting evidence")),
    "CGC-007": ("PROVIDER_DEGRADED", ("provider degraded", "degraded provider")),
    "CGC-008": ("ESCALATION_REQUIRED", ("escalation required", "must escalate")),
}


def detect_dictionary_refs(texts: list[str]) -> list[str]:
    haystack = "\n".join(texts).lower()
    found: list[str] = []
    for code, (_label, patterns) in COGNITIVE_DICTIONARY.items():
        if any(pattern in haystack for pattern in patterns):
            found.append(code)
    return found
