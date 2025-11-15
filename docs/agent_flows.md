# Agent Flows — USAA

This document describes the runtime flows for each agent, the decision points inside the Router, expected inputs/outputs, and failure/retry handling. This is written as an engineering log so reviewers can see the design thinking and expected behaviors.

---

## Overview

USAA exposes three primary agent roles:
- **Logic Agent** — deterministic, stepwise reasoning tasks: planning, workflows, technical breakdowns.
- **Creative Agent** — ideation, rewrite, UX copy, user-facing text generation.
- **Research Agent** — fact grounding, source consolidation, contradiction detection.

Agents may be invoked singly or in combination. The Router decides based on intent, confidence, and system policy. The Orchestrator (`usaa_brain.py`) coordinates multi-agent flows and final aggregation.

---

## Common primitives

- **Task**: internal unit of work (dict)
  - `id` (str) — unique
  - `type` (str) — e.g., "summarize", "plan", "research", "rewrite"
  - `payload` (any) — input content
  - `context` (dict) — conversation/context metadata
  - `meta` (dict) — routing hints (optional)

- **AgentResponse**:
  - `task_id` (str)
  - `agent` (str)
  - `engine` (str)
  - `output` (str or structured)
  - `confidence` (float 0..1) — optional, if engine returns
  - `logs` (list) — step trace

---

## Flow A — Single-Agent (simple request)

1. **User request** → `main.py` constructs Task.
2. Router analyzes intent (fast heuristic + prompt-based classifier).
3. Router selects single agent (e.g., "Creative Agent").
4. Router forwards Task to chosen agent.
5. Agent formats prompt, calls its engine wrapper, receives result.
6. Agent post-processes (cleaning, safety checks).
7. Agent returns `AgentResponse` to `usaa_brain`.
8. `usaa_brain` aggregates (single response), final formatting, return.

**Example**: `Rewrite this paragraph to be friendlier.` → Creative Agent → OpenAI

---

## Flow B — Multi-Agent (composite request)

1. **User request** ⇒ complex `Task` (e.g., "Make a research brief + 3-step plan + creative intro").
2. Router decomposes into subtasks:
   - `research_subtask` → Research Agent
   - `plan_subtask` → Logic Agent
   - `intro_subtask` → Creative Agent
3. Each subtask executed (parallel where safe).
4. Agents return `AgentResponse`s.
5. `usaa_brain` runs **merge policy**:
   - Validate research facts via Research Agent confidence.
   - If contradictions: spawn a follow-up Research Agent query to "Disagreement Hunter" mode.
   - Synthesize plan using Logic Agent + research citations.
   - Have Creative Agent produce final intro using plan + validated facts.
6. Final aggregator composes sections and returns final result.

**Example**: "Prepare a 1-page actionable brief on X with 3 recommended steps and a catchy intro."

---

## Flow C — Iterative Refinement / Debate

Used when correctness matters (e.g., technical instructions, compliance).

1. Router sends initial query to Research Agent.
2. If Research Agent returns low confidence or contradictory evidence:
   - Spin up a second Research Agent pass using alternate search prompt.
   - Optionally route contradiction to Logic Agent for reasoning about tradeoffs.
3. Use a **voting / adjudication** strategy:
   - If >1 agent agrees on core facts → mark as validated.
   - If no consensus → mark "requires human review" and provide trace.

**Why**: This reduces blind trust in single LLM outputs and provides audit trail.

---

## Failure modes & recovery

- **Engine timeout** → Retry up to 2 times with exponential backoff; if still failing, escalate to fallback agent (e.g., if Gemini times out, run a reduced Creative Agent path for partial response).
- **Low confidence** → If Research Agent confidence < threshold (0.5), spawn additional research pass.
- **Contradiction detected** → Create "disagreement task" and log all sources & exact conflicting claims.
- **Rate limit / quota** → Graceful degrade: return a clear message explaining partial output + "Try again" option.

---

## Logging & Traceability

- Each `Task` and `AgentResponse` must be logged (timestamped).
- Keep a minimal **conversation trace** for reproducing runs: prompt snapshots, engine raw outputs (truncated), and selection rationale.
- Provide `--export-trace` option in `usaa_brain` to serialize run into `_traces/` for offline inspection.

---

## Example mapping: intent → agent

- `summarize/rewrite` → Creative Agent
- `plan/stepwise/instruction` → Logic Agent
- `verify/fact-check` → Research Agent
- `multi-objective` → Router decomposes into Research + Logic + Creative

---

## Notes to Reviewers (human-signal)

- Documented decisions (e.g., why Logic uses Gemini) are included intentionally to show human tradeoffs.
- The design favors clear, deterministic fallback behaviors — this is a feature, not AI-avoidance.
