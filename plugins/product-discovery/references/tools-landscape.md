# Tools Landscape (Practitioner Reference)

The product discovery / research-ops tool ecosystem in 2026 — what each does, what each doesn't, and where this plugin's wedge sits. Load on demand when evaluating positioning, communicating with skeptical PMs, or comparing to a specific existing tool.

---

## 1. The Landscape in One Sentence

The PM tooling ecosystem (Productboard, Aha!, Roadmunk, Jira Product Discovery) has gone deep on **prioritization and roadmap visualization**. The research ops ecosystem (Dovetail, Notably, Looppanel) has gone deep on **synthesis tooling**. The AI agent layer (Zeda, Kraftful, Productboard Spark) has gone deep on **feedback ingestion and PRD drafting**. **Nobody has gone deep on running actual JTBD / ODI / OST end-to-end inside the framework, free, in the developer's environment.**

---

## 2. Major Tools — What They Are and What They Don't Do

### Productboard (+ Spark)
- **What it is:** PM platform connecting customer feedback to roadmap. Implements RICE, Kano, and ODI-flavored opportunity scoring. Productboard Spark (launched Oct 2025) is their AI agent — synthesizes feedback, drafts PRDs, runs competitive gap analysis. 150+ workflow templates.
- **What it doesn't do:** Run a real JTBD switch interview workflow. The opportunity scoring is template-only — there's no Bob Moesta-style force diagramming. Spark is document- and conversation-driven, not autonomously agentic — still needs human direction through pre-built workflows.
- **Pricing:** ~$19/maker/month (Essentials) to $300-400/maker/month (Enterprise). 20-seat team = $70K-$100K/year.

### Aha! Roadmaps
- **What it is:** Enterprise PM platform. Highly customizable scoring matrices. Strong multi-product portfolio. Added AI writing assistance 2024-2025.
- **What it doesn't do:** Encode JTBD or ODI as native methodology. AI is primarily a writing aid, not a discovery framework engine.
- **Pricing:** $59/user/month entry. Custom enterprise.

### Dovetail
- **What it is:** Dominant research repository. Auto-tagging, summary generation, "Ask Dovetail" chat across the repo. Filing cabinet with smart search.
- **What it doesn't do:** Know what a "job" is. JTBD lens must be applied by the researcher during synthesis. Dovetail organizes; it doesn't frame.
- **Pricing:** $39/user/month for teams; enterprise $21K+/year. Pricing increases have caused churn.

### Notably
- **What it is:** AI-first qualitative synthesis. Canvas-based, fast theme extraction. AI-native alternative to Dovetail.
- **What it doesn't do:** Collect interviews. Synthesis-only. No JTBD framework enforcement.
- **Pricing:** ~$50-200/user/month.

### Looppanel
- **What it is:** Speed-focused research ops. Auto-tagging, smart transcript search. Designed for high-volume interview teams.
- **What it doesn't do:** Run JTBD or ODI specifically.
- **Pricing:** $30-50/user/month range.

### Maze
- **What it is:** AI-first usability and concept testing. Unmoderated studies, in-product prompts.
- **What it doesn't do:** Generative discovery. Maze assumes you already know what to build and need to validate it.
- **Pricing:** Free (1 study/month), Starter $99/month, Enterprise $15K+/year.

### Zeda.io (closest direct competitor)
- **What it is:** AI-powered product discovery platform. Ingests GTM data, interviews, surveys, analytics, reviews. Auto-tags, clusters, surfaces opportunities. Drafts PRDs.
- **What it doesn't do:** Encode JTBD or ODI natively (surfaces clusters, not jobs). No OST. No codebase awareness.
- **Pricing:** $49-$299+/month per seat.

### Kraftful
- **What it is:** ChatGPT-powered tool for chatting with user data. Explicitly mentions JTBD and Double Diamond as methodologies.
- **What it doesn't do:** Persistent opportunity hierarchy. Every session starts fresh. No OST. No structured discovery artifact output.
- **Pricing:** $300/month Growth plan.

### Crayon / Klue
- **What they are:** Competitive intelligence platforms. Automated competitor monitoring (Crayon) and sales-team battlecards (Klue). Klue's Compete Agent (2025) delivers real-time intel to sellers.
- **What they don't do:** Discovery work. They're downstream of strategy (sales enablement), not upstream.
- **Pricing:** $20K-$40K/year custom enterprise.

### Strategyn ODIpro
- **What it is:** Tony Ulwick's firm's professional service + software tool for running full Outcome-Driven Innovation surveys. The canonical ODI implementation.
- **What it doesn't do:** Self-serve. Enterprise consulting engagement at tens of thousands per project.

---

## 3. The Frameworks Gap

