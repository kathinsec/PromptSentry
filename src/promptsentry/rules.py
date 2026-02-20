from dataclasses import dataclass
import re
from typing import Pattern, List

@dataclass(frozen=True)
class Rule:
    """
    A Rule describes one suspicious pattern.

    name        -> short identifier
    description -> human explanation
    severity    -> score weight
    pattern     -> compiled regex
    """
    name: str
    description: str
    severity: int
    pattern: Pattern[str]

    def find_matches(self, text: str) -> List[str]:
        return [m.group(0) for m in self.pattern.finditer(text)]


def default_rules() -> List[Rule]:
    return [
        Rule(
            name="instruction_override",
            description="Attempts to override earlier instructions",
            severity=8,
            pattern=re.compile(
                r"\b(ignore|disregard|forget)\b.*\b(previous|prior|earlier)\b.*\b(instructions|rules|messages)\b",
                re.IGNORECASE | re.DOTALL,
            ),
        ),
        Rule(
            name="system_prompt_request",
            description="Requests for hidden system prompt or policies",
            severity=10,
            pattern=re.compile(
                r"\b(reveal|show|print|dump|leak)\b.*\b(system prompt|hidden prompt|policy|internal)\b",
                re.IGNORECASE | re.DOTALL,
            ),
        ),
        Rule(
            name="role_manipulation",
            description="Attempts to change assistant roles or modes",
            severity=8,
            pattern=re.compile(
                r"\byou are now\b.*\b(system|developer|admin|root)\b",
                re.IGNORECASE | re.DOTALL,
            ),
        ),
        Rule(
            name="exfiltration_everything_above",
            description="Attempts to extract prior context ('everything above').",
            severity=9,
            pattern=re.compile(
                r"\b(print|show|dump|output)\b.*\b(everything|all)\b.*\b(above|previous|prior)\b",
                re.IGNORECASE | re.DOTALL,
            ),
        ),
    ]