from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import compile_request
from .io import read_json, write_json
from .models import CompileRequest
from .profiles import BUILTIN_PROFILES, get_profile
from .render import render_package


def _load_request(path: str, profile: str | None, budget: int | None) -> CompileRequest:
    data = read_json(path)
    request = CompileRequest.from_dict(data)
    if profile:
        request.target = get_profile(profile)
    if budget:
        request.token_budget = budget
    return request


def cmd_compile(args: argparse.Namespace) -> int:
    request = _load_request(args.input, args.profile, args.budget)
    package = compile_request(request)
    if args.format == "json":
        payload = package.to_dict()
        if args.output:
            write_json(args.output, payload)
        else:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        text = render_package(package, include_receipt=args.receipt)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    if not package.fidelity.passed:
        print("CogC fidelity gate FAILED", file=sys.stderr)
        return 2
    return 0


def cmd_profiles(_args: argparse.Namespace) -> int:
    for name, profile in sorted(BUILTIN_PROFILES.items()):
        print(f"{name}\tbudget={profile.context_budget}\treasoning={profile.open_ended_reasoning}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    request = _load_request(args.input, args.profile, args.budget)
    package = compile_request(request)
    report = package.fidelity.to_dict()
    report["compression_ratio"] = package.receipt.compression_ratio
    report["source_token_estimate"] = package.receipt.source_token_estimate
    report["compiled_token_estimate"] = package.receipt.compiled_token_estimate
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if package.fidelity.passed else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cogc", description="Capacity-Aware Cognitive Compression")
    parser.add_argument("--version", action="version", version="CogC 0.2.0")
    sub = parser.add_subparsers(dest="command", required=True)

    compile_p = sub.add_parser("compile", help="Compile raw context into a Cognitive Package")
    compile_p.add_argument("--input", "-i", required=True, help="Compile-request JSON")
    compile_p.add_argument("--output", "-o", help="Output file; stdout if omitted")
    compile_p.add_argument("--profile", choices=sorted(BUILTIN_PROFILES), help="Override target profile")
    compile_p.add_argument("--budget", type=int, help="Override token budget estimate")
    compile_p.add_argument("--format", choices=["text", "json"], default="text")
    compile_p.add_argument("--receipt", action="store_true", help="Include receipt in text output")
    compile_p.set_defaults(func=cmd_compile)

    validate_p = sub.add_parser("validate", help="Compile and print fidelity metrics")
    validate_p.add_argument("--input", "-i", required=True)
    validate_p.add_argument("--profile", choices=sorted(BUILTIN_PROFILES))
    validate_p.add_argument("--budget", type=int)
    validate_p.set_defaults(func=cmd_validate)

    profiles_p = sub.add_parser("profiles", help="List built-in target profiles")
    profiles_p.set_defaults(func=cmd_profiles)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
