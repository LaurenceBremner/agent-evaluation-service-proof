# Runbook

## Purpose

Use this service to evaluate whether a proposed AI workflow is ready for controlled rollout, needs human-review gating, or should be blocked before release.

## Inputs

- Workflow cases with expected action, required evidence, severity, risk tags, and human-review requirement.
- Agent outputs with selected action, evidence used, confidence, latency, cost, and escalation decision.

## Rollout Gates

| Decision | Trigger | Action |
| --- | --- | --- |
| `controlled_rollout` | All cases pass. | Ship to a limited cohort with post-launch monitoring. |
| `human_review_gate` | No blocking cases, but one or more cases require review. | Keep automation behind review, fix weak cases, then rerun eval. |
| `block_release` | Any case blocks. | Do not ship. Diagnose the blocking failure modes and rerun. |

## Failure Review

1. Inspect `detected_failure_modes` and `reasons` for each non-pass case.
2. Check whether failures cluster around action choice, evidence retrieval, escalation judgement, confidence, cost, or latency.
3. Update prompt, retrieval, routing, policy grounding, or review policy outside this service.
4. Rerun `/score` with the same eval cases and revised outputs.
5. Ship only after blockers are gone and review cases have explicit owners.

## Rollback Criteria

During a pilot, revert to manual or previous workflow if any of these appear:

- High-severity missed review.
- Repeated action mismatch on customer-impacting workflows.
- Missing required evidence on regulated, contractual, security, or billing cases.
- Latency or cost exceeds the budget agreed for the pilot.
- Users or operators report unexplained decisions that cannot be traced to evidence.

## Monitoring Notes

Minimum production instrumentation would include request ID, tenant/customer ID, case ID, model/prompt version, retrieval corpus version, detected failure modes, score, rollout decision, human-review owner, latency, cost, and final operator disposition.

This project does not persist those logs; it documents the operational shape the service would need.
