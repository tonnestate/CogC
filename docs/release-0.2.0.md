# CogC v0.2.0 Release Notes

CogC v0.2.0 is a packaging and repository-integrity release. It addresses the failure mode where documentation referenced `.github/skills/cogc` while a published repository could omit that hidden directory and thereby lose both the Agent Skill and the Python package source.

## What changed

- `src/cogc/` is now the canonical installable Python engine.
- `skill/cogc/` is now the visible canonical Agent Skill bundle.
- `.github/skills/cogc/` remains the GitHub-discovered mirror.
- The portable skill embeds an engine copy generated from `src/cogc`.
- `tools/sync_skill.py` synchronizes and verifies all copies.
- CI fails if the visible skill, embedded engine, or GitHub mirror drifts.
- `tools/install_skill.py` installs from the visible canonical skill.
- Standalone execution, fresh-skill installation, package layout, version consistency, schemas, fidelity, and offline evals are covered by tests.
- Tagged releases build Python distributions plus a portable Agent Skill archive.

## Behavioral scope

The deterministic compression behavior remains intentionally conservative. v0.2.0 does not add learned compression or claim downstream model-quality gains. Those remain evaluation-gated future work.

## Verified release checks

For the release artifact generated on 2026-09-19:

- 22 tests passed.
- Offline deterministic eval: 3/3 cases passed.
- Installed CLI reports `CogC 0.2.0`.
- Installed Python import resolves from `src/cogc`.
- Visible standalone skill executes successfully.
- `.github` mirror executes successfully.
- Fresh installation into an external skills directory executes successfully.
- Python wheel builds successfully from the standard `src` layout.
