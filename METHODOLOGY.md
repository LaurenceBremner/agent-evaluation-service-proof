# Methodology

## Motivation

I wanted this project to prove an actual service boundary: request validation, deterministic scoring, failure modes, tests, and a rollout decision.

## What I Tried

I modeled agent outputs as data rather than judging them through a dashboard. Each request carries workflow cases, expected actions, required evidence, human-review requirements, and observed outputs.

## Method

1. Define expected action, required evidence, severity, and review requirement.
2. Validate cases and outputs with Pydantic.
3. Score each output with deterministic penalties.
4. Map each case to pass, review, or block.
5. Convert the run into controlled rollout, human-review gate, or blocked release.

## Worked Example

A support account-risk case requires invoice evidence, usage lookup evidence, and human review. If the agent answers directly or misses required evidence, the service marks the case for review or block and returns the exact penalty reasons.

## Failure Modes

- Action mismatch.
- Missing required evidence.
- Missed required human review.
- Low confidence.
- Cost or latency budget breach.

## Tradeoffs

The scorer is deterministic and easy to test. It will miss nuanced language quality issues, but it gives a clear service contract that can sit in front of model-specific review.

## Limitations

The service uses synthetic data and has no production auth, rate limiting, persistence, audit sink, tenant isolation, or model-output provenance store.

## What I Would Change Next

Add authenticated run storage, trace IDs, model-output provenance, evaluator versioning, and a separate model-judge comparison pass.
