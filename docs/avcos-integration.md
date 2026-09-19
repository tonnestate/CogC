# AVCOS Integration

Recommended position:

```text
IntakeGov
  ↓
SPARI
  ↓
Evidence / RAG / Graph / Memory assembly
  ↓
CogC
  ↓
Meta-Cognitive Router / Bandit
  ↓
Local worker / Expert Room / OmniRoute specialist
  ↓
Verification
  ↓
Governor / Execution Boundary
  ↓
Reality outcome
  ↓
Learning
```

CogC should receive the target executor profile after the system has enough information to know which worker class it is preparing for. If routing happens after CogC in a given architecture, compile a neutral CIR first and perform the final capacity-specific compilation after route selection.

CogC must not become an authorization dependency. If CogC is unavailable, fall back to less compressed or raw context where safe.

Recommended AVCOS telemetry additions:

- `cogc_version`
- `compression_policy`
- `target_profile`
- `source_token_estimate`
- `compiled_token_estimate`
- `compression_ratio`
- `critical_retention`
- `fidelity_passed`
- `expand_count`
- `downstream_verified_success`
- `escalation_after_compression`
