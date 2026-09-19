# CogC

> [!WARNING]
> **EXPERIMENTAL — v0.2.0**  
> CogC is a research-oriented Agent Skill and reference implementation. The deterministic compiler, provenance tracking, reversible source handles, schemas, and fidelity checks are tested, but **downstream intelligence gains are not yet claimed**. Use it behind evaluation gates until your own raw-vs-summary-vs-CogC tests show a measurable benefit.

**Capacity-Aware Cognitive Compression for constrained AI agents.**

CogC compiles large, heterogeneous agent context into the **minimum sufficient, provenance-preserving working state for a specific target model**.

It is built for a practical problem that appears as agent systems become larger while their individual workers remain constrained: the system may know far more than the worker can reliably use.

A smaller model often does not need *more* context. It needs the **right context, in the right structure, with the right constraints preserved**.

CogC is both:

1. a **visible canonical Agent Skill** under `skill/cogc`;
2. a GitHub-discovered mirror under `.github/skills/cogc`; and
3. a dependency-free Python reference engine under `src/cogc`.

## Why CogC exists

Modern agent systems accumulate context from conversations, RAG, tools, logs, repositories, memory, previous runs, policies, evidence, and agent-to-agent handoffs. Passing all of that material directly to every worker creates several problems:

- **Context overload:** relevant facts compete with noise, repetition, obsolete state, and verbose history.
- **Small-model mismatch:** 4B–9B workers may have enough capability for a bounded task but fail when forced to reconstruct the task from a large raw context.
- **Expensive handoffs:** agents repeatedly transmit long histories even when the next worker needs only a few facts, constraints, and a known procedure.
- **Lossy summarization:** ordinary summaries can remove exact values, identifiers, stop conditions, evidence links, or other information that must survive unchanged.
- **Weak auditability:** after a summary, it can be difficult to determine which source supported a compressed claim.
- **Repeated rediscovery:** a worker may be given an entire historical trajectory even when a verified reusable procedure already captures what matters.
- **Unnecessary escalation:** systems may call larger or more expensive models simply because the context was poorly prepared for the cheaper worker.

CogC was created to test a different approach:

> **Do not ask a constrained model to understand everything the system knows. Compile what it needs to make the next correct decision.**

The goal is not to make a small model pretend to be a frontier model. The goal is to remove avoidable cognitive load so that each worker operates closer to its actual capability.

## What CogC brings

CogC turns this:

```text
raw conversation
+ RAG chunks
+ tool output
+ logs
+ memory
+ evidence
+ constraints
+ prior trajectories
                 │
                 ▼
          one huge prompt
```

into this:

```text
Task + evidence + constraints + memory + procedures + target profile
                              │
                              ▼
                             CogC
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 criticality            relevance +           procedural
 protection             deduplication          compilation
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                 provenance + fidelity gate
                              │
                              ▼
        minimum sufficient cognitive package
                              │
                              ▼
                       target worker
```

The v0.2.0 compiler provides:

- **Capacity-aware output:** compile for the intended worker rather than producing one universal summary.
- **C0–C5 criticality classes:** protect hard constraints and high-value information from aggressive reduction.
- **Exact-value protection:** preserve critical numbers, IDs, and machine-like identifiers.
- **Deterministic deduplication:** remove repeated source content before using lossy methods.
- **Task-focused selection:** prioritize information that is relevant to the current goal and next action.
- **Procedural compression:** prefer a verified workflow/subtask/function procedure over replaying entire historical trajectories.
- **Provenance:** retain source lineage for compiled facts.
- **Reversible source handles:** omit non-critical detail from working context without making the original source unreachable.
- **Cognitive Packets:** produce compact state suitable for agent handoffs.
- **Fidelity Gate:** verify protected information before a compressed package is used.
- **Compression receipts:** record what happened, which policy was used, and what was retained.
- **A/B/C evaluation support:** compare raw context, ordinary summary, and CogC instead of assuming compression is beneficial.

## Why use CogC

CogC is useful when **the bottleneck is not retrieval but usable cognitive bandwidth**.

Typical cases include:

### Small local models

A 4B or 9B worker may be perfectly capable of executing a narrow procedure while being unreliable when given 20,000 tokens of mixed history. CogC can transform that history into an explicit goal, current state, constraints, relevant facts, procedure, source handles, and stop conditions.

