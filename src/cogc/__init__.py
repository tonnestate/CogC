"""CogC — Capacity-Aware Cognitive Compression."""

from .core import compile_request
from .models import (
    CognitivePackage,
    CompileRequest,
    Criticality,
    FidelityReport,
    SourceItem,
    TargetProfile,
)

__all__ = [
    "compile_request",
    "CognitivePackage",
    "CompileRequest",
    "Criticality",
    "FidelityReport",
    "SourceItem",
    "TargetProfile",
]

__version__ = "0.2.0"
