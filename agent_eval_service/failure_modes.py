from typing import Literal

FailureMode = Literal[
    "action_mismatch",
    "missing_required_evidence",
    "missed_required_review",
    "unnecessary_review",
    "low_confidence",
    "latency_budget_exceeded",
    "cost_budget_exceeded",
]

BLOCKING_FAILURES = {"action_mismatch", "missed_required_review"}
REVIEW_FAILURES = {
    "missing_required_evidence",
    "unnecessary_review",
    "low_confidence",
    "latency_budget_exceeded",
    "cost_budget_exceeded",
}