### Tool-heavy agents

Logs, repository scans, search results, API responses, test output, and large JSON objects can dominate context. CogC reduces repeated and irrelevant material while preserving critical exact values and source references.

### Multi-agent handoffs

The next agent rarely needs the complete conversation of the previous agent. CogC can emit a compact Cognitive Packet with claims, evidence references, unresolved conflicts, procedures, and the next required action.

### Reusing expensive reasoning

If a difficult task has already been solved and verified, future workers should not have to rediscover the method from raw history. CogC can represent reusable experience as workflow, subtask, or function-level procedural memory.

### Reducing unnecessary use of larger models

A stronger model may be needed because the problem is genuinely difficult — or because a weaker model received a poor representation of the problem. CogC is designed to help distinguish those cases experimentally.

### Evidence-sensitive automation

When constraints, IDs, numerical values, evidence references, and stop conditions cannot be silently lost, a generic summary is insufficient. CogC treats protected information and provenance as part of the compilation contract.

## What CogC does **not** claim

CogC v0.2.0 does **not** claim that:

- compression always improves model quality;
- fewer tokens automatically mean better reasoning;
- a 4B model becomes equivalent to a frontier model;
- its current deterministic policies are optimal;
- published compression or memory research proves this combined architecture.

Those are empirical questions.

CogC is deliberately built so they can be tested.

## What CogC is not

CogC is not:

- a replacement for RAG or retrieval;
- a persistent-memory database;
- a model router;
- an authorization or governance layer;
- an agent framework;
- a generic summarizer;
- a private chain-of-thought extractor;
- a reason to compress context that is already small and appropriate.

It is a **capacity-aware compiler between assembled system state and the worker that must act on it**.

## The core idea

A conventional summarizer asks:

> How can I make this text shorter?

CogC asks:

> What is the minimum faithful cognitive state this specific worker needs to make the correct next decision?

For a constrained worker, the desired result is closer to:

```text
GOAL
Verify capability X.

CURRENT STATE
Source inspection completed; runtime behavior unverified.

HARD CONSTRAINTS
Do not modify production.
Do not accept README claims as runtime proof.

RELEVANT FACTS
Implementation entry point: module Y.
Expected behavior: Z.

PROCEDURE
WF-VERIFY-03

EVIDENCE
EV-17, EV-22

NEXT ACTION
Run isolated runtime test.

SUCCESS
Observed behavior matches claim X.

STOP / ESCALATE
Conflicting runtime evidence or unavailable test environment.

EXPANDABLE
EV-17, EV-22, SRC-41
```

rather than another prose summary.

## Install

Python 3.10+:

```bash
pip install -e .
```

Development:

```bash
pip install -e ".[dev]"
pytest
```

The canonical, visible skill source lives at:

```text
skill/cogc/SKILL.md
```

GitHub discovers the verified mirror at:

```text
.github/skills/cogc/SKILL.md
```

The Python package is independent under `src/cogc`. `tools/sync_skill.py --check` verifies that the portable skill and GitHub mirror contain the same generated engine and content. The skill can be copied into other project-level Agent Skills locations with `tools/install_skill.py`. See `docs/installation.md`.

## First compile

```bash
cogc compile \
  --input examples/repository-analysis.json \
  --profile qwen-4b \
  --format text \
  --receipt
```

Or without package installation:

```bash
python skill/cogc/scripts/compile_context.py \
  --input examples/repository-analysis.json \
  --profile qwen-4b \
  --format text \
  --receipt
```

Validate protected information:

```bash
cogc validate --input examples/repository-analysis.json --profile qwen-4b
```

## Core invariants

CogC v0.2.0 enforces these design rules:

- C0/C1 information is never dropped merely to satisfy a token budget.
- Exact critical numbers and machine-like identifiers must survive.
- Omitted non-critical source material remains addressable by source handle.
- Exact duplicate source content is stored once while provenance is merged.
- Compression starts with deterministic/lossless transformations.
- The output includes a compression receipt and fidelity result.
- If critical material alone exceeds the budget, CogC reports this rather than silently truncating it.

## Input example

