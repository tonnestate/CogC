# Roadmap

## v0.1.0 — deterministic prototype

Build an inspectable deterministic reference implementation and prove the evaluation contract.

## v0.2.0 — packaging and integrity

- standard `src/cogc` Python packaging;
- visible canonical `skill/cogc` source;
- GitHub-discovered `.github/skills/cogc` mirror;
- self-contained portable skill bundle;
- mirror/engine integrity checks;
- installer tests and standalone execution tests;
- tagged-release automation.

## v0.2.x — hardening

- richer structured-data preservation;
- deterministic large-log compaction;
- explicit `expand` command backed by an external source store;
- stronger model-profile calibration harness;
- optional LLMLingua/LLMLingua-2 backend adapter;
- plugin API for compressors;
- decision-equivalence evaluator.

## v0.3.x — learning, only after real labels exist

- compression-failure dataset;
- ACON-style guideline/policy optimization;
- contextual bandit over compression policies;
- target-specific policy models;
- verified teacher-trajectory procedural distillation.
