# Changelog

## 0.2.0 — 2026-09-19

Packaging and repository-integrity release.

- Moved the installable Python engine to the standard `src/cogc` package layout.
- Added visible canonical Agent Skill source at `skill/cogc` so the project remains inspectable even if dot-directories are lost during manual upload.
- Kept `.github/skills/cogc` as the GitHub-discovered mirror.
- Added `tools/sync_skill.py` to generate/verify the embedded engine and GitHub skill mirror.
- Added CI integrity gates that fail when the visible skill, GitHub mirror, or embedded engine drifts.
- Changed `tools/install_skill.py` to install from the visible canonical skill source.
- Added standalone-skill, installer, package-layout, version-consistency, and mirror-integrity tests.
- Added release workflow for tagged `v*` releases.
- Preserved the deterministic v0.1 compiler behavior; this release fixes delivery and packaging before adding learned compression.

## 0.1.0 — 2026-09-19

Initial experimental release.

- Agent Skills-compatible `SKILL.md`.
- Deterministic CIR compiler.
- C0–C5 criticality model.
- Critical number/identifier Fidelity Gate.
- Exact deduplication with provenance merging.
- Task-relevance selection and extractive shortening.
- Reversible source handles for omitted context.
- Qwen 4B / Qwen 9B / generic / frontier target profiles.
- Procedure selection.
- CLI, JSON schemas, examples, offline eval and tests.
