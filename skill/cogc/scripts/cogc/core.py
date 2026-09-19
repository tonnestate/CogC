from __future__ import annotations

from dataclasses import replace

from .criticality import classify
from .dictionary import detect_dictionary_refs
from .fidelity import verify_fidelity
from .models import (
    CIRUnit,
    CognitivePackage,
    CompileRequest,
    CompressionReceipt,
    Criticality,
    Procedure,
)
from .render import render_package
from .utils import canonicalize, content_hash, estimate_tokens, keyword_set, sentence_split

VERSION = "0.2.0"


def _build_cir(request: CompileRequest) -> list[CIRUnit]:
    units: list[CIRUnit] = []
    seen: dict[str, CIRUnit] = {}
    for item in request.sources:
        text = canonicalize(item.text)
        if not text:
            continue
        key = text.casefold()
        if key in seen:
            existing = seen[key]
            if item.id not in existing.source_refs:
                existing.source_refs.append(item.id)
            existing.metadata.setdefault("deduplicated_sources", []).append(item.id)
            continue
        unit = CIRUnit(
            id=item.id,
            text=text,
            kind=item.kind,
            criticality=classify(item),
            source_refs=[item.id],
            metadata=dict(item.metadata),
        )
        units.append(unit)
        seen[key] = unit
    return units


def _score_units(units: list[CIRUnit], request: CompileRequest) -> list[CIRUnit]:
    query = keyword_set(f"{request.goal} {request.task} {' '.join(request.success_conditions)}")
    out: list[CIRUnit] = []
    for index, unit in enumerate(units):
        overlap = len(keyword_set(unit.text) & query)
        critical_bonus = {0: 100.0, 1: 60.0, 2: 25.0, 3: 8.0, 4: 2.0, 5: 0.0}[int(unit.criticality)]
        recency_bonus = max(0.0, 2.0 - index * 0.01)
        kind_bonus = 5.0 if unit.kind.lower() in {"workflow", "procedure", "evidence", "current_state"} else 0.0
        out.append(replace(unit, score=critical_bonus + overlap * 5.0 + recency_bonus + kind_bonus))
    return out


def _select_procedure(request: CompileRequest) -> Procedure | None:
    if not request.procedures:
        return None
    query = keyword_set(f"{request.goal} {request.task}")
    ranked: list[tuple[int, Procedure]] = []
    for proc in request.procedures:
        corpus = keyword_set(f"{proc.title} {' '.join(proc.triggers)} {' '.join(proc.steps)}")
        ranked.append((len(query & corpus), proc))
    ranked.sort(key=lambda x: (x[0], x[1].id), reverse=True)
    if ranked[0][0] == 0 and len(request.procedures) > 1:
        return None
    return ranked[0][1]


def _extractive_shorten(unit: CIRUnit, query: set[str], max_tokens: int) -> CIRUnit:
    if estimate_tokens(unit.text) <= max_tokens or int(unit.criticality) <= 1:
        return unit
    sentences = sentence_split(unit.text)
    if len(sentences) <= 1:
        return unit
    scored: list[tuple[float, int, str]] = []
    for idx, sentence in enumerate(sentences):
        overlap = len(keyword_set(sentence) & query)
        scored.append((overlap * 5.0 + (1.0 if idx == 0 else 0.0), idx, sentence))
    scored.sort(reverse=True)
    chosen: list[tuple[int, str]] = []
    used = 0
    for _score, idx, sentence in scored:
        t = estimate_tokens(sentence)
        if chosen and used + t > max_tokens:
            continue
        chosen.append((idx, sentence))
        used += t
        if used >= max_tokens:
            break
    if not chosen:
        return unit
    chosen.sort()
    text = " ".join(sentence for _, sentence in chosen)
    meta = dict(unit.metadata)
    meta["extractively_shortened"] = True
    return replace(unit, text=text, metadata=meta)


def _fit_budget(units: list[CIRUnit], request: CompileRequest, reserved_tokens: int) -> tuple[list[CIRUnit], bool]:
    budget = request.token_budget or request.target.context_budget
    available = max(0, budget - reserved_tokens)
    critical = [u for u in units if int(u.criticality) <= 1]
    optional = [u for u in units if int(u.criticality) > 1 and u.criticality != Criticality.C5_NOISE]
    kept = list(critical)
    used = sum(estimate_tokens(u.text) for u in critical)
    over_budget = used > available
    if over_budget:
        return kept, True

    query = keyword_set(f"{request.goal} {request.task}")
    optional.sort(key=lambda u: (u.score, -int(u.criticality)), reverse=True)
    for unit in optional:
        remaining = available - used
        if remaining <= 0:
            break
        candidate = _extractive_shorten(unit, query, max_tokens=max(24, remaining))
        tokens = estimate_tokens(candidate.text)
        if tokens <= remaining:
            kept.append(candidate)
            used += tokens
    return kept, False


def compile_request(request: CompileRequest) -> CognitivePackage:
    cir = _score_units(_build_cir(request), request)
    procedure = _select_procedure(request)
    fixed_text = "\n".join([
        request.goal,
        request.task,
        *request.success_conditions,
        *request.stop_conditions,
        *(procedure.steps if procedure else []),
    ])
    reserved = estimate_tokens(fixed_text) + 80
    kept, over_budget = _fit_budget(cir, request, reserved)

    immutable = [u for u in kept if int(u.criticality) <= 1]
    facts = [u for u in kept if int(u.criticality) > 1]
    expandable = {u.id: u.text for u in cir if u.id not in {k.id for k in kept}}
    source_map = {u.id: list(u.source_refs) for u in kept}

    placeholder_receipt = CompressionReceipt(
        version=VERSION,
        policy=request.policy,
        target_profile=request.target.name,
        source_units=len(request.sources),
        cir_units=len(cir),
        kept_units=len(kept),
        source_token_estimate=sum(estimate_tokens(item.text) for item in request.sources) + reserved,
        compiled_token_estimate=0,
        compression_ratio=1.0,
        source_state_hash=content_hash([request.goal, request.task] + [u.text for u in cir]),
        dictionary_refs=detect_dictionary_refs([u.text for u in kept]),
        over_budget_due_to_critical=over_budget,
    )
    package = CognitivePackage(
        goal=request.goal,
        task=request.task,
        target_profile=request.target.name,
        immutable=immutable,
        facts=facts,
        procedure=procedure,
        success_conditions=list(request.success_conditions),
        stop_conditions=list(request.stop_conditions),
        expandable=expandable,
        source_map=source_map,
        receipt=placeholder_receipt,
        fidelity=None,  # type: ignore[arg-type]
    )
    rendered = render_package(package, include_receipt=False)
    fidelity = verify_fidelity(cir, kept, rendered)
    compiled_tokens = estimate_tokens(rendered)
    source_tokens = max(1, placeholder_receipt.source_token_estimate)
    receipt = replace(
        placeholder_receipt,
        compiled_token_estimate=compiled_tokens,
        compression_ratio=compiled_tokens / source_tokens,
    )
    package.receipt = receipt
    package.fidelity = fidelity
    return package