```json
{
  "goal": "Verify whether a repository already provides capability X.",
  "task": "Inspect source and obtain runtime evidence.",
  "token_budget": 1200,
  "sources": [
    {
      "id": "POLICY-1",
      "kind": "constraint",
      "criticality": "C0",
      "text": "Do not write to production without explicit approval."
    },
    {
      "id": "EVID-1",
      "kind": "evidence",
      "criticality": "C1",
      "text": "README claims FEATURE-X; runtime proof is still missing."
    }
  ]
}
```

See `examples/` and `skill/cogc/schemas/compile-request.schema.json` for the full contract.

## Repository layout

```text
.
├── src/cogc/                  # installable Python engine (canonical engine source)
├── skill/cogc/                # visible canonical Agent Skill
│   ├── SKILL.md
│   ├── references/
│   ├── schemas/
│   └── scripts/
│       └── cogc/              # generated portable engine copy
├── .github/
│   ├── skills/cogc/           # generated/verified GitHub Agent Skill mirror
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── docs/
├── evals/
├── examples/
├── tests/
├── tools/
│   ├── install_skill.py
│   └── sync_skill.py
├── pyproject.toml
└── README.md
```

## Scientific and engineering basis

CogC is intentionally reuse-first. Its design is informed by:

- Microsoft LLMLingua / LLMLingua-2 and LongLLMLingua for context compression;
- Microsoft ACON for learning from compressed-context failures and compressor distillation;
- Agent Workflow Memory for reusable procedural knowledge;
- Agent Memory Distillation for hierarchical workflow/subtask/function transfer to small agents;
- Letta and Mem0 as references for persistent memory/context-management boundaries.

See `skill/cogc/references/research-foundations.md` for links and the precise boundary.

The repository does **not** claim these papers prove CogC as a combined architecture. CogC must beat its baselines empirically.

## Evaluation contract

Do not evaluate CogC by compression ratio alone.

The required downstream comparison is:

| Arm | Context |
|---|---|
| A | raw/full context |
| B | ordinary summary/current context handling |
| C | CogC |

Use the same target model, tasks, and acceptance tests. Measure verified task success, critical-field retention, retries, latency, tokens, model escalations, and total cost.

Run the offline deterministic smoke eval:

```bash
python evals/run_offline_eval.py
```

The offline eval validates fidelity and compression mechanics only. It does not masquerade as a model-quality benchmark.

## Current status

**v0.2.0 — EXPERIMENTAL**

The deterministic mechanics are implemented and tested. Promotion requires downstream evidence that CogC provides one of the following without reducing required quality:

- lower context cost;
- lower latency;
- fewer retries;
- fewer unnecessary escalations;
- higher verified success for constrained workers;
- or materially better verified output at comparable total cost.

Until such evidence exists for a given environment, CogC should be treated as an experimental optimization layer with raw-context fallback.

## Roadmap

### v0.1.0 — deterministic compiler

- CIR
- criticality protection
- provenance
- reversible source handles
- exact deduplication
- extractive reduction
- capacity profiles
- procedure injection
- Fidelity Gate
- A/B/C evaluation harness

### v0.2.0 — packaging and integrity

- standard `src/cogc` package layout;
- visible canonical `skill/cogc` bundle;
- verified `.github/skills/cogc` mirror;
- self-contained portable skill;
- mirror/engine drift detection in CI;
- standalone and installer tests.

### v0.2.x — optional compression backends

Candidates, only after evaluation:

- LLMLingua-2 adapter;
- structured tool-output compressor;
- context-policy plugins;
- stronger decision-equivalence tests.

### v0.3.x — learning

Only with real labeled outcomes:

- ACON-style compression-failure learning;
- target-model-specific compression policy;
- contextual-bandit policy selection;
- teacher-to-small-worker procedural distillation.

## GitHub repository metadata

**Description**

> Experimental capacity-aware cognitive compression for AI agents — compile large context, evidence, constraints, and procedures into small-model-ready packages with provenance and fidelity checks.

**Topics / keywords**

```text
agent-skills
ai-agents
cognitive-compression
context-compression
context-engineering
context-management
small-language-models
slm
llm-agents
local-llm
prompt-compression
agent-memory
procedural-memory
agent-handoffs
provenance
fidelity
multi-agent-systems
qwen
llmlingua
```

## License

Apache-2.0. See `LICENSE`.
