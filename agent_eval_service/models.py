from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from agent_eval_service.failure_modes import FailureMode

Severity = Literal["low", "medium", "high"]
CaseStatus = Literal["pass", "review", "block"]
RolloutDecision = Literal["controlled_rollout", "human_review_gate", "block_release"]


class WorkflowCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    workflow: str = Field(min_length=1)
    customer_context: str = Field(min_length=1)
    expected_action: str = Field(min_length=1)
    required_evidence: list[str] = Field(default_factory=list)
    requires_human_review: bool
    severity: Severity
    risk_tags: list[str] = Field(default_factory=list)


class AgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    action: str = Field(min_length=1)
    evidence_used: list[str] = Field(default_factory=list)
    human_review: bool
    confidence: float = Field(ge=0, le=1)
    latency_ms: int = Field(ge=0)
    estimated_cost_usd: float = Field(ge=0)
    notes: str = Field(default="")


class CaseScore(BaseModel):
    case_id: str
    score: int = Field(ge=0, le=100)
    status: CaseStatus
    severity: Severity
    detected_failure_modes: list[FailureMode]
    reasons: list[str]


class ScoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    cases: list[WorkflowCase] = Field(min_length=1)
    outputs: list[AgentOutput] = Field(min_length=1)


class ScoreSummary(BaseModel):
    run_id: str
    rollout_decision: RolloutDecision
    pass_rate: int = Field(ge=0, le=100)
    average_score: int = Field(ge=0, le=100)
    blocking_case_count: int = Field(ge=0)
    review_case_count: int = Field(ge=0)
    case_scores: list[CaseScore]

