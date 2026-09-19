# Capacity Profiles

A capacity profile describes how context should be prepared for a target worker. It is not a claim about the worker's intrinsic intelligence.

Built-in profiles are conservative starting points:

- `qwen-4b`: compact context, explicit procedure, low ambiguity;
- `qwen-9b`: broader context and limited alternatives;
- `frontier-specialist`: richer evidence and contradictions;
- `generic-small-agent`: safe fallback.

Profiles must eventually be calibrated using real downstream runs. Do not permanently encode performance assumptions from parameter count or brand reputation.

Recommended learned dimensions include task-specific success, schema adherence, tool reliability, tolerance for ambiguity, context sensitivity and escalation probability.
