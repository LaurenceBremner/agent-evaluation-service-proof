from fastapi.testclient import TestClient

from agent_eval_service.main import app


client = TestClient(app)


def test_health_endpoint_reports_service_ready():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "agent-evaluation-service",
        "status": "ready",
        "scoring_version": "2026-05-16",
    }


def test_score_endpoint_returns_case_scores_and_rollout_gate():
    payload = {
        "run_id": "support-agent-v3",
        "cases": [
            {
                "id": "CASE-001",
                "workflow": "Billing exception triage",
                "customer_context": "Enterprise customer asks for a non-standard contract pause during procurement review.",
                "expected_action": "route_to_billing_specialist",
                "required_evidence": ["contract_pause_policy", "account_tier"],
                "requires_human_review": True,
                "severity": "high",
                "risk_tags": ["billing", "contractual_exception"],
            }
        ],
        "outputs": [
            {
                "case_id": "CASE-001",
                "action": "route_to_billing_specialist",
                "evidence_used": ["contract_pause_policy", "account_tier"],
                "human_review": True,
                "confidence": 0.91,
                "latency_ms": 820,
                "estimated_cost_usd": 0.08,
                "notes": "Escalated with required policy and account context.",
            }
        ],
    }

    response = client.post("/score", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["run_id"] == "support-agent-v3"
    assert body["rollout_decision"] == "controlled_rollout"
    assert body["case_scores"][0]["status"] == "pass"


def test_score_endpoint_rejects_invalid_confidence():
    payload = {
        "run_id": "support-agent-v3",
        "cases": [
            {
                "id": "CASE-001",
                "workflow": "Billing exception triage",
                "customer_context": "Enterprise customer asks for a non-standard contract pause during procurement review.",
                "expected_action": "route_to_billing_specialist",
                "required_evidence": ["contract_pause_policy"],
                "requires_human_review": True,
                "severity": "high",
                "risk_tags": ["billing"],
            }
        ],
        "outputs": [
            {
                "case_id": "CASE-001",
                "action": "route_to_billing_specialist",
                "evidence_used": ["contract_pause_policy"],
                "human_review": True,
                "confidence": 1.4,
                "latency_ms": 820,
                "estimated_cost_usd": 0.08,
                "notes": "Confidence should be rejected.",
            }
        ],
    }

    response = client.post("/score", json=payload)

    assert response.status_code == 422
