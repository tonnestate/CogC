from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill" / "cogc"
SKILL = SKILL_DIR / "SKILL.md"


def _text() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_skill_has_required_frontmatter() -> None:
    text = _text()
    assert text.startswith("---\n")
    frontmatter = text.split("---", 2)[1]
    assert "name: cogc" in frontmatter
    assert "description:" in frontmatter


def test_skill_name_is_spec_compatible() -> None:
    name = "cogc"
    assert len(name) <= 64
    assert name == name.lower()
    assert name.replace("-", "").isalnum()


def test_skill_uses_progressive_disclosure() -> None:
    text = _text()
    # Keep the active skill payload compact; detailed material belongs in references/.
    assert len(text.splitlines()) <= 200
    assert "## Workflow" in text
    assert "references/criticality-model.md" in text
    assert "references/capacity-profiles.md" in text
    assert "references/fidelity-contract.md" in text
    assert "references/research-foundations.md" in text


def test_skill_has_no_project_specific_orchestration_names() -> None:
    text = _text().lower()
    forbidden = ["intakegov", "spari", "omniroute", "avcos"]
    assert not any(term in text for term in forbidden)


def test_skill_referenced_local_files_exist() -> None:
    text = _text()
    refs = set(re.findall(r"`((?:references|schemas)/[^`]+)`", text))
    assert refs
    for ref in refs:
        # Schemas may be referenced as a directory; only concrete files are checked.
        if ref.endswith("/") or ref == "schemas/":
            continue
        assert (SKILL_DIR / ref).exists(), ref


def test_skill_description_is_trigger_oriented() -> None:
    frontmatter = _text().split("---", 2)[1]
    assert "Use CogC" in frontmatter
    assert "small or local model" in frontmatter
    assert "do not use it" in frontmatter
