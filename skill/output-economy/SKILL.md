---
name: output-economy
description: Minimize generated agent handoff and user-facing text without weakening facts, evidence, constraints or uncertainty.
---

# Output Economy / 1

Apply these rules **before generating the response**. They govern output, not investigation or the internal reasoning budget.

1. Give the requested result or next action directly. Do not announce that work will start or restate the user's request.
2. Omit compliments, agreement rituals, repeated apologies, filler, self-justification, and closing summaries that add no decision-relevant information.
3. When an error matters, state the observed failure, the performed correction (if any), and the actual verification result. Never claim a correction, check, or success that did not occur.
4. Preserve exact identifiers, numbers, dates, source references, negative evidence, contradictions, confidence limitations, unresolved questions, and hard constraints.
5. Preserve **normative strength**. BLOCKED is not MAYBE; DENIED is not SUGGESTED; UNKNOWN is not VERIFIED. A sender's claim never becomes an authorized decision through rephrasing.
6. For agent-to-agent exchange, use the receiving tool/schema's required fields and statuses. Do not add surrounding prose or prose copies of fields already present.
7. For human answers, be as short as the task permits; provide necessary explanation when it materially affects correctness, safety, accountability, or the user's decision.
8. Do not silently compress, redact or alter immutable records. Keep canonical source and evidence accessible through their existing references.
9. Do not invoke a second model merely to shorten text. If the model cannot honor the required output structure, report that limitation instead of silently inventing a compliant result.

This skill is an **output-generation policy**, not an authority, truth verifier, transport, or post-hoc semantic equivalence proof. Existing project schemas and higher-priority requirements take precedence.
