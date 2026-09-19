#!/usr/bin/env python3
"""Synchronize the portable skill bundle and the GitHub Agent Skill mirror.

Canonical sources:
- Python engine: src/cogc
- Skill docs/schemas/wrappers: skill/cogc

Generated/verified copies:
- Embedded portable engine: skill/cogc/scripts/cogc
- GitHub-discovered mirror: .github/skills/cogc
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "src" / "cogc"
CANONICAL_SKILL = ROOT / "skill" / "cogc"
EMBEDDED_ENGINE = CANONICAL_SKILL / "scripts" / "cogc"
GITHUB_MIRROR = ROOT / ".github" / "skills" / "cogc"


def _files(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not root.exists():
        return result
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rel = path.relative_to(root).as_posix()
        result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def _assert_equal(left: Path, right: Path, label: str) -> None:
    a = _files(left)
    b = _files(right)
    if a == b:
        return
    missing_right = sorted(set(a) - set(b))
    missing_left = sorted(set(b) - set(a))
    changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    details = []
    if missing_right:
        details.append(f"missing from {right}: {missing_right}")
    if missing_left:
        details.append(f"extra in {right}: {missing_left}")
    if changed:
        details.append(f"content differs: {changed}")
    raise SystemExit(f"{label} is out of sync: " + "; ".join(details))


def sync() -> None:
    if not ENGINE.exists():
        raise SystemExit(f"Missing engine source: {ENGINE}")
    if not (CANONICAL_SKILL / "SKILL.md").exists():
        raise SystemExit(f"Missing canonical SKILL.md: {CANONICAL_SKILL / 'SKILL.md'}")

    if EMBEDDED_ENGINE.exists():
        shutil.rmtree(EMBEDDED_ENGINE)
    shutil.copytree(ENGINE, EMBEDDED_ENGINE, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    if GITHUB_MIRROR.exists():
        shutil.rmtree(GITHUB_MIRROR)
    GITHUB_MIRROR.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(CANONICAL_SKILL, GITHUB_MIRROR, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def check() -> None:
    required = [
        ENGINE / "__init__.py",
        CANONICAL_SKILL / "SKILL.md",
        CANONICAL_SKILL / "scripts" / "compile_context.py",
        GITHUB_MIRROR / "SKILL.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing required CogC release files: " + ", ".join(missing))
    _assert_equal(ENGINE, EMBEDDED_ENGINE, "Embedded skill engine")
    _assert_equal(CANONICAL_SKILL, GITHUB_MIRROR, "GitHub Agent Skill mirror")
    print("CogC skill integrity: OK")


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize or verify CogC skill copies")
    parser.add_argument("--check", action="store_true", help="Fail if generated skill copies are out of sync")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        sync()
        check()
        print("CogC skill copies synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
