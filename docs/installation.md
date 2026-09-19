# Skill Installation

The canonical skill source is `.github/skills/cogc`.

That location is directly usable as a GitHub Copilot project skill. The repository intentionally keeps only one canonical copy so that `.github`, `.claude` and `.agents` variants cannot drift.

To copy the same skill into another project-level Agent Skills location:

```bash
python tools/install_skill.py --target claude
python tools/install_skill.py --target agents
```

For another repository or a custom skills directory:

```bash
python tools/install_skill.py --destination /path/to/project/.claude/skills
```

Use `--force` only when you intentionally want to replace an existing installed copy.

The Python engine remains inside the skill directory under `scripts/cogc`, so the copied skill is self-contained. It can be invoked without installing the root Python package:

```bash
python .claude/skills/cogc/scripts/compile_context.py --input request.json --profile qwen-4b --format text
```
