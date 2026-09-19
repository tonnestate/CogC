# Criticality Model

CogC protects information according to six classes.

| Class | Meaning | Compression rule |
|---|---|---|
| C0 | Immutable critical | Keep verbatim; never lossy-compress |
| C1 | Critical | Normalize only; preserve exact meaning, numbers, IDs and source refs |
| C2 | High value | Keep when relevant; extractive shortening permitted |
| C3 | Supporting | Rank by task relevance and budget |
| C4 | Redundant | Remove after provenance-safe deduplication |
| C5 | Noise | Remove unless explicitly requested |

Examples of C0 include high-priority operator instructions, authorization boundaries, payment limits, execution controls, legal constraints, immutable IDs and explicit stop conditions.

Explicit classification supplied by the caller always overrides heuristic classification. The heuristic classifier is a convenience mechanism, not an authority boundary.
