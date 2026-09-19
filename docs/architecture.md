# Architecture

CogC sits after retrieval/state assembly and before execution/routing consumption.

```text
Goal / Task
   ↓
Retrieval + RAG + Graph + Memory + Evidence
   ↓
CIR builder
   ↓
Criticality classification
   ↓
Lossless canonicalization + deduplication
   ↓
Task relevance scoring
   ↓
Capacity-aware budget selection
   ↓
Procedure selection
   ↓
Cognitive Package
   ↓
Fidelity Gate
   ↓
Target worker
```

## Why CIR exists

Raw context sources differ substantially: tool logs, database rows, conversations, evidence, documents and workflow memory. CIR establishes a minimal common boundary that can be inspected, tested and versioned.

## Why the first release is deterministic

The main product risk is not lack of sophisticated compression. It is building a complex learned subsystem whose downstream value is unknown. v0.2.1 preserves that deterministic baseline while reducing the active Agent Skill payload through progressive disclosure before later ML is considered.

## Budget behavior

C0/C1 material is retained even when it causes the package to exceed the requested budget. The receipt records `over_budget_due_to_critical=true`. This behavior is intentional: a token budget is not an authorization to destroy critical state.
