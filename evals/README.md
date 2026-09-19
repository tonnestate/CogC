# CogC Evaluations

The bundled offline eval intentionally measures only properties CogC can verify without calling an LLM:

- protected-field retention;
- exact-number/identifier retention;
- deterministic compression ratio;
- regression behavior.

Run:

```bash
python evals/run_offline_eval.py
```

The scientifically relevant evaluation is downstream A/B/C:

- A — target model with full/raw context;
- B — target model with ordinary summarization/current context handling;
- C — the same target model with CogC.

Use identical tasks and acceptance tests. Record verified success, critical-fact retention, retries, latency, total tokens, external model calls, escalation rate and cost per accepted outcome.

This repository does not fake the downstream score by substituting compression metrics for task success.
