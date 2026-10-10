from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import IntEnum
from typing import Any


class Criticality(IntEnum):
    """Lower numeric values are more important and less compressible."""

    C0_IMMUTABLE = 0
    C1_CRITICAL = 1
    C2_HIGH_VALUE = 2
    C3_SUPPORTING = 3
    C4_REDUNDANT = 4
    C5_NOISE = 5

    @classmethod
    def parse(cls, value: str | int | None) -> "Criticality | None":
        if value is None:
            return None
        if isinstance(value, int):
            return cls(value)
        normalized = str(value).strip().upper().replace("-", "_")
        aliases = {
            "C0": cls.C0_IMMUTABLE,
            "C0_IMMUTABLE": cls.C0_IMMUTABLE,
            "IMMUTABLE": cls.C0_IMMUTABLE,
            "C1": cls.C1_CRITICAL,
            "C1_CRITICAL": cls.C1_CRITICAL,
            "CRITICAL": cls.C1_CRITICAL,
            "C2": cls.C2_HIGH_VALUE,
            "C2_HIGH_VALUE": cls.C2_HIGH_VALUE,
            "HIGH": cls.C2_HIGH_VALUE,
            "HIGH_VALUE": cls.C2_HIGH_VALUE,
            "C3": cls.C3_SUPPORTING,
            "C3_SUPPORTING": cls.C3_SUPPORTING,
            "SUPPORTING": cls.C3_SUPPORTING,
            "C4": cls.C4_REDUNDANT,
            "C4_REDUNDANT": cls.C4_REDUNDANT,
            "REDUNDANT": cls.C4_REDUNDANT,
            "C5": cls.C5_NOISE,
            "C5_NOISE": cls.C5_NOISE,
            "NOISE": cls.C5_NOISE,
        }
        if normalized not in aliases:
            raise ValueError(f"Unknown criticality: {value}")
        return aliases[normalized]

    @property
    def short(self) -> str:
        return f"C{int(self)}"


@dataclass(slots=True)
class SourceItem:
    id: str
    text: str
    kind: str = "context"
    criticality: Criticality | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceItem":
        return cls(
            id=str(data["id"]),
            text=str(data.get("text", "")),
            kind=str(data.get("kind", "context")),
            criticality=Criticality.parse(data.get("criticality")),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass(slots=True)
class TargetProfile:
    name: str = "generic-small-agent"
    context_budget: int = 4096
    instruction_depth: str = "low"
    open_ended_reasoning: str = "low"
    schema_adherence: str = "medium"
    ambiguity_tolerance: str = "low"
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "TargetProfile":
        data = data or {}
        return cls(
            name=str(data.get("name", "generic-small-agent")),
            context_budget=int(data.get("context_budget", 4096)),
            instruction_depth=str(data.get("instruction_depth", "low")),
            open_ended_reasoning=str(data.get("open_ended_reasoning", "low")),
            schema_adherence=str(data.get("schema_adherence", "medium")),
            ambiguity_tolerance=str(data.get("ambiguity_tolerance", "low")),
            notes=list(data.get("notes", [])),
        )


@dataclass(slots=True)
class Procedure:
    id: str
    title: str
    steps: list[str]
    triggers: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Procedure":
        return cls(
            id=str(data["id"]),
            title=str(data.get("title", data["id"])),
            steps=[str(v) for v in data.get("steps", [])],
            triggers=[str(v) for v in data.get("triggers", [])],
            source_refs=[str(v) for v in data.get("source_refs", [])],
        )


@dataclass(slots=True)
class CompileRequest:
    goal: str
    task: str
    sources: list[SourceItem]
    target: TargetProfile = field(default_factory=TargetProfile)
    token_budget: int | None = None
    success_conditions: list[str] = field(default_factory=list)
    stop_conditions: list[str] = field(default_factory=list)
    procedures: list[Procedure] = field(default_factory=list)
    policy: str = "deterministic"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CompileRequest":
        target = TargetProfile.from_dict(data.get("target"))
        return cls(
            goal=str(data.get("goal", "")),
            task=str(data.get("task", "")),
            sources=[SourceItem.from_dict(x) for x in data.get("sources", [])],
            target=target,
            token_budget=(int(data["token_budget"]) if data.get("token_budget") is not None else None),
            success_conditions=[str(v) for v in data.get("success_conditions", [])],
            stop_conditions=[str(v) for v in data.get("stop_conditions", [])],
            procedures=[Procedure.from_dict(x) for x in data.get("procedures", [])],
            policy=str(data.get("policy", "deterministic")),
        )


@dataclass(slots=True)
class CIRUnit:
    id: str
    text: str
    kind: str
    criticality: Criticality
    source_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)
    score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["criticality"] = self.criticality.short
        return data


@dataclass(slots=True)
class FidelityReport:
    passed: bool
    critical_retention: float
    exact_number_retention: float
    exact_identifier_retention: float
    missing_critical_ids: list[str] = field(default_factory=list)
    missing_numbers: list[str] = field(default_factory=list)
    missing_identifiers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CompressionReceipt:
    version: str
    policy: str
    target_profile: str
    source_units: int
    cir_units: int
    kept_units: int
    source_token_estimate: int
    compiled_token_estimate: int
    compression_ratio: float
    source_state_hash: str
    dictionary_refs: list[str] = field(default_factory=list)
    over_budget_due_to_critical: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CognitivePackage:
    goal: str
    task: str
    target_profile: str
    immutable: list[CIRUnit]
    facts: list[CIRUnit]
    procedure: Procedure | None
    success_conditions: list[str]
    stop_conditions: list[str]
    expandable: dict[str, str]
    source_map: dict[str, list[str]]
    receipt: CompressionReceipt
    fidelity: FidelityReport

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "task": self.task,
            "target_profile": self.target_profile,
            "immutable": [x.to_dict() for x in self.immutable],
            "facts": [x.to_dict() for x in self.facts],
            "procedure": asdict(self.procedure) if self.procedure else None,
            "success_conditions": self.success_conditions,
            "stop_conditions": self.stop_conditions,
            "expandable": self.expandable,
            "source_map": self.source_map,
            "receipt": self.receipt.to_dict(),
            "fidelity": self.fidelity.to_dict(),
        }
