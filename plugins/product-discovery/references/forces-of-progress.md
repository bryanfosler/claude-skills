# Four Forces of Progress (Practitioner Reference)

Bob Moesta's force diagram is the analytic frame for understanding any switch. Load on demand when running switch interviews, doing competitor teardowns through the firing lens, or diagnosing low conversion / churn.

---

## 1. The Equation

Plot two products on a timeline: Product A (old) and Product B (new). Four forces act on the person.

**A switch happens only when F1 + F2 > F3 + F4.**

- **F1 — Push of the Situation:** What is wrong with the current state (NOT the new product). What broke, frayed, or accumulated.
- **F2 — Pull of the New Solution:** Magnetism. What attracts them forward — a promise, a peer story, a vision of better.
- **F3 — Anxiety of the New:** Fear created by the new solution itself. "Will it work? Will my team adopt it? What if I'm wrong?"
- **F4 — Habit of the Present:** Inertia. The pull of what they already do, regardless of whether they like it.

Most teams chase F2 (build more features). Moesta's counter-intuitive move: **reducing F3 and F4 is often more effective than increasing F2.**

---

## 2. Per-Force Examples and Elicitation

### F1 — Push (the Situation)

What changed in their context that made today the day. The push is **upstream of your product entirely** — you cannot create a push through marketing; you can only help someone recognize one they're already experiencing.

> "If there's no push, they can't even see your product because we're creatures of habit."

**Examples:**
- A car starting to make a sound months before the "buying decision"
- A boss telling someone they're not delivering fast enough (social push)
- A spreadsheet that crashed during a meeting (functional push)
- A move, a promotion, a new child, a death — life-stage pushes

**Elicit by asking:**
- "What was the very first moment you thought 'something has to change?'"
- "What was going on in your life at that time?"
- "Walk me back to before you were even looking — what was bothering you?"
- "What happened the day or week before you started searching?"

### F2 — Pull (Magnetism of the New)

The specific promise that pulls them forward. Often a single feature, a peer recommendation, or a vivid story of someone like them succeeding.

**Examples:**
- A friend saying "this changed how I work" (social pull)
- A demo video showing a clean dashboard (functional pull)
- A vision of being the kind of person who has their act together (emotional pull)
- A specific moment of "oh — I didn't know that was possible"

**Elicit by asking:**
- "What did you see that made you think this might work?"
- "Whose recommendation mattered? Why theirs?"
- "What did you imagine your life looking like with this?"
- "What was the moment you decided to try it?"

### F3 — Anxiety (Fear of the New)

The product itself creates F3. Every feature, every onboarding step, every pricing tier raises some anxiety. **More features can increase F3 more than F2** — the question "can it really do all those things?" becomes the dominant signal.

> "More features create actually anxiety, can it do all those things?"

**Examples:**
- "Will my team adopt this?"
- "Will it integrate with what we have?"
- "Will the data be accurate?"
- "What if I lose what I have now?"
- "What if my boss thinks I made the wrong call?" (social anxiety)

**Elicit by asking:**
- "What almost stopped you?"
- "What were you worried about right before signing up?"
- "Who did you check with before deciding? What did you ask them?"
- "What did you do to reduce the risk?"

### F4 — Habit (Inertia of the Present)

The pull of the existing behavior. Even people who hate their current solution have habits, workflows, mental models, and identities built around it. **F4 has nothing to do with whether they like the current solution** — only with the cost of changing.

**Examples:**
- "We've used Jira for six years, our workflows are built around it"
- A spreadsheet so messy nobody else can read it — but the owner knows where everything is
- Identity attachment: "I'm a Things user" / "I'm an Excel person"
- The dining table that has hosted every family holiday for 40 years

**Elicit by asking:**
- "What did you have to stop doing?"
- "What workarounds did you build that you had to give up?"
- "What did you miss about the old way?"
- "What did you have to change about how you think about [this task]?"

