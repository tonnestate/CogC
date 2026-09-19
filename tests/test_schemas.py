from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from cogc.core import compile_request
from cogc.models import CompileRequest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "skill" / "cogc" / "schemas"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_example_request_validates() -> None:
    schema = _load(SCHEMAS / "compile-request.schema.json")
    request = _load(ROOT / "examples" / "repository-analysis.json")
    jsonschema.Draft202012Validator(schema).validate(request)


def test_compiled_package_validates() -> None:
    schema = _load(SCHEMAS / "cognitive-package.schema.json")
    request = CompileRequest.from_dict(_load(ROOT / "examples" / "repository-analysis.json"))
    package = compile_request(request).to_dict()
    jsonschema.Draft202012Validator(schema).validate(package)


def test_receipt_validates() -> None:
    schema = _load(SCHEMAS / "compression-receipt.schema.json")
    request = CompileRequest.from_dict(_load(ROOT / "examples" / "repository-analysis.json"))
    receipt = compile_request(request).receipt.to_dict()
    jsonschema.Draft202012Validator(schema).validate(receipt)
