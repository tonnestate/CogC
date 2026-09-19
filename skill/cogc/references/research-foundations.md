# Research Foundations and Prior Art

CogC composes ideas from existing research and open-source systems. It does not claim that context compression itself is novel.

## Prompt and long-context compression

- LLMLingua / LLMLingua-2 — Microsoft. Prompt compression and distilled task-agnostic compression.
  - https://github.com/microsoft/LLMLingua
  - https://aclanthology.org/2024.findings-acl.57/
- LongLLMLingua — relevance-aware long-context compression.
  - https://aclanthology.org/2024.acl-long.91/

## Agent context optimization

- ACON: Optimizing Context Compression for Long-horizon LLM Agents. Learns compression guidelines from full-context-success/compressed-context-failure cases and studies compressor distillation.
  - https://arxiv.org/abs/2510.00615
  - https://github.com/microsoft/acon

## Procedural memory

- Agent Workflow Memory (ICML 2025). Induces reusable workflows from agent experience.
  - https://proceedings.mlr.press/v267/wang25bx.html
  - https://github.com/zorazrw/agent-workflow-memory
- Agent Memory Distillation (2026 preprint). Transfers hierarchical workflow/subtask/function memory to smaller agents; results should be independently validated before production assumptions are made.
  - https://arxiv.org/abs/2608.07169

## Persistent memory / context engineering

- Letta: https://github.com/letta-ai/letta
- Mem0: https://github.com/mem0ai/mem0

## CogC's intended contribution

CogC focuses on the integration boundary:

`task + protected constraints + evidence + procedural memory + target capacity → minimal faithful cognitive package`

Its distinguishing requirements are capacity awareness, hard-field preservation, reversible source handles, provenance, fidelity gates and downstream A/B/C evaluation.

No scientific paper proves the complete CogC composition will improve a given agent. The repository is therefore evaluation-first and treats the business hypothesis as falsifiable.
