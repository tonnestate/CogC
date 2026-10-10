from __future__ import annotations

from .models import TargetProfile

BUILTIN_PROFILES: dict[str, TargetProfile] = {
    "generic-small-agent": TargetProfile(
        name="generic-small-agent",
        context_budget=4096,
        instruction_depth="low",
        open_ended_reasoning="low",
        schema_adherence="medium",
        ambiguity_tolerance="low",
        notes=["Prefer explicit procedures and stop conditions."],
    ),
    "qwen-4b": TargetProfile(
        name="qwen-4b",
        context_budget=4096,
        instruction_depth="low",
        open_ended_reasoning="low",
        schema_adherence="high",
        ambiguity_tolerance="low",
        notes=["Keep one task boundary, explicit next action, compact evidence references."],
    ),
    "qwen-9b": TargetProfile(
        name="qwen-9b",
        context_budget=8192,
        instruction_depth="medium",
        open_ended_reasoning="medium",
        schema_adherence="high",
        ambiguity_tolerance="medium",
        notes=["Can retain broader evidence and limited alternatives."],
    ),
    "frontier-specialist": TargetProfile(
        name="frontier-specialist",
        context_budget=16000,
        instruction_depth="high",
        open_ended_reasoning="high",
        schema_adherence="high",
        ambiguity_tolerance="high",
        notes=["Preserve contradictions and richer source context."],
    ),
}


def get_profile(name: str) -> TargetProfile:
    key = name.strip().lower()
    if key not in BUILTIN_PROFILES:
        raise KeyError(f"Unknown profile {name!r}. Available: {', '.join(sorted(BUILTIN_PROFILES))}")
    p = BUILTIN_PROFILES[key]
    return TargetProfile(
        name=p.name,
        context_budget=p.context_budget,
        instruction_depth=p.instruction_depth,
        open_ended_reasoning=p.open_ended_reasoning,
        schema_adherence=p.schema_adherence,
        ambiguity_tolerance=p.ambiguity_tolerance,
        notes=list(p.notes),
    )
