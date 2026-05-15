# AI-Era Discipline (Practitioner Reference)

What the plugin SHOULD do with AI, what it MUST NEVER do, and the genuinely novel patterns the AI era unlocks. Load on demand when the plugin is doing synthesis, friction mining at scale, competitor research, or anything that involves LLMs touching user data.

---

## 1. The Landscape in Two Sentences

Building has gotten dramatically cheaper. Discovery hasn't gotten easier — it's gotten noisier. Teresa Torres (2024-2025): **"Building is very cheap now. That doesn't mean we should build every idea we have."**

The bottleneck has moved into discovery and validation. Getting it right matters more than ever. The temptation to shortcut it has never been stronger.

---

## 2. What the Plugin SHOULD Do

### Verbatim-Quote-Anchored Insights

Every theme surfaced from review mining, interview synthesis, or competitor analysis must link to **2-5 verbatim source quotes with URLs**. No theme exists without proof.

This is the rule that separates real insight from AI-generated plausibility theater. The quote is the evidence. The theme is a hypothesis about what the evidence means. An LLM can write a confident summary of 12 weak reviews that looks identical to a confident summary of 500 rich reviews. The summary format itself signals authority it may not have earned.

**UX pattern:** every insight card shows synthesis at top, verbatim quotes in an expandable section below, source URL/document reference alongside each quote.

### Volume-Declared Confidence

"Based on 12 reviews" and "based on 847 reviews" should look different in the UI. Confidence is a function of evidence mass.

- Directional hypotheses from thin data (< 30 sources): tag explicitly
- Validated patterns from strong data (100+ sources): can be presented with higher confidence
- Confidence signals must be honest, not performative

### Dual-Pass Synthesis (Torres's Workflow)

> "Lazy AI synthesis — reading AI summaries without doing your own synthesis first — is the most dangerous pattern I observe in practitioners." — Teresa Torres

Torres's documented workflow: **do your own synthesis first, then run AI synthesis, then compare.** Every time she does this, she finds things the AI missed, and the AI finds things she missed.

The plugin should support this two-step explicitly:
1. User produces their own first-pass synthesis
2. Plugin produces AI synthesis
3. Plugin shows the diff — what each found that the other missed

Torres estimates that dump-transcript-into-AI workflows capture roughly **5% of actual conversation value**. The mechanical synthesis misses what the participant was working around, avoided saying, or revealed in their phrasing choices.

### Scale-Based Friction Mining

Running 500-1000 App Store, G2, or Trustpilot reviews through an LLM to surface recurring themes is one of the most legitimately useful AI applications in discovery. At that scale, manual analysis is impractical; AI clustering is genuinely better than the alternative (not doing it).

Apple's own ML research pipeline (published) is the model:
- Filter for spam/profanity
- Extract insights via fine-tuned LLMs
- Dynamic topic modeling
- Select **representative** insights (not just topic labels) — this preserves verbatim texture
- Generate short summaries

The plugin should do this with strict source-attribution requirements. See Section 4 for bias risks.

### Perplexity-Style Sourcing for Competitor Research

Perplexity Pro is the strongest general tool for competitive landscape scanning because it retrieves live public data with citations. The hallucination risk is lower than purely parametric models — you can verify claims immediately.

The plugin should model this: every competitor claim gets a source link. Pricing, features, customer logos, packaging details — all must be sourced.

### Cross-Session Theme Clustering

Across a series of discovery interviews, AI can detect patterns that aren't obvious when reading one interview at a time. AI sees the corpus; humans see individual sessions. The combination is stronger than either alone.

### Draft Outcome Statements

