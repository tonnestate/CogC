#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / ".github" / "skills" / "cogc" / "scripts"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

from cogc.core import compile_request
from cogc.models import CompileRequest
from cogc.profiles import get_profile


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic CogC offline fidelity/compression eval")
    parser.add_argument("--dataset", default="evals/datasets/smoke.jsonl")
    args = parser.parse_args()

    failures = 0
    rows = []
    for line in (ROOT / args.dataset).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        request_data = json.loads((ROOT / case["request"]).read_text(encoding="utf-8"))
        request = CompileRequest.from_dict(request_data)
        request.target = get_profile(case["profile"])
        if request_data.get("token_budget") is not None:
            request.token_budget = int(request_data["token_budget"])
        package = compile_request(request)
        passed = package.fidelity.passed == bool(case.get("expect_fidelity", True))
        if "max_ratio" in case:
            passed = passed and package.receipt.compression_ratio <= float(case["max_ratio"])
        if not passed:
            failures += 1
        rows.append({
            "id": case["id"],
            "passed": passed,
            "fidelity": package.fidelity.passed,
            "ratio": round(package.receipt.compression_ratio, 4),
            "source_tokens_est": package.receipt.source_token_estimate,
            "compiled_tokens_est": package.receipt.compiled_token_estimate,
        })

    print(json.dumps({"cases": rows, "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
