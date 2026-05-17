from agent_eval_service.failure_modes import BLOCKING_FAILURES, REVIEW_FAILURES, FailureMode
from agent_eval_service.models import AgentOutput, CaseScore, ScoreRequest, ScoreSummary, WorkflowCase

SCORING_VERSION = "2026-05-16"


def _status_for(score: int, severity: str, failure_modes: list[FailureMode]) -> str:
    blocking_failure = any(mode in BLOCKING_FAILURES for mode in failure_modes)
    review_failure = any(mode in REVIEW_FAILURES for mode in failure_modes)

    if score < 70 or (severity == "high" and blocking_failure):
        return "block"
    if score < 85 or review_failure:
        return "review"
    return "pass"


def _clamp_score(score: int) -> int:
    return max(0, min(100, score))


def score_case(workflow_case: WorkflowCase, output: AgentOutput) -> CaseScore:
    score = 100
    failure_modes: list[FailureMode] = []
    reasons: list[str] = []

    if output.action != workflow_case.expected_action:
        score -= 30
        failure_modes.append("action_mismatch")
        reasons.append("Agent selected an action that does not match the expected workflow decision.")

    missing_evidence = sorted(set(workflow_case.required_evidence) - set(output.evidence_used))
    if missing_evidence:
        score -= 20
        failure_modes.append("missing_required_evidence")
        reasons.append(f"Missing required evidence: {', '.join(missing_evidence)}.")

    if workflow_case.requires_human_review and not output.human_review:
        score -= 40
        failure_modes.append("missed_required_review")
        reasons.append("High-severity required human review was missed.")

    if not workflow_case.requires_human_review and output.human_review:
        score -= 10
        failure_modes.append("unnecessary_review")
        reasons.append("Workflow was escalated when automated handling was acceptable.")

    if output.confidence < 0.72:
        score -= 15
        failure_modes.append("low_confidence")
        reasons.append("Agent confidence fell below the review threshold.")

    if output.latency_ms > 2500:
        score -= 10
        failure_modes.append("latency_budget_exceeded")
        reasons.append("Agent response exceeded the latency budget.")

    if output.estimated_cost_usd > 0.50:
        score -= 10
        failure_modes.append("cost_budget_exceeded")
        reasons.append("Agent response exceeded the per-case cost budget.")

    final_score = _clamp_score(score)
    return CaseScore(
        case_id=workflow_case.id,
        score=final_score,
        status=_status_for(final_score, workflow_case.severity, failure_modes),
        severity=workflow_case.severity,
        detected_failure_modes=failure_modes,
        reasons=reasons,
    )


def _missing_output_score(workflow_case: WorkflowCase) -> CaseScore:
    return CaseScore(
        case_id=workflow_case.id,
        score=0,
        status="block",
        severity=workflow_case.severity,
        detected_failure_modes=["action_mismatch"],
        reasons=["No agent output was provided for this workflow case."],
    )


def score_request(request: ScoreRequest) -> ScoreSummary:
    outputs_by_case_id = {output.case_id: output for output in request.outputs}
    case_scores = [
        score_case(workflow_case, outputs_by_case_id[workflow_case.id])
        if workflow_case.id in outputs_by_case_id
        else _missing_output_score(workflow_case)
        for workflow_case in request.cases
    ]

    pass_count = sum(case_score.status == "pass" for case_score in case_scores)
    blocking_count = sum(case_score.status == "block" for case_score in case_scores)
    review_count = sum(case_score.status == "review" for case_score in case_scores)
    average_score = round(sum(case_score.score for case_score in case_scores) / len(case_scores))

    if blocking_count:
        rollout_decision = "block_release"
    elif review_count:
        rollout_decision = "human_review_gate"
    else:
        rollout_decision = "controlled_rollout"

    return ScoreSummary(
        run_id=request.run_id,
        rollout_decision=rollout_decision,
        pass_rate=round((pass_count / len(case_scores)) * 100),
        average_score=average_score,
        blocking_case_count=blocking_count,
        review_case_count=review_count,
        case_scores=case_scores,
    )

