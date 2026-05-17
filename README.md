# Agent Evaluation Service

FastAPI/Pydantic service for scoring AI workflow outputs and returning rollout gates.

Live page: https://laurencebremner.github.io/agent-evaluation-service-proof/

## What It Shows

- A real service boundary: `GET /health` and `POST /score`.
- Pydantic request and response validation.
- Deterministic penalties for action mismatch, missing evidence, missed human review, low confidence, cost, and latency.
- A browser demo with memory-only BYO OpenAI API key check, tiny Responses API eval calls when a key is supplied, and mock fallback when it is not.
- Pytest coverage for API behavior, scoring, and sample data.

## Method

The method is documented in [`METHODOLOGY.md`](METHODOLOGY.md). In short: define expected actions and required evidence, validate outputs, score deterministically, and map the run to controlled rollout, human-review gate, or blocked release.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest tests
python3 -m uvicorn agent_eval_service.main:app --reload
```

## Key Files

- `agent_eval_service/main.py`: FastAPI app.
- `agent_eval_service/models.py`: Pydantic schemas.
- `agent_eval_service/scoring.py`: deterministic scoring logic.
- `agent_eval_service/failure_modes.py`: failure taxonomy.
- `data/sample_eval_dataset.json`: sample request.
- `tests/`: API, scoring, and fixture tests.
- `docs/index.html`: public demo page.
- `METHODOLOGY.md`: rationale, method, worked example, failure modes, and next steps.

## Boundary

The service uses synthetic data. It does not implement production auth, rate limiting, persistence, audit-log storage, secrets management, tenant isolation, or model-output provenance.
