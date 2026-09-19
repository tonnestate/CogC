from cogc.fidelity import verify_fidelity
from cogc.models import CIRUnit, Criticality


def unit(text: str) -> CIRUnit:
    return CIRUnit(
        id="AUTH-1",
        text=text,
        kind="authorization",
        criticality=Criticality.C0_IMMUTABLE,
        source_refs=["AUTH-1"],
    )


def test_missing_critical_number_fails() -> None:
    u = unit("Payment limit is 500 EUR for CASE-9001.")
    report = verify_fidelity([u], [u], "Payment limit applies to CASE-9001.")
    assert not report.passed
    assert "500" in " ".join(report.missing_numbers)


def test_full_critical_text_passes() -> None:
    u = unit("Payment limit is 500 EUR for CASE-9001.")
    report = verify_fidelity([u], [u], "Payment limit is 500 EUR for CASE-9001.")
    assert report.passed
