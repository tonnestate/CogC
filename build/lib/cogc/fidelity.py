from __future__ import annotations

from .models import CIRUnit, FidelityReport
from .utils import exact_numbers, identifiers


def verify_fidelity(original: list[CIRUnit], kept: list[CIRUnit], rendered_text: str) -> FidelityReport:
    critical = [u for u in original if int(u.criticality) <= 1]
    kept_ids = {u.id for u in kept}
    missing_critical = [u.id for u in critical if u.id not in kept_ids]
    critical_retention = 1.0 if not critical else (len(critical) - len(missing_critical)) / len(critical)

    critical_text = "\n".join(u.text for u in critical)
    nums = exact_numbers(critical_text)
    ids = identifiers(critical_text)
    missing_nums = sorted(v for v in nums if v not in rendered_text)
    missing_ids = sorted(v for v in ids if v not in rendered_text)
    number_retention = 1.0 if not nums else (len(nums) - len(missing_nums)) / len(nums)
    id_retention = 1.0 if not ids else (len(ids) - len(missing_ids)) / len(ids)

    warnings: list[str] = []
    if missing_nums:
        warnings.append("Critical numeric values were lost.")
    if missing_ids:
        warnings.append("Critical identifiers were lost.")
    if missing_critical:
        warnings.append("One or more C0/C1 units were not retained.")

    passed = not missing_critical and not missing_nums and not missing_ids
    return FidelityReport(
        passed=passed,
        critical_retention=critical_retention,
        exact_number_retention=number_retention,
        exact_identifier_retention=id_retention,
        missing_critical_ids=missing_critical,
        missing_numbers=missing_nums,
        missing_identifiers=missing_ids,
        warnings=warnings,
    )
