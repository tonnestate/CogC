from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_installer_creates_self_contained_skill(tmp_path: Path) -> None:
    parent = tmp_path / "skills"
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "install_skill.py"), "--destination", str(parent)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    installed = parent / "cogc"
    assert (installed / "SKILL.md").is_file()
    assert (installed / "scripts" / "cogc" / "core.py").is_file()

    proc = subprocess.run(
        [
            sys.executable,
            str(installed / "scripts" / "compile_context.py"),
            "--input",
            str(ROOT / "examples" / "repository-analysis.json"),
            "--profile",
            "qwen-4b",
            "--format",
            "json",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["fidelity"]["passed"] is True