| Framework | Source | Tool Implementation |
|-----------|--------|---------------------|
| **Opportunity Solution Tree (OST)** | Teresa Torres | **No native SaaS.** Teams use Miro/Notion manually. |
| **Outcome-Driven Innovation (ODI)** | Tony Ulwick / Strategyn | ODIpro enterprise service. Partially in Productboard Spark prompts. |
| **JTBD Switch Interview** | Bob Moesta | **No tool implementation.** Template PDFs only. |
| **Kano Model** | Noriaki Kano | Productboard, Aha!, airfocus (scoring options) |
| **RICE Scoring** | Sean McElrath (Intercom) | Productboard, Aha!, Linear, Jira |
| **Double Diamond** | British Design Council | Miro/Mural templates only |
| **Continuous Discovery Habits worksheets** | Teresa Torres | Sold through Product Talk Academy; not in any SaaS |

**The OST gap is the biggest.** It's the most widely adopted modern PM discovery framework, and no tool natively builds and maintains one. Teams run it in Miro with sticky notes.

---

## 4. The Plugin's Wedge

Six structural advantages the plugin holds over the SaaS competitive set:

### Wedge 1: Codebase-Aware
Every tool above lives entirely in the PM world. None know what's in the code, what's technically trivial vs. expensive, or what's already partially built. A Claude Code plugin has unique access to the codebase. This is **a genuinely unavailable angle for any SaaS competitor**.

### Wedge 2: Free
The ecosystem ranges from $39/user/month (Dovetail) to $300+/maker/month (Productboard Enterprise). Free tiers are severely limited. A Claude Code user gets the plugin at zero marginal cost. The cost of being wrong with the plugin is minutes; the cost of being wrong with Productboard is an annual contract.

### Wedge 3: Actually Runs the Frameworks
Kraftful **names** JTBD. Productboard Spark **has an ODI template**. But none of them actually **run** a real JTBD decomposition — breaking down functional/emotional/social jobs, ranking by evidence, applying the switch interview lens. This is always done by a human consultant or well-read PM, never by the tool itself.

The plugin should be the first that **actually runs** JTBD switch interviews, ODI opportunity scoring with the floor-at-zero formula, and OST maintenance — not just names them.

### Wedge 4: No Setup, No Maintenance
Zeda, Dovetail, EnjoyHQ all require feeding data in. Maintenance burden is a consistently cited adoption failure mode. A plugin triggered during a coding session, reading existing files and context, avoids the setup/maintenance problem entirely.

### Wedge 5: Living OST in a Folder
No tool maintains a living Opportunity Solution Tree from interview notes, customer signals, and experiment results. The plugin can — and it lives in the user's repo as Markdown, version-controlled, no dashboard required.

### Wedge 6: Judgment Layer
Productboard Spark generates a PRD. Zeda generates an opportunity list. Dovetail generates themes. **None of them help a PM make the actual prioritization call** with business goals, team capacity, technical constraints, and strategy in mind. The plugin can synthesize across these because it sees the whole project context.

---

## 5. What the Plugin Should NOT Try to Be

- **Not a research repository.** Dovetail is better at storage. Use it.
- **Not a roadmap visualizer.** Productboard / Aha! are better at this.
- **Not a usability testing platform.** Maze, UserTesting own this.
- **Not a competitive intelligence service.** Crayon / Klue do continuous monitoring at enterprise scale.

The plugin's wedge is upstream of all of these: **running the actual discovery frameworks rigorously, in context, free, with codebase awareness.**

---

## 6. Pricing Reference

| Tool | Entry | Enterprise |
|---|---|---|
| Productboard | ~$19/maker/month | $300-400/maker/month |
| Aha! Roadmaps | $59/user/month | Custom |
| Dovetail | $39/user/month | $21K+/year |
| Maze | $99/month (Starter) | $15K+/year |
| Zeda.io | $49/month (team) | $299+/month |
| Kraftful | $300/month (Growth) | Custom |
| Crayon | Custom | $25K-40K/year |
| Klue | Custom | $20K-40K/year |
| Miro | Free–$10/user/month | Custom |
| **Claude Code plugin** | **$0 marginal cost** | **—** |

---

## Sources

- [Productboard Spark](https://www.productboard.com/product/spark/)
- [Productboard opportunity scoring framework](https://www.productboard.com/skills/opportunity-scoring-framework/)
- [Aha! pricing](https://www.aha.io/roadmaps/pricing)
- [Dovetail pricing](https://dovetail.com/pricing/)
- [Strategyn ODI](https://strategyn.com/outcome-driven-innovation/)
- [Strategyn ODIpro](https://strategyn.com/odipro/)
- [Zeda.io](https://zeda.io/)
- [Kraftful vs Zeda comparison](https://www.kraftful.com/vs/zeda-io)
- [Crayon review](https://research.com/software/reviews/crayon)
- [Klue vs Crayon comparison](https://parano.ai/blog/klue-vs-crayon)
- [Lenny's State of Tech Tools 2025](https://www.lennysnewsletter.com/p/the-state-of-tech-tools-in-2025)
