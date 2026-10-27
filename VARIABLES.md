# Variables and controls

| Class | Recorded variable | Treatment |
|---|---|---|
| Intended fixed controls | Identical initial/current facts within pairs; condition label only in private policy metadata; disabled retained history empty; no future/stale projection; cross-case incoming h1 only under frozen handoff | Copied from `trial-plan.json`; not a preregistration claim |
| Manipulated | `continuity_enabled` versus `continuity_disabled` | One paired factor |
| Design | 6 cases × 2 conditions × 2 sessions = 24 cells; fixed node/model assignments | No randomization proof; 19 returns, 5 holds |
| Runtime changes | Startup import failure, repairs/interventions, technical refreeze before inference | Exact final-refreeze time unknown; partial order only |
| Founder role-play | Added family narrative branches after baseline | Baseline facts and scores unchanged |
| Responses | Exact task payload, raw answer, strict score, elapsed seconds, engine identity | Payload and answer retained byte-for-byte in JSON |
| Measurements | Prompt/task/source hashes; latency; prompt/completion/total tokens where returned | Missing values remain unknown |
| Uncontrolled | Hardware, model, output/context limits, scheduling, capacity, cache, provider behavior | Confounds; do not infer causality |
| Unverifiable | Model-weight SHA-256, provider hardware, total Root usage, financial cost | Explicitly not measured/verified |

The task instruction asks for JSON under 180 tokens. Runtime engine caps (256 or 512) are separate. Source aggregate hashes and byte counts appear in `source_evidence.json`; cutoff is the Founder-supplied minute 23:08 UTC (18:08 America/Chicago), after an approximate 18:42 UTC start, for 266 nominal minutes. Packaging, inspection, and publication are after cutoff.
