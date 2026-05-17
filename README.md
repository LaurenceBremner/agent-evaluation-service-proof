# Production-Style Agent Evaluation Service

A small FastAPI/Pydantic service for turning synthetic AI workflow cases into scored rollout decisions.

## Overview

This project focuses on a narrow deployment question: can a simple eval service catch AI workflow outputs that sound plausible but should not ship?

The scenario is a support/account-risk assistant. Each synthetic case defines the expected action, required evidence, severity, review requirement, and operational limits. The service scores proposed agent outputs against those expectations and returns pass/fail status, detected failure modes, average score, pass rate, and a rollout gate.

## Service Shape

- `GET /health` returns service readiness and scoring version.
- `POST /score` accepts workflow cases plus agent outputs and returns case scores, detected failure modes, pass rate, average score, and rollout gate.
- Pydantic models enforce request shape, confidence bounds, non-negative cost/latency, and allowed severity/status values.
- Deterministic scoring keeps the result explainable in interviews and reviewable in tests.

## What It Shows

- A service boundary around AI-output evaluation rather than a dashboard-only artifact.
- Explicit expected-action and evidence checks.
- Human-review thresholds for risky workflow cases.
- Cost, latency, confidence, and hallucinated-policy penalties.
- Rollout gates that separate controlled rollout, review-gated rollout, and blocked release.

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest tests
python3 -m uvicorn agent_eval_service.main:app --reload
```

Example score payload:

```bash
curl -X POST http://127.0.0.1:8000/score \
  -H 'Content-Type: application/json' \
  --data @data/sample_eval_dataset.json
```

## Limits

- Uses synthetic data only.
- No authentication, rate limiting, audit log sink, persistence layer, background worker, or model invocation is implemented.
- No Kubernetes, private cloud, multi-tenant isolation, or enterprise network deployment is claimed.
- The service boundary is intentionally small: validation, scoring, failure taxonomy, and rollout decisioning.
- Production use would require auth, request tracing, durable logs, secrets management, tenant isolation, alerting, and model-output provenance.

## Evidence

- Service entry point: `agent_eval_service/main.py`
- Request and response models: `agent_eval_service/models.py`
- Failure taxonomy: `agent_eval_service/failure_modes.py`
- Scoring logic: `agent_eval_service/scoring.py`
- Sample data: `data/sample_eval_dataset.json`
- Tests: `tests/`
- Runbook: `runbook.md`
- Artifact index: `artifact_index.md`
