---
name: self-improving-loop
description: >
  Run a task as an autonomous self-checking loop that improves its own approach each pass
  until it clears a goal or exhausts a loop budget. Use for tasks Claude does not one-shot
  well — where the first output is mediocre but a defined quality signal can tell good from
  bad, and each iteration can learn from the last failure and amend the prompt/approach.
  Triggers: "loop on this until it's good", "keep improving until it hits X", "self-improving
  loop", "run it N times and keep the best", "iterate to a goal", "learning loop", or /refine-loop.
---

# Self-Improving Loop

Run a task as a closed loop: **produce → score → diagnose → amend → repeat**, stopping when output clears a goal or a loop budget runs out. The thing that improves across passes is the *approach itself* (the prompt, the plan, the parameters), informed by the previous pass's specific failure. The durable output is both the best result **and** the converged approach that produced it.

This is the keep-or-discard discipline of an overnight research loop (Karpathy's autoresearch: mutate the code, keep changes that lower the metric), applied to knowledge work: mutate the prompt/approach, keep changes that raise a quality score.

## When to use

Use this when **all three** hold:
- Claude does not reliably one-shot the task (first output is mediocre or inconsistent)
- A **quality signal exists or can be defined** — a rubric, an assertion, a passing test, or a verifier-agent that scores an output good vs. bad
- Each failure teaches something the *next* prompt can encode (so passes genuinely improve, not just re-roll)

Do **not** use this when:
- The task one-shots fine — just do it
- No checkable signal exists and quality is pure taste with no rubric — looping only burns tokens; sit with the human instead
- The problem is *continuity across sessions*, not *quality within a task* — that's `long-running-agent-harness`, a different skill (see below)

### Not the same as the harness

| | `long-running-agent-harness` | `self-improving-loop` (this) |
|---|---|---|
| Loop type | self-**continuing** | self-**improving** |
| Improves each pass | nothing (fixed roadmap) | the prompt/approach |
| What persists | progress log + feature ledger | the converged prompt + best output |
| Stops when | all features pass | goal cleared, or budget exhausted |
| Fights | drift, redo, false "done" | one-shot mediocrity |

## The hard gate: define the goal signal first

**No checker, no loop.** A self-checking loop with a vague checker just repeats randomly. Before any iteration, pin down exactly one of these and write it down:

- **Rubric** — 3–7 weighted criteria, each scorable 0–N, with an explicit pass threshold (e.g. "≥ 90% of max, and no criterion below 60%"). Best for prose, designs, plans, copy.
- **Assertion / test** — a deterministic check that passes or fails (compiles, all tests green, output matches schema, number reconciles). Best for code, data, structured output.
- **Verifier-agent** — a separate agent prompted to *adversarially* judge the output against the rubric and return a score + the single most important gap. Use when scoring needs judgment but you still want autonomy.

The goal signal must return **two things every pass**: a *score* (to compare passes and gate stop) and a *diagnosis* (the specific top failure, so the next pass can target it). A score with no diagnosis cannot drive improvement.

## The loop

```
0. Define the goal signal (rubric / assertion / verifier) + stop conditions.   ← gate
1. Produce an output with the current approach.
2. Score it against the goal signal. Capture score + top-1 diagnosis.
3. KEEP-OR-DISCARD: if this pass beat the best-so-far, adopt it as the new
   baseline; if it regressed, discard and revert to the prior approach.
4. STOP? if score ≥ goal, or passes ≥ budget, or K passes with no gain → exit.
5. AMEND: rewrite the approach to target the diagnosis from step 2
   (add a constraint, fix the failing dimension, change a parameter).
6. Go to 1.
Exit: return the best output AND the converged approach. Log the score trail.
```

Three rules that make it actually converge:

- **Target the diagnosis, don't re-roll.** Each amendment must address the *specific* gap the checker named. "Try again" is not an amendment; "the prior pass missed the EU channel split — add it to the prompt" is.
- **Keep-or-discard against best-so-far, not against the last pass.** Otherwise a single bad mutation drags the baseline down and the loop oscillates. (This is the autoresearch discipline — only keep changes that moved the metric the right way.)
- **Stop on no-gain, not just on budget.** Track consecutive passes with no improvement; bail after K (default 2). A loop that's plateaued is done whether or not the bar was hit — report the best result and the plateau honestly.

## Execution modes

### Autonomous (default) — Workflow-orchestrated

Use the Workflow tool so the loop runs in the background with deterministic control flow and a code-enforced keep-or-discard gate. This is the walk-away mode: "run until it hits the bar or 8 passes."

Template:

```js
export const meta = {
  name: 'self-improving-loop',
  description: 'Iterate a task to a goal: produce, score, diagnose, amend, keep-or-discard',
  phases: [{ title: 'Iterate' }],
}

// --- configure per task ---
const GOAL = args?.goal ?? 90          // pass threshold on the rubric
const BUDGET = args?.budget ?? 8       // max passes
const NO_GAIN_LIMIT = 2                // stop after this many passes without improvement
const TASK = args.task                 // what to produce
const RUBRIC = args.rubric             // the scoring criteria text

const SCORE_SCHEMA = {
  type: 'object',
  required: ['score', 'topGap', 'rationale'],
  properties: {
    score: { type: 'number' },                         // 0..100 against the rubric
    topGap: { type: 'string' },                         // the single most important failure
    rationale: { type: 'string' },
  },
}

let approach = `Produce the following.\n\nTASK:\n${TASK}`
let best = { score: -1, output: null, approach: null }
let noGain = 0

for (let pass = 1; pass <= BUDGET; pass++) {
  const output = await agent(approach, { label: `produce#${pass}`, phase: 'Iterate' })

  const verdict = await agent(
    `Adversarially score this output against the rubric. Be a harsh grader; default low when unsure.\n\n` +
    `RUBRIC:\n${RUBRIC}\n\nOUTPUT:\n${output}`,
    { label: `score#${pass}`, phase: 'Iterate', schema: SCORE_SCHEMA }
  )
  log(`pass ${pass}: score ${verdict.score} — gap: ${verdict.topGap}`)

  // keep-or-discard against best-so-far
  if (verdict.score > best.score) {
    best = { score: verdict.score, output, approach }
    noGain = 0
  } else {
    noGain++
  }

  if (verdict.score >= GOAL) { log(`goal ${GOAL} cleared at pass ${pass}`); break }
  if (noGain >= NO_GAIN_LIMIT) { log(`plateaued after ${noGain} passes without gain`); break }

  // amend the approach to target the diagnosis — build off the BEST approach, not the last
  approach = `${best.approach}\n\n` +
    `The previous best attempt scored ${best.score}/100. Its single biggest weakness was:\n` +
    `"${verdict.topGap}"\n` +
    `Produce a new version that specifically fixes that weakness while preserving everything that already worked.`
}

