from cogc.criticality import classify
from cogc.models import Criticality, SourceItem


def test_explicit_criticality_wins() -> None:
    item = SourceItem(id="X", text="ordinary text", criticality=Criticality.C0_IMMUTABLE)
    assert classify(item) == Criticality.C0_IMMUTABLE


def test_owner_instruction_is_immutable() -> None:
    item = SourceItem(id="X", kind="owner_instruction", text="Owner approval required")
    assert classify(item) == Criticality.C0_IMMUTABLE


def test_chitchat_is_noise() -> None:
    item = SourceItem(id="X", kind="chitchat", text="hello")
    assert classify(item) == Criticality.C5_NOISE
