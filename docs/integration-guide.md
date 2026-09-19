# Integration Guide

CogC is intended to sit between state assembly and execution.

A typical integration is:

```text
Task / Goal
  ↓
Retrieval / Evidence / Memory assembly
  ↓
Target worker selection or capacity profile
  ↓
CogC
  ↓
Worker / specialist / agent team
  ↓
Verification
  ↓
Action / result
  ↓
Outcome telemetry
```

If routing happens before compilation, pass the selected target profile directly to CogC.

If routing happens after initial state assembly, construct a neutral Cognitive Intermediate Representation first and perform the final capacity-specific compilation once the worker class is known.

CogC is an optimization layer, not an authorization dependency. If CogC is unavailable or its Fidelity Gate fails, fall back to a less compressed representation or raw context where safe.

Recommended telemetry:

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

For learning systems, retain the tuple:

```text
task class
× target model
× compression policy
× compression ratio
× verified downstream outcome
```

This is the minimum useful basis for later target-specific compression policies.
