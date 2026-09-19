from __future__ import annotations

from .models import CIRUnit, CognitivePackage, Procedure


def _render_units(title: str, units: list[CIRUnit]) -> list[str]:
    if not units:
        return []
    lines = [title]
    for unit in units:
        refs = ",".join(unit.source_refs)
        lines.append(f"- [{unit.criticality.short}] {unit.text} <{refs}>")
    return lines


def _render_procedure(procedure: Procedure | None) -> list[str]:
    if not procedure:
        return []
    lines = [f"PROCEDURE {procedure.id} — {procedure.title}"]
    for i, step in enumerate(procedure.steps, 1):
        lines.append(f"{i}. {step}")
    return lines


def render_package(package: CognitivePackage, include_receipt: bool = False) -> str:
    lines = [
        "COGC COGNITIVE PACKAGE",
        f"TARGET: {package.target_profile}",
        "",
        "GOAL",
        package.goal,
        "",
        "TASK",
        package.task,
        "",
    ]
    lines.extend(_render_units("IMMUTABLE / CRITICAL", package.immutable))
    if package.immutable:
        lines.append("")
    lines.extend(_render_units("RELEVANT STATE", package.facts))
    if package.facts:
        lines.append("")
    proc_lines = _render_procedure(package.procedure)
    lines.extend(proc_lines)
    if proc_lines:
        lines.append("")
    if package.success_conditions:
        lines.append("SUCCESS CONDITIONS")
        lines.extend(f"- {x}" for x in package.success_conditions)
        lines.append("")
    if package.stop_conditions:
        lines.append("STOP / ESCALATION CONDITIONS")
        lines.extend(f"- {x}" for x in package.stop_conditions)
        lines.append("")
    if package.expandable:
        lines.append("EXPANDABLE SOURCE HANDLES")
        lines.extend(f"- {key}" for key in sorted(package.expandable))
    if include_receipt:
        lines.extend([
            "",
            "COMPRESSION RECEIPT",
            f"- source_tokens_est: {package.receipt.source_token_estimate}",
            f"- compiled_tokens_est: {package.receipt.compiled_token_estimate}",
            f"- compression_ratio: {package.receipt.compression_ratio:.3f}",
            f"- fidelity_passed: {package.fidelity.passed}",
        ])
    return "\n".join(lines).strip() + "\n"
