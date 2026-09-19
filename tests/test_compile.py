from __future__ import annotations

import json
from pathlib import Path

from cogc.core import compile_request
from cogc.models import CompileRequest
from cogc.render import render_package

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> CompileRequest:
    data = json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))
    return CompileRequest.from_dict(data)


def test_repository_example_preserves_critical_fields() -> None:
    package = compile_request(load("repository-analysis.json"))
    text = render_package(package)
    assert package.fidelity.passed
    assert "100 EUR" in text
    assert "EV-481" in text
    assert "OWN-001" in package.source_map
    assert package.procedure is not None
    assert package.procedure.id == "WF-OSS-005"


def test_exact_duplicate_is_collapsed_but_sources_remain() -> None:
    package = compile_request(load("repository-analysis.json"))
    units = package.immutable + package.facts
    bg = [u for u in units if u.id == "BG-001"]
    assert len(bg) <= 1
    if bg:
        assert "BG-002" in bg[0].source_refs


def test_noise_is_not_selected() -> None:
    package = compile_request(load("repository-analysis.json"))
    selected_ids = {u.id for u in package.immutable + package.facts}
    assert "NOISE-001" not in selected_ids


def test_handoff_retains_case_identifier_and_date() -> None:
    package = compile_request(load("company-handoff.json"))
    text = render_package(package)
    assert package.fidelity.passed
    assert "CASE-2041" in text
    assert "2026-09-18" in text
