# Competitor Teardown — Elite Methodology (Practitioner Reference)

The seven moves that separate a real strategic teardown from a feature comparison table. Load on demand when running competitor analysis for positioning, market entry, or strategy work.

---

## 1. The Goal — Reconstruct the Theory of Mind

The failure mode of generic competitor analysis: treating it as a feature audit. Comparison table. SWOT grid. Tells you nothing useful.

A real teardown has one goal: **reconstruct the competitor's theory of mind.** What job do they believe they are serving? Who do they believe the protagonist is? What do they believe is the incumbent way that job is being done badly? What are they *not* trying to do?

The output is a **one-page thesis** (Section 9), not a comparison table.

April Dunford in *Obviously Awesome*: positioning always implies a competitive alternative, whether stated or not. When Stripe positioned against "payments are hard for developers" rather than "PayPal," they made a category claim — asserting they were inventing a new market, not improving the old one. That framing told you everything.

Geoffrey Moore (*Crossing the Chasm*): every entrant implicitly names two things — a **market alternative** (what the customer would do if you didn't exist) and a **product alternative** (a direct competitor). The gap between them is where the value proposition lives.

---

## 2. Move 1: Four Fits Analysis (Balfour / Reforge)

A competitor is a **system**, not a product. Four fits must be coherent or the system stresses:

| Fit | Question |
|-----|----------|
| **Market-Product** | What specific pain, in which specific segment? (Linear: "engineering teams who find Jira painful" — not "teams that do PM") |
| **Product-Channel** | What channel does the product's architecture assume? (Linear's fast desktop app encodes word-of-mouth among engineers. Jira's deep IT integrations encode top-down procurement.) |
| **Channel-Model** | Does the pricing structure align with how adoption actually spreads? (Linear's per-seat aligns with viral team growth. Flat-fee would undermine it.) |
| **Model-Market** | Does the revenue model scale within the addressable market? |

**Strategic move:** when a competitor's fits are misaligned, they are vulnerable. Jira's enterprise-IT channel (slow, top-down) was misaligned with the Product-Channel reality that engineers make daily tool choices by trying things. Linear exploited the misalignment.

---

## 3. Move 2: Interview the Firers (JTBD Switch Lens)

> Don't ask "why do you like this product?" — ask "walk me through the day you decided to switch away from the old thing."

This is the Moesta switch-interview methodology (see `switch-interview-guide.md`) turned outward. The output is a **firing profile** — the conditions under which users decide the competitor has failed them. More valuable than the hiring profile because it reveals the competitor's ceiling.

The four forces become four strategic surfaces:

- **F1 (Push)** = your marketing. The competitor's failure mode.
- **F2 (Pull)** = the job your product must credibly claim to do better.
- **F3 (Anxiety)** = your positioning challenge.
- **F4 (Habit)** = the competitor's moat. Their structural advantage.

**Practical method:** 8-12 recent switchers from the target competitor. Ask only about the switching story. Listen for emotional inflection — anger, resignation, relief — as signals of where frustration peaked. Code against the four forces. Patterns are your strategic input.

---

## 4. Move 3: Review Mining — JTBD-Coded, Not Skimmed

App store, G2, Reddit, Trustpilot reviews are **primary research material**, not anecdotal noise. Method is thematic coding.

For each review, assign codes:
- **Functional job:** What task are they trying to complete?
- **Emotional job:** How do they want to feel?
- **Social job:** How do they want to be perceived?
- **Switch trigger:** What frustrated them enough to look?
- **Anchor phrase:** Verbatim language (this becomes copy input)

After coding 40-60 reviews, look for frequency patterns.

**Review patterns that reveal positioning gaps:**

| Pattern | Interpretation |
|---------|---------------|
| High satisfaction with *features*, low satisfaction with *outcomes* | Competitor built tools but didn't solve the job. Users are proficient but not successful. |
| Churned users who still love the product | Problem isn't the product — it's solving the wrong job for them. Market fit broke. |
| Frustrated users who haven't switched | High F4 (switching anxiety). Lock-in, not loyalty. Brittle moat. |
| Reviews compare to a surprising alternative | Real competitive landscape revealed. If Notion reviews compare to Excel, the real alternative is spreadsheets. |

Every theme surfaced must link to 2-5 verbatim quotes. No quotes = no theme. See `friction-mining-sources.md` for source map and `ai-era-discipline.md` for the verbatim-quote rule.

---

## 5. Move 4: Onboarding Teardown — The First 10 Minutes

A competitor's onboarding is the most compressed strategic artifact you can analyze. It encodes:

1. **Who they think the user is.** First question asked (or skipped) reveals their persona assumption. Notion: "what's your team type?" Linear: create a project. Superhuman: 1:1 human call. Different theories of user.
2. **What they believe the first value moment is.** Shortest path to perceived value encodes JTBD hypothesis. Path ends at first task = task capture job. Path ends at invited teammate = collaboration job.
3. **What they sacrifice for activation.** Friction is a choice. Required integrations before use = belief that value is impossible without ecosystem. Dummy data = belief first-use delight matters more than real-world relevance.
4. **Their trust level with new users.** Email-only vs. credit card vs. detailed persona quiz reveals assumed commitment and sales motion (PLG vs. enterprise).

**Capture in the teardown:**
- Time to first value moment (TTFV) in seconds
- Number of decisions required before first meaningful action
- Data collected and why
- Copy framing at each step (outcome language vs. feature language)
- What they do **not** show in the first session
- **The first email after signup** (highest signal — reveals what they believe the user's main risk is: not understanding [tutorial], not coming back [engagement hook], not inviting team [virality], not converting [sales trigger])

---

## 6. Move 5: Pricing Teardown — Reading the Pricing Page as Strategy

A pricing page encodes more strategic intent than any press release.

**Plan count and naming:**
- 2 plans = PLG, conversion through use, not sales
- 3 plans = classic value ladder
- 4+ plans = market segmentation complexity, possibly lost coherence
- Generic names ("Starter/Pro/Business") = no differentiation. Functional names ("Free/Plus/Business") signal tier intent.

**Feature gating choices:** what they place in higher tiers reveals what they believe constitutes premium value. SSO + admin in enterprise tier = security as enterprise-sale driver. Analytics in premium = they believe data is the value-add. Features migrating down between tiers = commoditization.

**Price point anchoring:** $9/$29/$99 = incremental upgrades. $15/$150 binary = individual-vs-team buyer. Per-seat aligns with bottom-up viral. Usage-based aligns with infrastructure positioning. Flat-rate aligns with simplicity-as-value.

**Conspicuous absences:**
- No free tier in PLG market = they concluded free doesn't convert
- No annual discount = they don't need cash or don't trust retention
- "Contact Sales" on all plans = pricing page is theater

**Linear example:** Business tier at $16/seat/month sits above Jira Premium ($14.54) and Shortcut ($12). Deliberate signal: not competing on price. AI agents on Free tier signals competitive pre-emption against Copilot. Buying top-of-funnel in a space they bet will matter in 18 months.

---

## 7. Move 6: Network Effects and Defensibility (a16z)

For platform/marketplace competitors. Three questions:

1. **Is the inventory differentiated or commoditized?** Airbnb (differentiated, strong NE) vs. Uber drivers (commoditized, fragile NE — whoever has liquidity wins).
2. **Does value grow with scale, or plateau?** Once 5-minute rideshare is achieved, more drivers add no user value. Network effect has exhausted itself. Defending a dried-up moat.
3. **What is the multi-tenanting pressure?** If users can run both platforms simultaneously at zero cost (Doordash + Uber Eats), NEs are weakened. Costly switching/exclusivity (Airbnb calendar) = real moat.

Andrew Chen's atomic network concept: every network has a minimum viable community size. Slack's atomic network is the team channel, not the company — that's why a department can adopt Slack even if the company uses Teams. **Identify the level at which the competitor's value is created. That's the level at which they can be disrupted.**

---

## 8. Move 7: Wardley Evolution Mapping

Wardley Maps plot value-chain components against an evolution axis: **Genesis → Custom → Product → Commodity.**

Three things this reveals:

- **Where competitors are overinvested.** Custom infrastructure for things that are rapidly commoditizing (auth, payments, search) = burning resources defending a hill that's about to become a plain. Stripe won partly because competitors treated commodity payments as differentiated.
- **Where the next disruption will come from.** Components moving Product → Commodity are ripe for abstraction. When a competitor's "secret sauce" becomes an API, the moat disappears.
- **Which strategic plays are available.** Standard plays: **commoditize a competitor's value proposition** (force their differentiator to become table stakes), **block and tackle** (prevent access to a component they need), **ecosystem** (make them a component in your value chain).

---

## 9. Output Format — The One-Page Thesis

A teardown should produce a single artifact, readable in 3 minutes, that drives decisions. Not a feature table. Not SWOT.

```
COMPETITOR: [Name]

THEIR THEORY: They believe the job is [X], being done badly in [current way],
for [specific persona].

THEIR WEDGE: They entered by doing [specific thing] dramatically better than
[the incumbent or status quo]. Their beachhead was [segment].

THEIR FOUR FITS:
- Market: [who, specifically]
- Product: [what they've built and what it implies]
- Channel: [how it actually spreads]
- Model: [how they charge and what that signals]

THEIR STRENGTHS (and why they're real):
- [strength 1] because [structural reason]
- [strength 2] because [structural reason]

WHERE THEY'RE VULNERABLE:
- [weakness 1] — evidence: [review pattern / pricing signal / onboarding gap]
- [weakness 2] — evidence: [specific observation]

WHAT JOB THEY'RE UNDERSERVING:
[The outcome segment they claim to serve but don't actually complete well]

OUR OPENING:
[One sentence: the specific job, for the specific segment, that they are not
serving well and we could serve better — and why we're positioned to do it]
```

### Linear Teardown — Worked Example

> **COMPETITOR:** Linear
>
> **THEIR THEORY:** They believe the job is "keeping engineering teams aligned and shipping without friction," being done badly by Jira's admin-first complexity, for software engineers at high-growth startups and scale-ups.
>
> **THEIR WEDGE:** Entered by delivering an order of magnitude faster UI (50-100ms vs. Jira's 200-500ms) and an opinionated workflow that required no configuration to feel useful. Beachhead: 5-50 person engineering teams at VC-backed startups.
>
> **THEIR FOUR FITS:** Market = engineering-led product companies. Product = local-first, keyboard-driven, opinionated. Channel = word-of-mouth among engineers, engineer-first PLG. Model = per-seat, growing as headcount grows.
>
> **WHERE THEY'RE VULNERABLE:** Engineering teams that report to non-technical stakeholders (product, business owners) who need Gantt-style visibility. Linear has no answer for the "my VP wants a roadmap view" problem.
>
> **OUR OPENING:** The team that has adopted Linear for engineering but still uses Confluence + Notion + Google Sheets for planning, roadmapping, and stakeholder communication — three tools where Linear intentionally doesn't compete. That coordination layer is completely unserved.

---

## 10. Three Case Theses (Brief)

**Notion vs. Confluence:** Confluence assumed knowledge management is IT infrastructure (top-down, admin-configured, user-consumed). Notion's insight: knowledge creation is personal behavior that scales to teams. Bottom-up adoption path was structurally incompatible with Confluence's deployment model. Notion's weakness: personal flexibility creates organizational chaos at scale — any product with Notion's ease plus governance can attack at the standardization inflection.

**Stripe vs. Braintree/PayPal:** Incumbents framed the job as a business operations problem (accepting money safely, compliantly). Stripe redefined it as a developer problem (integrate payment into an application in hours, not weeks). Documentation was distribution strategy. Every developer who charged their first customer became an advocate. The wedge wasn't a better processor — it was destroying the premise that payment integration requires a merchant account setup call and 6-week certification.

**Sunsama vs. Things 3:** Different jobs. Things hired by people who want to **manage commitments** (capture and organization). Sunsama hired by people who want to **plan their days** (scheduling and intention-setting). Users don't switch because Things fails — they outgrow the job Things solves. Inbox-zero stops feeling like success when the underlying problem is "too many commitments, too little time." This is the firing lens applied: they fired Things because they discovered Things was solving the wrong problem.

---

## 11. The Five Forces (Threat-Vector Scan)

Porter's framework, used as a competitor diagnostic:

- **Supplier power:** Platform/API dependencies? (Slack depended on email infra and Google/Microsoft integrations — those suppliers were also competitive threats.)
- **Buyer power:** Substitutability? Linear holding price above Jira signals low buyer power in their segment (engineers choose tools, procurement doesn't negotiate).
- **Threat of substitutes:** Non-obvious alternatives? If users do the job in Notion instead of Jira, that matters more than Linear vs. Jira.
- **New entrant barriers:** Switching cost? Data gravity, integrations, workflows.
- **Competitive rivalry intensity:** Price moves, hiring signals (LinkedIn job posts), patent filings — all signal strategic direction.

---

## Sources

- [Brian Balfour — Why PMF Isn't Enough (Four Fits)](https://brianbalfour.com/essays/product-market-fit-isnt-enough)
- [a16z — Dynamics of Network Effects](https://a16z.com/the-dynamics-of-network-effects/)
- [Andrew Chen — The Cold Start Problem](https://andrewchen.com/)
- [How Linear Builds Product — Lenny Rachitsky](https://www.lennysnewsletter.com/p/how-linear-builds-product)
- [Obviously Awesome — April Dunford](https://www.aprildunford.com/books)
- *Crossing the Chasm* — Geoffrey Moore
- [Bob Moesta on JTBD — Intercom](https://www.intercom.com/blog/podcasts/podcast-bob-moesta-on-jobs-to-be-done/)
- [Positioning & Messaging Teardown — MKT1](https://newsletter.mkt1.co/p/positioning-and-messaging-teardown)
- [Linear Pricing Teardown — Tierly](https://tierly.app/blog/linear-pricing-teardown)
- [Wardley Mapping 101](https://www.wardleymaps.com/guides/wardley-mapping-101)
