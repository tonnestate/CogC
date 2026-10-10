# Fidelity Contract

Compression is acceptable only if the package preserves what the worker requires to act correctly.

The v0.2.1 Fidelity Gate is intentionally strict about protected material:

1. every C0/C1 CIR unit must remain in the package;
2. numbers present in protected material must remain exact;
3. machine-like identifiers present in protected material must remain exact;
4. retained units must preserve source handles.

This gate does not prove semantic equivalence. Downstream A/B/C evaluation remains required.

If fidelity fails, reduce compression aggressiveness or return raw context. Never silently waive the gate.
