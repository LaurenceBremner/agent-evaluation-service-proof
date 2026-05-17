from fastapi import FastAPI

from agent_eval_service.models import ScoreRequest, ScoreSummary
from agent_eval_service.scoring import SCORING_VERSION, score_request

app = FastAPI(
    title="Agent Evaluation Service",
    version=SCORING_VERSION,
    description="Synthetic AI workflow evaluation service with deterministic scoring and rollout gates.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "service": "agent-evaluation-service",
        "status": "ready",
        "scoring_version": SCORING_VERSION,
    }


@app.post("/score", response_model=ScoreSummary)
def score(payload: ScoreRequest) -> ScoreSummary:
    return score_request(payload)
