from dataclasses import dataclass
from typing import List, Optional
from .rules import Rule, default_rules

@dataclass
class Finding:
    rule_name: str
    description: str
    severity: int
    matches: List[str]


@dataclass
class DetectionResult:
    text: str
    score: int
    findings: List[Finding]


class PromptSentryDetector:
    """
    Core detection engine.

    Applies rules to text and computes a suspicion score.
    """

    def __init__(self, rules: Optional[List[Rule]] = None) -> None:
        self.rules: List[Rule] = rules if rules is not None else default_rules()

    def analyze(self, text: str) -> DetectionResult:
        score = 0
        findings: List[Finding] = []

        for rule in self.rules:
            matches = rule.find_matches(text)

            if matches:
                score += rule.severity
                findings.append(
                    Finding(
                        rule_name=rule.name,
                        description=rule.description,
                        severity=rule.severity,
                        matches=matches[:5],
                    )
                )

        return DetectionResult(text=text, score=score, findings=findings)