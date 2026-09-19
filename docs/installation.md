# Installation

CogC v0.2.1 deliberately separates the Python package from Agent Skill packaging.

## Python package

The installable engine lives in `src/cogc`:

```bash
python -m pip install -e .
cogc --version
```

The Python package does **not** depend on `.github/skills` being present.

## Canonical Agent Skill

The visible canonical skill bundle lives at:

```text
skill/cogc/
```

It contains `SKILL.md`, references, schemas, wrappers, and an embedded copy of the reference engine so the skill remains self-contained when copied elsewhere.

## GitHub Agent Skill mirror

GitHub-discoverable project skill:

```text
.github/skills/cogc/
```

This directory is a generated/verified mirror of `skill/cogc`.

After changing `src/cogc` or `skill/cogc`, run:

```bash
python tools/sync_skill.py
```

CI runs:

```bash
python tools/sync_skill.py --check
```

and fails if the copies drift.

## Install into other Agent Skill locations

```bash
python tools/install_skill.py --target claude
python tools/install_skill.py --target agents
```

For another repository or a custom skills directory:

```bash
python tools/install_skill.py --destination /path/to/project/.claude/skills
```

Use `--force` only when you intentionally want to replace an existing installed copy.

The copied skill is self-contained and can run without installing the root package:

```bash
python .claude/skills/cogc/scripts/compile_context.py \
  --input request.json \
  --profile qwen-4b \
  --format text
```