---

## 3. The Counter-Intuitive Insight — Friction Beats Features

The condo example: Moesta's company was selling condos to downsizers. People canceled six weeks out because they couldn't figure out what to do with all their stuff. Pure F3/F4 friction.

**Solution:** raise the price and include moving services plus two years of storage.

**Result:** sales increased 30%. The product itself didn't change. The friction did.

The dining table example: Downsizers explicitly said they did not want a dining table. They were not having holidays anymore. But they would not close on the condo until they knew where the table was going. **The table was "the emotional bank account for their entire life"** — family history, holiday meals, social identity.

Moesta built a smaller, symbolic space for the dining table — too small to actually eat at; people used it for puzzles. Sales increased 22%.

**The lesson for the plugin:** when conversion or adoption is weak, do not default to "add features." Instrument the F3/F4 surface first. What anxiety can you remove? What habit are you forcing users to break? Often the cheapest, fastest win is a friction reduction, not a product addition.

---

## 4. Mapping a Force Diagram from an Interview

For each switch interview, produce this artifact:

```
PUSH (what was wrong with the current situation):
- [specific events, dates, social pressure, accumulated frustration]

PULL (what attracted them to the new solution):
- [specific features, peer stories, vision of outcome]

ANXIETY (what worried them about the new solution):
- [specific fears, what almost stopped them, who they checked with]

HABIT (what they had to give up or break):
- [workarounds, identity, integrations, mental models]

HIRE CRITERIA (what the new solution had to do):
FIRE CRITERIA (what they stopped using / giving up):

ENERGIES PRESENT:
- Functional: [time / effort / speed / knowledge]
- Emotional: [feelings / fears / desires]
- Social: [perception / identity / status]
```

After 8-12 interviews, cluster by recurring force combinations (push + pull + anxiety + habit patterns that repeat). Each cluster is a job. Most products have 3-5 clusters, often in conflict.

---

## 5. Using Forces in Competitor Teardowns

The four forces map directly to strategic surfaces:

- **F1 is your marketing.** What pushes do you amplify and validate?
- **F2 is your positioning.** What promise pulls them toward you specifically?
- **F3 is your onboarding and risk reversal.** Where can you remove anxiety?
- **F4 is your competitor's moat.** Switching cost they've built. Hardest to attack.

Linear vs. Jira teardown through the forces:
- **F1:** "Jira is slow, complicated, and built for project managers, not engineers"
- **F2:** "fast, beautiful, opinionated UX that respects engineering workflow"
- **F3:** "will Linear have the reporting my manager needs?" → answered with Cycles and Roadmaps
- **F4:** "we've been on Jira for six years, migration is a project" → answered with migration tooling

Every GTM move Linear made can be read as a response to one of these forces.

---

## 6. Quick Diagnostic — Why Aren't They Switching?

When a prospect won't convert, ask which force dominates:

| Symptom | Likely Force | Move |
|---------|-------------|------|
| "I'm fine with what I have" | Low F1 | You can't build a push. Find prospects whose context has changed. |
| "I'm not sure I get it" | Low F2 | Sharpen the promise. Show one vivid use case, not a feature list. |
| "I need to think about it" | High F3 | Identify the specific anxiety. Risk reversal: trial, money-back, white-glove onboarding. |
| "We're too busy to switch right now" | High F4 | Reduce migration friction. Bundle services. Make the first step trivial. |

---

## Sources

- Bob Moesta on Lenny's Podcast (2023-08-24) — primary
- *Demand-Side Sales 101*, Moesta
- [Bob Moesta on JTBD — Intercom Podcast](https://www.intercom.com/blog/podcasts/podcast-bob-moesta-on-jobs-to-be-done/)
- [Unpacking the Progress-Making Forces Diagram — jobstobedone.org](https://jobstobedone.org/radio/unpacking-the-progress-making-forces-diagram/)
