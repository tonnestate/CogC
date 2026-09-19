---
name: cogc
description: Experimental capacity-aware cognitive compression for AI agents. Use CogC when a constrained worker must act on large, heterogeneous, repetitive, tool-heavy, RAG-heavy, memory-heavy, or handoff context and needs a smaller task-specific working state without losing hard constraints, exact values, identifiers, evidence, provenance, procedures, stop conditions, or source recoverability. CogC is especially useful for small/local models, agent handoffs, tool-output reduction, and verified procedural reuse. Do not use it as a substitute for retrieval, routing, governance, task decomposition, or persistent memory.
license: Apache-2.0
---

# CogC — Capacity-Aware Cognitive Compression

CogC compiles raw agent context into the minimum sufficient, provenance-preserving cognitive representation for a specific target worker.

The objective is not “make the prompt shorter.” The objective is:

> Give this particular worker the smallest faithful state from which it can make the correct next decision.

## Use CogC when

Use CogC when at least one of these conditions applies:

- the target worker is a constrained model such as a 4B–9B local model;
- raw context is larger or noisier than the worker can reliably use;
- tool output, logs, search results, RAG chunks, memory, or repository scans dominate context;
- a handoff between agents would otherwise copy long conversational history;
- a verified prior trajectory can be represented as a reusable procedure instead of replayed verbatim;
- evidence and source provenance must survive compression;
- the system needs a measurable raw-vs-summary-vs-CogC comparison.

Do not trigger CogC merely because text is long. If the full context is already small, precise, and appropriate for the worker, preserve it.

## Hard boundaries

CogC MUST NOT:

- authorize actions;
- override Owner, security, legal, payment, execution-boundary, PAUSE, KILL, or FREEZE controls;
- select the business goal;
- replace IntakeGov, SPARI, RAG, Graph, persistent memory, OmniRoute, a meta-router, or the Governor;
- silently remove exact identifiers, numbers, evidence links, stop conditions, or hard constraints;
- pretend estimated tokens are provider billing tokens;
- treat textual similarity as proof that downstream decisions remain equivalent;
- require private chain-of-thought from any model.

## Required workflow

### 1. Identify the target worker

Before compression, determine or state the target capacity profile. Prefer measured profiles over parameter-count assumptions.

Built-in profiles in v0.2.0:

- `qwen-4b`
- `qwen-9b`
- `frontier-specialist`
- `generic-small-agent`

If the actual model does not match a built-in profile, use the closest conservative profile and record the mismatch.

### 2. Assemble source state before compressing

Retrieve first, compress second.

CogC may consume:

- task and goal;
- hard constraints;
- evidence;
- current state;
- RAG/Graph results;
- memory;
- tool observations;
- verified procedures;
- prior failure patterns;
- success and stop conditions.

Do not use CogC to compensate for missing retrieval.

### 3. Classify criticality

Use the CIR criticality classes described in `references/criticality-model.md`.

C0 and C1 content is protected. Explicit source criticality always wins over heuristic classification.

### 4. Apply lossless transformations first

Use this order:

1. canonicalization;
2. exact deduplication;
3. structural/reference deduplication;
4. source-handle substitution;
5. irrelevant/noise removal;
6. extractive reduction;
7. learned or semantic compression only when separately validated.

Stop compressing as soon as the budget is satisfied.

### 5. Prefer procedures over replaying trajectories

If verified procedural memory exists, provide the smallest relevant level:

- workflow;
- subtask;
- function.

Do not paste entire historical agent conversations when a verified procedure conveys the actionable knowledge.

### 6. Preserve provenance and reversibility

Fold important omitted material behind stable source handles. Do not destroy it.

A worker must be able to request the original evidence or observation when uncertainty requires expansion.

### 7. Run the Fidelity Gate

Never use a CogC package for consequential work if its fidelity report fails.

The v0.2.0 verifier checks at minimum:

- retention of C0/C1 units;
- exact critical numbers;
- exact critical identifiers;
- source mapping.

If verification fails, use a less aggressive policy or the raw context.

### 8. Measure downstream outcomes

When evaluating CogC, compare:

- A: raw/full context;
- B: ordinary summary/current context handling;
- C: CogC.

Measure verified task success, not compression ratio alone.

## CLI usage

From the repository root after `pip install -e .`:

```bash
cogc compile --input examples/repository-analysis.json --profile qwen-4b --format text --receipt
```

Without installation, from the skill directory:

```bash
python scripts/compile_context.py --input ../../../examples/repository-analysis.json --profile qwen-4b --format text --receipt
```

Validate the same request:

```bash
cogc validate --input examples/repository-analysis.json --profile qwen-4b
```

List built-in profiles:

```bash
cogc profiles
```

## Input contract

The compile request is JSON. See `schemas/compile-request.schema.json` and the examples.

At minimum provide:

```json
{
  "goal": "...",
  "task": "...",
  "sources": [
    {"id": "SRC-1", "kind": "constraint", "text": "..."}
  ]
}
```

For important constraints, set `criticality` explicitly rather than relying on heuristics.

## Output contract

CogC returns a Cognitive Package containing:

- goal;
- task;
- target profile;
- immutable/critical units;
- selected relevant state;
- optional procedure;
- success conditions;
- stop conditions;
- expandable source handles;
- source map;
- compression receipt;
- fidelity report.

See `schemas/cognitive-package.schema.json`.

## Small-model compilation rule

For a constrained worker, prefer this shape:

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

Do not ask a weak model to rediscover a known method from raw history.

## Failure behavior

CogC is an optimization layer. If it fails, degrade gracefully:

```text
validated compiled package
→ less compressed package
→ extractive package
→ deduplicated raw context
→ raw context
```

A compressor outage is not a global blocker.

## Research and reuse

Before adding a new compression mechanism, inspect current prior art and prefer reuse. Start with `references/research-foundations.md`.

The v0.2.0 engine deliberately implements only deterministic compilation and extractive reduction. Learned ACON-like policies, model-specific training, and dedicated compressor models belong in later releases only after the A/B/C harness shows measurable downstream value.

## Completion rule

CogC has succeeded only when a constrained agent receives materially less working context while retaining required constraints and evidence and achieves equal or higher verified downstream quality, or when the same quality is achieved with meaningfully lower total cognitive cost.
