# Compression Policies

CogC v0.2.0 ships one production-ready policy: `deterministic`.

It performs:

1. whitespace canonicalization;
2. exact content deduplication;
3. criticality classification;
4. task relevance scoring;
5. C5 noise removal;
6. C0/C1 unconditional retention;
7. extractive sentence selection for non-critical long units;
8. reversible folding of omitted units behind source handles.

Future backends may include LLMLingua-family compression or ACON-inspired learned policies. Such backends must remain optional until they beat the deterministic/raw baselines on downstream verified outcomes.
