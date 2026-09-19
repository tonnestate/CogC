from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".github" / "skills" / "cogc" / "SKILL.md"


def test_skill_has_required_frontmatter() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    frontmatter = text.split("---", 2)[1]
    assert "name: cogc" in frontmatter
    assert "description:" in frontmatter


def test_skill_name_is_spec_compatible() -> None:
    name = "cogc"
    assert len(name) <= 64
    assert name == name.lower()
    assert name.replace("-", "").isalnum()