return { bestScore: best.score, bestOutput: best.output, convergedApproach: best.approach }
```

Invoke with `args: { task, rubric, goal, budget }`. Read the result, then hand the user the best output **and** the converged approach (the reusable prompt is half the value).

Notes:
- Producer and scorer are **separate agents** — never let the agent that wrote the output grade its own work; that's how scores inflate.
- For taste-heavy work, run a small **panel** (3 scorers, take the median) instead of one, to damp scorer noise.
- For wide solution spaces, fan out *several* approaches per pass with `parallel()` and keep the best — a tournament, not a single chain.
- Workflow agents reach MCP/file tools via ToolSearch, so the loop can pull Dovetail, M365, vault files, etc. inside a producer step.

### Inline — one pass at a time

When you want to stay in the seat (subjective output, or you're not sure the rubric is right yet): run one pass, show the user the score + diagnosis + the proposed amendment, and continue on their nod. Cheap, interactive, and lets the rubric itself get corrected mid-loop. This is how the pattern has been run ad hoc — the skill just makes the checker and keep-or-discard explicit.

## Cost vs output — don't mindlessly burn tokens

Loop cost ≈ (agents per pass) × (passes) × (tokens per agent). This adds up fast — especially via the Workflow tool, whose "dynamic workflow" permission prompt is warning about exactly this: it can fan out many subagents. Right-size before running.

Cost levers, biggest first:
- **Checker type.** A deterministic checker (assertion/code) is **free** — no scorer agent at all. An LLM verifier costs one agent call per pass; a 3-judge panel triples that. Use code when the score is computable; use a single judge by default; reserve a panel for genuinely subjective/taste work where judge variance is real.
- **Passes** (budget × no-gain). Each pass is a full producer (+ scorer) round. Keep budget 5–8 and no-gain 2; don't inflate "just in case."
- **Context re-reading.** If every agent re-opens large files, cost compounds. Pass the relevant excerpt once in the prompt instead.
- **Model tier.** Use a cheaper model (Sonnet/Haiku) for mechanical produce/score; reserve the top tier for the hardest judging.
- **Fan-out width.** Tournament / parallel-variants multiply per-pass cost — only when the solution space is genuinely wide.

Two worked examples from this skill's first runs (same 5-pass budget):
- **Deterministic checker** (tier-pricing loop): only producer agents cost tokens → ~5 agents, ~140K tokens.
- **3-judge panel** (dashboard IA loop): 5 passes × (1 producer + 3 judges) = 20 agents, ~615K tokens — ~4× the cost for the same passes, almost entirely the panel. A single judge would have roughly halved it.

To run the **same** loop cheaper:
1. **Inline mode** — run the loop in the main conversation, no Workflow tool. No subagent fan-out, no dynamic-workflow prompt, and you see each pass so you can stop early. Cheapest; best when you're present.
2. **Deterministic or single-judge checker** instead of a panel.
3. **Lower budget**, tighter no-gain limit.
4. **Cheaper model** for produce/score.

Rule of thumb: reach for the Workflow tool (autonomous fan-out) only when you'll genuinely walk away **and** the loop needs many passes or parallel variants. For a handful of passes while you're watching, inline is cheaper and just as good.

## Stop conditions

Always set all three before starting:
- **Goal** — the score threshold that means "done" (and any per-criterion floor).
- **Budget** — max passes (default 6–8). A hard ceiling so it can't run away.
- **No-gain limit** — consecutive passes without improvement before bailing (default 2).

Report which condition fired. "Plateaued at 84/90 after pass 5" is a real, useful result — not a failure to hide.

## Capture the converged approach

The reusable artifact is **the prompt/approach that finally worked**, not just the one good output. At the end:
- Return the best output for immediate use.
- Return the converged prompt so it can be reused, saved as a snippet, or promoted into a skill/command if the task recurs.
- Keep the score trail (pass → score → gap) so the user can see *how* it converged and trust the result.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Loop runs but output doesn't improve | Vague checker, or amendments re-roll instead of targeting the gap | Tighten the rubric; require each amendment to name the gap it fixes |
| Score oscillates up and down | Keeping against last pass, not best-so-far | Keep-or-discard against best; revert regressions |
| Score inflates, output still weak | Producer is grading itself | Use a separate scorer agent; make it adversarial |
| Never terminates / burns tokens | No no-gain limit, budget too high | Set no-gain limit (2) and a hard budget; stop on plateau |
| Hits the bar but result is off-target | Rubric measured the wrong thing | Fix the rubric, not the loop — run inline until the rubric is right |
| Subjective quality, scorer noisy | Single judge on a taste task | Panel of 3 scorers, take the median |

## Quick reference

Before looping:
- Define the goal signal (rubric / assertion / verifier) — **no checker, no loop**
- Set goal threshold, budget, and no-gain limit

Each pass:
- Produce with the current approach
- Score with a *separate* checker → score + top-1 gap
- Keep-or-discard against best-so-far
- Stop if goal cleared / budget hit / plateaued
- Amend to target the named gap; build off the best approach

After:
- Return best output **and** converged approach
- Report which stop condition fired + the score trail

Hard rules:
- The checker is separate from the producer
- Amend to the diagnosis; never just "try again"
- Keep against best-so-far; revert regressions
- Always have a budget and a no-gain limit

## References

- Karpathy, autoresearch (keep-or-discard experiment loop): https://github.com/karpathy/autoresearch
- Sibling skill: `long-running-agent-harness` (self-continuing, multi-session continuity)
