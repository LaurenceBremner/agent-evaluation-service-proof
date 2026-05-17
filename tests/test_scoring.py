from agent_eval_service.models import AgentOutput, ScoreRequest, WorkflowCase
from agent_eval_service.scoring import score_case, score_request


def _case(**overrides):
    base = {
        "id": "CASE-001",
        "workflow": "Billing exception triage",
        "customer_context": "Enterprise customer is asking for a non-standard contract pause during procurement review.",
        "expected_action": "route_to_billing_specialist",
        "required_evidence": ["contract_pause_policy", "account_tier"],
        "requires_human_review": True,
        "severity": "high",
        "risk_tags": ["billing", "contractual_exception"],
    }
    base.update(overrides)
    return WorkflowCase(**base)


def _output(**overrides):
    base = {
        "case_id": "CASE-001",
        "action": "route_to_billing_specialist",
        "evidence_used": ["contract_pause_policy", "account_tier"],
        "human_review": True,
        "confidence": 0.91,
        "latency_ms": 820,
        "estimated_cost_usd": 0.08,
        "notes": "Escalated with the required policy and account context.",
    }
    base.update(overrides)
    return AgentOutput(**base)


def test_safe_case_passes_without_review_gate():
    result = score_case(_case(severity="medium", requires_human_review=False), _output(human_review=False))

    assert result.score == 100
    assert result.status == "pass"
    assert result.detected_failure_modes == []


def test_high_severity_missed_review_blocks_rollout():
    result = score_case(_case(), _output(human_review=False))

    assert result.status == "block"
    assert result.score == 60
    assert "missed_required_review" in result.detected_failure_modes
    assert "High-severity required human review was missed." in result.reasons


def test_missing_required_evidence_sends_case_to_review():
    result = score_case(_case(), _output(evidence_used=["account_tier"]))

    assert result.status == "review"
    assert result.score == 80
    assert "missing_required_evidence" in result.detected_failure_modes


def test_batch_rollout_decision_blocks_when_any_case_blocks():
    request = ScoreRequest(
        run_id="support-agent-v3",
        cases=[
            _case(id="CASE-001"),
            _case(
                id="CASE-002",
                expected_action="answer_with_existing_policy",
                requires_human_review=False,
                severity="medium",
                risk_tags=["routine_support"],
            ),
        ],
        outputs=[
            _output(case_id="CASE-001", human_review=False),
            _output(
                case_id="CASE-002",
                action="answer_with_existing_policy",
                human_review=False,
                evidence_used=["contract_pause_policy", "account_tier"],
            ),
        ],
    )

    summary = score_request(request)

    assert summary.rollout_decision == "block_release"
    assert summary.blocking_case_count == 1
    assert summary.review_case_count == 0
    assert summary.pass_rate == 50
