from __future__ import annotations

import hashlib
import re
from pathlib import Path

import cogc

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "cogc"
SKILL = ROOT / "skill" / "cogc"
MIRROR = ROOT / ".github" / "skills" / "cogc"


def _tree(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        out[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def test_visible_skill_and_github_mirror_exist() -> None:
    assert (SKILL / "SKILL.md").is_file()
    assert (MIRROR / "SKILL.md").is_file()


def test_github_mirror_matches_visible_skill() -> None:
    assert _tree(SKILL) == _tree(MIRROR)


def test_embedded_engine_matches_src_engine() -> None:
    assert _tree(SRC) == _tree(SKILL / "scripts" / "cogc")


def test_installable_package_is_not_sourced_from_dotgithub() -> None:
    package_path = Path(cogc.__file__).resolve().as_posix()
    assert "/src/cogc/" in package_path
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'package-dir = {"" = "src"}' in pyproject
    assert '.github/skills/cogc/scripts' not in pyproject


def test_versions_are_consistent() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', pyproject, flags=re.MULTILINE)
    assert match
    assert match.group(1) == cogc.__version__ == "0.2.0"
