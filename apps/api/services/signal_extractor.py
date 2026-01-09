from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Signal:
    type: str
    confidence: float
    keywords: List[str]


# Keep it small + high-signal. You can expand later.
_RULES = {
    "sanctions": ["sanction", "ofac", "blacklist", "export control", "restricted entity"],
    "regulatory_action": ["regulator", "fine", "penalty", "consent order", "enforcement", "compliance failure"],
    "fraud": ["fraud", "money laundering", "aml", "bribery", "embezzlement", "insider trading"],
    "lawsuit": ["lawsuit", "sued", "litigation", "court", "class action", "settlement"],
    "data_breach": ["data breach", "breach", "leak", "ransomware", "hack", "compromised"],
    "bankruptcy": ["bankruptcy", "chapter 11", "insolvent", "restructuring", "default"],
}

_WORD_RE = re.compile(r"[a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)?")

def extract_signals(text: str) -> List[Signal]:
    if not text:
        return []

    lower = text.lower()
    found: List[Signal] = []

    for signal_type, keywords in _RULES.items():
        hits = [kw for kw in keywords if kw in lower]
        if not hits:
            continue

        # simple confidence: more keyword hits => higher confidence (cap at 1.0)
        confidence = min(1.0, 0.4 + 0.2 * len(hits))
        found.append(Signal(type=signal_type, confidence=confidence, keywords=hits[:5]))

    # sort: highest confidence first
    found.sort(key=lambda s: s.confidence, reverse=True)
    return found
