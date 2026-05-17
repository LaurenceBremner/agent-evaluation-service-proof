# Evidence Log

## 2026-05-16

- Added tests first for scoring behavior, API behavior, and sample data scoring.
- Verified red state after dependency setup: tests failed because `agent_eval_service.main` and `agent_eval_service.models` did not exist.
- Implemented FastAPI service, Pydantic models, deterministic scoring, failure taxonomy, and sample synthetic dataset.
- Verified `python3 -m pytest tests` with 8 passing tests after installing the project requirements.

## Dependency Note

Use a repo-local virtual environment, for example `python3 -m venv .venv`, then install `requirements.txt`. The `.venv/` directory should stay local and should not be committed.
