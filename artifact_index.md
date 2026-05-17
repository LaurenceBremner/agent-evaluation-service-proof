# Artifact Index

| Path | Type | Verification command | Pass status | Blocker |
| --- | --- | --- | --- | --- |
| `README.md` | Project overview | `test -s README.md` | Pass | None |
| `agent_eval_service/main.py` | FastAPI service boundary | `python3 -m pytest tests/test_api.py` | Pass: 3/3 tests | None |
| `agent_eval_service/models.py` | Pydantic request/response validation | `python3 -m pytest tests/test_api.py tests/test_scoring.py` | Pass: 7/7 tests | None |
| `agent_eval_service/failure_modes.py` | Failure-mode taxonomy | `python3 -m pytest tests/test_scoring.py` | Pass: 4/4 tests | None |
| `agent_eval_service/scoring.py` | Deterministic scoring and rollout gates | `python3 -m pytest tests/test_scoring.py tests/test_sample_dataset.py` | Pass: 5/5 tests | None |
| `data/sample_eval_dataset.json` | Synthetic eval dataset | `python3 -m pytest tests/test_sample_dataset.py` | Pass: 1/1 test | None |
| `tests/` | Pytest suite | `python3 -m pytest tests` | Pass: 8/8 tests | None |
| `runbook.md` | Rollout and rollback operating notes | `test -s runbook.md` | Pass | None |
