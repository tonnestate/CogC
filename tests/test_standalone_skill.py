from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "repository-analysis.json"


def _run(script: Path) -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(script),
            "--input",
            str(EXAMPLE),
            "--profile",
            "qwen-4b",
            "--format",
            "json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def test_visible_skill_runs_without_root_package_path() -> None:
    payload = _run(ROOT / "skill" / "cogc" / "scripts" / "compile_context.py")
    assert payload["fidelity"]["passed"] is True
    assert payload["receipt"]["version"] == "0.2.0"


def test_github_skill_mirror_runs() -> None:
    payload = _run(ROOT / ".github" / "skills" / "cogc" / "scripts" / "compile_context.py")
    assert payload["fidelity"]["passed"] is True
