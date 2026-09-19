# Cognitive Intermediate Representation (CIR)

CIR is the stable representation between source assembly and compression.

Each unit contains:

- `id`: stable source/unit identifier;
- `text`: canonicalized content;
- `kind`: semantic type such as constraint, evidence, workflow or observation;
- `criticality`: C0–C5;
- `source_refs`: original source handles;
- `metadata`: optional machine-readable context;
- `score`: task-relevance score assigned during compilation.

CogC v0.2.0 intentionally keeps CIR simple. It does not invent an ontology for the whole company. The representation exists to make compression inspectable and testable.
