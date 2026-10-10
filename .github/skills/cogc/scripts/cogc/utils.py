from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ0-9_./:-]+", re.UNICODE)
NUMBER_RE = re.compile(r"(?<!\w)[+-]?(?:\d{1,3}(?:[.,]\d{3})+|\d+)(?:[.,]\d+)?(?:\s?[%€$£¥])?(?!\w)")
IDENTIFIER_RE = re.compile(
    r"\b(?:[A-Z]{2,}[A-Z0-9_-]*\d+[A-Z0-9_.:-]*|[A-Z]{2,}(?:[-_][A-Z0-9]+)+|[A-Fa-f0-9]{8,}|[A-Z]{2,}\d{2,})\b"
)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")


def estimate_tokens(text: str) -> int:
    """Dependency-free approximation; never presented as provider billing tokens."""
    return len(TOKEN_RE.findall(text or ""))


def canonicalize(text: str) -> str:
    return " ".join((text or "").replace("\x00", " ").split())


def content_hash(parts: Iterable[str]) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8", errors="replace"))
        h.update(b"\x00")
    return h.hexdigest()


def keyword_set(text: str) -> set[str]:
    stop = {
        "the", "and", "for", "with", "that", "this", "from", "into", "are", "was", "were",
        "der", "die", "das", "und", "mit", "für", "von", "ist", "sind", "ein", "eine", "einer",
        "to", "of", "in", "on", "or", "a", "an", "be", "as", "at", "by", "it", "is",
    }
    return {w.lower() for w in WORD_RE.findall(text or "") if len(w) > 2 and w.lower() not in stop}


def sentence_split(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_RE.split(text or "") if s.strip()]


def exact_numbers(text: str) -> set[str]:
    return {m.group(0).strip() for m in NUMBER_RE.finditer(text or "")}


def identifiers(text: str) -> set[str]:
    return {m.group(0) for m in IDENTIFIER_RE.finditer(text or "")}
