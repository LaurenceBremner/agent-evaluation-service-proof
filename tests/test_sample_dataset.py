import json
from pathlib import Path

from agent_eval_service.models import ScoreRequest
from agent_eval_service.scoring import score_request


def test_sample_dataset_scores_to_human_review_gate():
    dataset_path = Path("data/sample_eval_dataset.json")
    payload = json.loads(dataset_path.read_text())

    summary = score_request(ScoreRequest(**payload))

    assert summary.run_id == "synthetic-agent-release-2026-05-16"
    assert summary.rollout_decision == "human_review_gate"
    assert summary.review_case_count == 2
    assert summary.blocking_case_count == 0
