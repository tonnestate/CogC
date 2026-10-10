---
name: cogc
description: Compile large or noisy agent context into the minimum faithful working state needed by a specific target model. Use CogC whenever an AI agent—especially a small or local model—must work with oversized tool output, RAG results, memory, logs, repository context, agent handoffs, or prior trajectories. Preserve hard constraints, exact values, identifiers, evidence provenance, procedures, contradictions, success criteria, stop conditions, and reversible source handles while removing irrelevant or redundant context. Use CogC before handing oversized context to a constrained worker; do not use it when the existing context is already small, precise, and task-appropriate.
license: Apache-2.0
---

# CogC — Capacity-Aware Cognitive Compression

Compile context for the worker that will actually consume it.

The objective is not maximum compression. Produce the smallest faithful working state that still lets the target worker make the correct next decision.

## Workflow

1. Identify the task and target worker.
2. Gather the relevant source state before compressing it.
3. Mark protected information and unresolved contradictions.
4. Build or normalize the Cognitive Intermediate Representation (CIR).
5. Apply lossless reduction before any lossy reduction.
6. Replace verified historical trajectories with procedures when that preserves the required knowledge.
7. Compile the remaining state for the target worker's capacity.
8. Keep omitted evidence recoverable through stable source handles.
9. Run the Fidelity Gate.
10. If fidelity fails, reduce compression or return the raw context.

## Protect first

Never silently remove or alter:

- explicit constraints and authorization boundaries;
- exact identifiers, dates, amounts, units, versions, and other critical values;
- evidence references and provenance;
- success criteria and acceptance conditions;
- stop, escalation, or rollback conditions;
- unresolved contradictions that could change the next action.

Use explicit caller-supplied criticality when available. Otherwise apply the conservative rules in `references/criticality-model.md`.

## Compression order

Prefer transformations in this order:

1. canonicalize formatting;
2. remove exact duplicates;
3. replace repeated material with references;
4. remove clearly irrelevant/noisy material;
5. select task-relevant evidence;
6. shorten non-critical material extractively;
7. use semantic or learned compression only when separately validated.

Stop compressing once the working state fits the target worker and task. Do not optimize token count at the expense of downstream correctness.

## Compile for the receiver

Do not create one universal summary. Adapt the package to the target worker.

For constrained workers, prefer an explicit shape such as:

```text
GOAL
CURRENT STATE
HARD CONSTRAINTS
RELEVANT FACTS
PROCEDURE
TOOLS / SOURCE HANDLES
NEXT DECISION
SUCCESS CONDITION
STOP / ESCALATION CONDITION
```

Use `references/capacity-profiles.md` when selecting or defining a target profile.

## Prefer procedures over history

When verified procedural memory already captures the method, provide the smallest useful level instead of replaying raw history:

- workflow — end-to-end method;
- subtask — reusable intermediate method;
- function — tool-specific execution or recovery knowledge.

Read `references/procedural-memory.md` when compiling prior experience.

## Preserve provenance and reversibility

Treat omitted but important source material as folded, not destroyed. Retain stable source handles so the worker or orchestrator can recover the original evidence when needed.

Read `references/cognitive-intermediate-representation.md` for the CIR contract and `references/fidelity-contract.md` for preservation requirements.

## Run deterministic compilation

When the CogC scripts are available, use the deterministic compiler rather than manually rewriting large contexts.

Installed package:

```bash
cogc compile --input <request.json> --profile <profile> --format text --receipt
cogc validate --input <request.json> --profile <profile>
```

Standalone skill directory:

```bash
python scripts/compile_context.py --input <request.json> --profile <profile> --format text --receipt
python scripts/validate_context.py --input <request.json> --profile <profile>
```

Input and output schemas are in `schemas/`.

## Fidelity Gate

Before using a compressed package for consequential work, verify protected-field retention and source mapping.

If the Fidelity Gate fails:

1. retry with less aggressive compression;
2. use extractive-only reduction;
3. use deduplicated raw context;
4. fall back to raw context.

Never silently waive a failed fidelity check.

## Output

Return a Cognitive Package containing the information needed for the next action, including as applicable:

- goal and task;
- target profile;
- protected constraints;
- selected relevant facts and evidence;
- procedure;
- unresolved contradictions;
- success and stop conditions;
- expandable source handles;
- source map;
- fidelity result;
- compression receipt.

Do not claim success from compression ratio alone.

## Evaluation

When evaluating whether CogC helps an agent, compare the same target model on the same tasks:

- A — raw/full context;
- B — ordinary summarization or existing context handling;
- C — CogC.

Prefer downstream verified task success, retries, latency, total token use, escalation rate, and cost over text-similarity metrics.

Read `references/research-foundations.md` only when evaluating, extending, or researching CogC. It is not required for routine compilation.

## Boundaries

CogC prepares context. It does not:

- choose organizational or business goals;
- authorize actions or override safety/security controls;
- replace retrieval, routing, task decomposition, persistent memory, or execution governance;
- require private chain-of-thought;
- prove that a compressed package is semantically equivalent merely because protected fields were retained.

When the full context is already small, precise, and appropriate for the target worker, do not use CogC.
