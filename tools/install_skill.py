#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".github" / "skills" / "cogc"

TARGETS = {
    "github": ROOT / ".github" / "skills",
    "claude": ROOT / ".claude" / "skills",
    "agents": ROOT / ".agents" / "skills",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy the canonical CogC skill into a project skill directory without maintaining duplicate sources."
    )
    parser.add_argument(
        "--target",
        choices=sorted(TARGETS),
        help="Project target directory shorthand. Omit when --destination is supplied.",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        help="Custom parent skills directory, e.g. /path/to/project/.claude/skills",
    )
    parser.add_argument("--force", action="store_true", help="Replace an existing cogc directory")
    args = parser.parse_args()

    if bool(args.target) == bool(args.destination):
        parser.error("Provide exactly one of --target or --destination")

    parent = args.destination.resolve() if args.destination else TARGETS[args.target].resolve()
    dest = parent / "cogc"

    if dest.resolve() == SOURCE.resolve():
        print(f"CogC is already canonical at {dest}")
        return 0

    if dest.exists():
        if not args.force:
            raise SystemExit(f"Destination exists: {dest}. Use --force to replace it.")
        shutil.rmtree(dest)

    parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"Installed CogC skill to {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