Seeding an LLM with interview transcripts and asking it to generate candidate outcome statements (in the Torres/JTBD style, or Ulwick's "Minimize + time/likelihood" syntax) produces a useful first draft. LLMs generate more candidates than a human typically would in one sitting, which is valuable for coverage.

The human still validates, edits, and reframes. The LLM does volume; the human does judgment.

---

## 3. What the Plugin MUST NEVER Do

### Never: Synthetic Users as Validation

Synthetic users (AI-generated personas / simulated respondents) cannot substitute for real research. **This is Bryan's hard rule.** Evidence base:

- **NN/g (2024):** synthetic users say yes to nearly everything (sycophancy), generate lists of needs without prioritization ability, dramatically overstate enthusiasm. Testing hypothetical drone delivery, synthetic users responded enthusiastically — not because drones are appealing, but because the AI is trained to please.
- **Columbia (2024):** small variations in persona description produce dramatically divergent responses. Fully LLM-generated personas predicted Democratic victories in all 50 states in a US election simulation. Training-data bias surfaces as false signal.
- **Hu and Collier (2024):** "LLM-generated personas exhibited increasingly positive sentiment and higher subjectivity as more details were added, often portraying idealised individuals with strong community values and minimal life challenges." Not the contradictory, time-constrained, confused humans who actually use products.
- **ACM Interactions (2025-2026):** "Synthetic Persona Fallacy" — the risk that AI-generated research gives organizations the psychological comfort of having done research without providing the actual signal.

**Safe synthetic uses:**
- Hypothesis generation before real research (generate questions, not answers)
- Stress-testing feature ideas against a range of synthetic types to find load-bearing assumptions
- UI/UX automated testing flows (AI agents acting as users for functional testing, not insight generation)

**Unsafe synthetic uses:**
- Treating synthetic responses as validation for a product decision
- Niche populations (elderly, non-English speakers, specific occupational roles) — training-data gaps create actively misleading profiles
- Presenting synthetic findings to stakeholders without disclosing their nature

**The plugin must never describe synthetic outputs as "user research" or "user insights."** They are hypothesis inputs.

### Never: Unverified Competitor Specifics

AI competitive analysis works well for high-level frameworks. It fails badly for specifics — pricing tiers, customer logos, packaging details, feature capabilities. These specifics "can sound convincing but could be completely fabricated" (Klue, 2024-2025).

The plugin must require source links for:
- Pricing claims
- Specific product capabilities
- Customer logos or testimonials referenced
- Funding details, revenue, headcount
- Roadmap or feature timing

If a source can't be found, the plugin must label the claim as **unverified hypothesis**, not analysis.

### Never: Theme-Only Outputs Without Quotes

A list of "top pain points" without the quotes that justify each item is not insight. It is plausibility theater. Every theme requires evidence. See Section 2 (Verbatim-Quote-Anchored Insights).

### Never: Full-Pipeline AI PRDs

AI-generated PRDs fail not because the AI produces poor prose — it doesn't — but because the judgment calls embedded in a good PRD (which edge cases matter, what tradeoffs are acceptable, what the team needs to hear vs. what stakeholders need to hear) require contextual product sense that AI doesn't have.

AI can draft the structure and fill in known constraints. It cannot make the strategic choices that give a PRD its value.

Gartner predicted (2024) that 30% of generative AI projects would be abandoned after PoC by end of 2025, citing "poor data quality, inadequate risk controls, escalating costs or unclear business value." Full-pipeline AI PRDs are the cohort that gets abandoned.

### Never: Synthetic A/B Tests

AI-generated responses cannot simulate actual user behavior in a real product context. Behavioral data requires behavioral reality. Synthetic "would you prefer A or B" responses produce the same sycophancy problem as synthetic personas.

---

## 4. Bias Risks in Review Summarization

Even legitimate scale-based friction mining carries documented biases:

- **Recency skew:** reviews spike after updates and feature requests. Summary run after a controversial update over-represents that cohort.
- **Class imbalance:** negative reviews are longer and more detailed. LLMs over-weight negative sentiment. Positives tend to be shorter and under-represented.
- **Selection bias:** review-writers are not representative users. They skew toward frustrated users seeking resolution outlet, and power users with strong opinions. The silent majority — who feel nothing strongly — never appear.
- **Accuracy variation:** research on LLM sentiment analysis shows up to 10% accuracy fluctuation across identical repeated inference runs, even with deterministic settings. Individual sentiment labels should not be treated as reliable.

The plugin should surface these biases explicitly when presenting results, not bury them in fine print.

---

## 5. Tooling and Privacy

When sending user data to LLMs, check data policies:
- Some tools (notably ChatGPT directly) use uploaded data for model training
- Matters for participant confidentiality, NDA-covered research, IRB compliance

If the plugin is processing interview transcripts or user-identifiable feedback, default to:
1. Local processing where possible
2. API endpoints with explicit no-training data policies
3. Anonymization before upload (strip names, employers, identifying specifics)

---

## 6. Source Provenance — The VeriTrail Pattern

Microsoft Research's VeriTrail system (2025-2026) addresses the honesty problem in multi-step AI workflows by tracing the provenance of every output claim back through intermediate steps to source text.

The concept applies directly to PM tooling: **every insight needs a traceable path to its source material.**

Practical implementation requirements:
- Every surfaced insight displays the source link and verbatim evidence supporting it
- Theme labels never appear without supporting quotes
- Volume of sources displayed alongside summaries ("based on 847 reviews" vs. "based on 12 reviews")
- Confidence signals are honest: directional hypotheses from thin data, validated patterns from strong data
- The plugin makes it easy for the PM to click through to primary sources — not just accept the summary

---

## 7. The Novel Idea — Continuous Competitive Drift Detection

A pattern the AI era genuinely unlocks (not widely implemented in 2025-2026 tooling):

**Monthly automated scans of competitor public surface area** (pricing pages, homepage copy, product changelogs, job postings, G2 review velocity) with LLM-based change detection.

- New job posts mentioning a specific skill set → strategic direction signal
- Pricing page changes → margin pressure or repositioning
- Homepage copy shifts → target persona shift or positioning move
- Review velocity spike (positive or negative) → product event, market reception
- Feature changelog acceleration → competitive response cycle

The output is not a competitive analysis report — it's a **delta digest**: "since last month, Linear changed X, Y, Z. Notion's pricing page now emphasizes [phrase]. Three new G2 reviews mention [pattern]."

This is genuinely new because:
1. Manual monitoring at this cadence is prohibitive for small teams
2. AI clustering of changes is faster and more comprehensive than human watching
3. Continuous baseline allows surfacing **drift** (rate of change) not just snapshots
4. Perplexity-style sourcing makes every flagged change traceable

Existing tools (Crayon, Klue) do version of this for enterprise sales teams at $20-40K/year. The plugin can do a lighter version at zero marginal cost for the user.

---

## 8. The AI-Assisted PM Workflow (2024-2025 Pattern)

Observed across high-performing product organizations (Linear, Notion, Vercel):

| Activity | Mode |
|----------|------|
| Weekly user touchpoints | **Stay human.** Short unmoderated interviews, recorded and transcribed. Primary evidence source. |
| Synthesis | **AI-augmented.** Transcripts go through Dovetail / Looppanel / Claude for first-pass theme extraction. Human researcher reviews and amends. |
| Competitor monitoring | **Continuous.** Perplexity-style daily/weekly scanning of competitor public activity. |
| Prototyping | **Earlier and cheaper.** Vibe-coded prototypes (Cursor, Lovable, v0) go into concept testing within days of idea generation. Biggest behavioral change in discovery workflows. |
| PRDs and specs | **Drafted with AI, written by humans.** AI generates first pass; PM rewrites substantially. Judgment calls stay human. |

The plugin should fit this pattern, not try to replace it.

---

## 9. Plugin Design Principles (Summary)

1. **Traceability is mandatory.** Every insight links to source. No theme without quotes. No quotes without provenance.
2. **Synthesis is layered, not final.** AI produces hypothesis candidates; humans evaluate them. Make the two-step visible.
3. **Volume declared, not hidden.** Confidence is a function of evidence mass.
4. **Real user data is primary.** Synthetic inputs are scaffolding for research design, never substitute for actual signal.
5. **Competitor claims need sources.** AI-generated competitor analysis without source URLs is competitive fiction.
6. **Discovery acceleration, not replacement.** The plugin's value prop is making it faster and easier to do real discovery — not to simulate having done it.

---

## Sources

- [NN/g — Synthetic Users](https://www.nngroup.com/articles/synthetic-users/)
- [Teresa Torres — airfocus interview (AI for PM)](https://airfocus.com/blog/teresa-torres-ai-product-management/)
- [Looppanel — AI Interview Analysis](https://www.looppanel.com/blog/ai-interview-analysis)
- [State of Synthetic Research 2025 — Conversion Alchemy](https://christophersilvestri.com/research-reports/state-of-synthetic-research-in-2025/)
- [Klue — Competitive analysis with AI](https://klue.com/blog/how-to-do-competitive-analysis-with-ai)
- [Apple ML Research — App Store Review Summarization](https://machinelearning.apple.com/research/app-store-review)
- [SVPG — AI Product Management 2 Years In](https://www.svpg.com/ai-product-management-2-years-in/)
- [Reforge — AI Native Product Teams](https://www.reforge.com/blog/ai-native-product-teams)
- [ACM Interactions — Synthetic Persona Fallacy](https://interactions.acm.org/blog/view/the-synthetic-persona-fallacy-how-ai-generated-research-undermines-ux-research)
- [Gartner — 30% of GenAI projects abandoned](https://www.gartner.com/en/newsroom/press-releases/2024-07-29-gartner-predicts-30-percent-of-generative-ai-projects-will-be-abandoned-after-proof-of-concept-by-end-of-2025)
- [Microsoft Research — VeriTrail](https://www.microsoft.com/en-us/research/blog/veritrail-detecting-hallucination-and-tracing-provenance-in-multi-step-ai-workflows/)
- [Lenny — How AI Will Impact PM](https://www.lennysnewsletter.com/p/how-ai-will-impact-product-management)
