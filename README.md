# CogC

**Capacity-Aware Cognitive Compression for constrained AI agents.**

CogC compiles large, heterogeneous agent state into the minimum sufficient, provenance-preserving representation for a specific target worker. It is designed for environments where 4B–9B local models, variable external specialists and multi-agent handoffs must perform useful work without receiving every raw token the system knows.

CogC is both:

1. a valid GitHub Agent Skill under `.github/skills/cogc`; and
2. a dependency-free Python reference engine for deterministic cognitive compilation.

Version `0.1.0` is deliberately conservative. It does **not** ship a new learned compressor. It establishes the measurable contract first: CIR, protected criticality classes, deduplication, extractive reduction, provenance, reversible source handles, target profiles and a Fidelity Gate.

## The problem

A small model often fails for two very different reasons:

- it lacks capability; or
- the system gave it the wrong cognitive representation.

CogC targets the second problem.

Instead of:

```text
30,000 raw tokens
→ "please understand all of this"
→ constrained worker
```

CogC aims for:

```text
Task + evidence + constraints + memory + procedures + target profile
                              │
                              ▼
                             CogC
                              │
                              ▼
Goal + critical state + relevant facts + procedure + source handles
                              │
                              ▼
                       constrained worker
```

## What CogC is not

CogC is not:

- a replacement for RAG or retrieval;
- a persistent-memory database;
- a router;
- a Governor or authorization layer;
- an agent framework;
- a generic summarizer;
- proof that a 4B model becomes a frontier model.

It is a **capacity-aware compiler** between assembled system state and the worker that must act on it.

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

The skill itself lives at:

```text
.github/skills/cogc/SKILL.md
```

GitHub Copilot recognizes project Agent Skills from `.github/skills`. The skill follows the open Agent Skills `SKILL.md` format. For Claude/portable project installation, see `docs/installation.md`.

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
python .github/skills/cogc/scripts/compile_context.py \
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

CogC v0.1.0 enforces these design rules:

- C0/C1 information is never dropped to satisfy a token budget.
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
      "id": "OWN-1",
      "kind": "owner_instruction",
      "criticality": "C0",
      "text": "Do not write to production without Owner approval."
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

See `examples/` and `.github/skills/cogc/schemas/compile-request.schema.json` for the full contract.

## Repository layout

```text
.
├── .github/
│   ├── skills/cogc/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── schemas/
│   │   └── scripts/
│   │       └── cogc/          # portable reference engine
│   └── workflows/ci.yml
├── docs/
├── evals/
├── examples/
├── tests/
├── pyproject.toml
└── README.md
```

## Scientific / engineering basis

CogC is intentionally reuse-first. Its design is informed by:

- Microsoft LLMLingua / LLMLingua-2 and LongLLMLingua for context compression;
- Microsoft ACON for learning from compressed-context failures and compressor distillation;
- Agent Workflow Memory for reusable procedural knowledge;
- Agent Memory Distillation for hierarchical workflow/subtask/function transfer to small agents;
- Letta and Mem0 as references for persistent memory/context-management boundaries.

See `.github/skills/cogc/references/research-foundations.md` for links and the precise boundary.

The repository does **not** claim these papers prove CogC as a combined architecture. CogC must beat its baselines empirically.

## Evaluation contract

Do not evaluate CogC by token reduction alone.

The required downstream comparison is:

| Arm | Context |
|---|---|
| A | raw/full context |
| B | ordinary summary/current context handling |
| C | CogC |

Use the same target model, tasks and acceptance tests. Measure verified task success, critical-field retention, retries, latency, tokens, premium-model escalations and total cost.

Run the offline deterministic smoke eval:

```bash
python evals/run_offline_eval.py
```

The offline eval validates fidelity and compression mechanics only. It does not masquerade as a model-quality benchmark.

## Roadmap

### v0.1.x — deterministic compiler

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

## Status

`EXPERIMENTAL`

Promotion condition: constrained agents must achieve equal or better verified downstream quality with lower cognitive cost, or materially higher verified quality at equivalent total cost.

## License

Apache License 2.0. See `LICENSE`.
