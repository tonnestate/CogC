# CogC v0.2.1 Release Notes

CogC v0.2.1 refactors the Agent Skill itself.

The previous `SKILL.md` was formally valid but carried too much product documentation, research context, architecture explanation, and project-specific language in the active skill payload. That made the skill harder to scan and contradicted CogC's own principle of reducing unnecessary context.

v0.2.1 changes the skill to a progressive-disclosure design:

- `SKILL.md` contains the trigger, operational workflow, invariants, execution commands, fidelity fallback, output contract, and resource pointers.
- detailed criticality, CIR, capacity, fidelity, procedural-memory, compression-policy, and research material remains in `references/` and is loaded only when needed;
- project-specific orchestration names were removed from the public skill instructions;
- tests now enforce a bounded skill payload and verify all referenced local resources exist.

The compression engine itself remains deterministic. This release does not claim new downstream model-quality gains.
