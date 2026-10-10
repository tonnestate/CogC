from cogc import CompileRequest, Criticality, SourceItem, TargetProfile, compile_request


def test_duplicate_sources_upgrade_to_strongest_criticality():
    statement = "REUSE_DENIED because the signed decision is BLOCKED."
    req = CompileRequest(
        goal="Transfer decision unchanged",
        task="Pass through state",
        sources=[
            SourceItem(id="older-optional", text=statement, criticality=Criticality.C4_REDUNDANT),
            SourceItem(id="canonical-blocker", text=statement, criticality=Criticality.C0_IMMUTABLE),
        ],
        token_budget=512,
        target=TargetProfile(context_budget=512),
    )
    packet = compile_request(req)
    assert packet.fidelity.passed
    assert len(packet.immutable) == 1
    assert packet.immutable[0].criticality == Criticality.C0_IMMUTABLE
    assert packet.immutable[0].source_refs == ["older-optional", "canonical-blocker"]
    assert not packet.facts


def test_duplicate_high_priority_is_not_lost_under_tiny_budget():
    statement = "AUTHORITY=DENIED; STATUS=BLOCKED; DO_NOT_EXECUTE."
    req = CompileRequest(
        goal="Execute only if authorized",
        task="Evaluate action",
        sources=[
            SourceItem(id="old", text=statement, criticality=Criticality.C5_NOISE),
            SourceItem(id="binding", text=statement, criticality=Criticality.C1_CRITICAL),
        ],
        token_budget=1,
    )
    packet = compile_request(req)
    assert packet.receipt.over_budget_due_to_critical
    assert len(packet.immutable) == 1
    assert packet.immutable[0].text == statement
    assert packet.immutable[0].criticality == Criticality.C1_CRITICAL
