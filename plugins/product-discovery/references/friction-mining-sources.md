# Friction Mining — Source Map by Domain

Where to find real, verbatim user friction at scale. Load on demand when running review/forum mining, competitor friction analysis, or pre-fieldwork research.

---

## 1. The Core Discipline — Verbatim Quotes or Nothing

Every theme surfaced from friction mining must link to **2-5 verbatim source quotes with URLs**. No theme exists without proof.

This is the rule that separates real friction mining from AI-generated plausibility theater. The quote is the evidence. The theme is a hypothesis about what the evidence means. An LLM can write a confident summary of 12 weak reviews that looks identical to a confident summary of 500 rich reviews. Volume must be declared. Provenance must be traceable.

The plugin should make every theme expandable to its source quotes, and every quote clickable to its URL.

## 1b. Tooling Reality — What WebFetch Can Actually Reach (Dogfood-Confirmed)

| Source class | WebFetch result | Workaround |
|---|---|---|
| Reddit threads (direct fetch) | ❌ blocked | Google site-scoped search → fetch cached snippets |
| App Store / Play Store reviews | ❌ JS-rendered, returns nothing | Paid APIs (AppFollow, AppTweak, Sensor Tower) or user-pasted |
| Twitter/X | ❌ similarly limited | Manually-pasted threads |
| G2 / Capterra / Trustpilot | ⚠ partial | Often need multiple URLs to get review content |
| HN comments / threads | ✓ full | Direct WebFetch |
| Forums (Obsidian, MacPowerUsers, head-fi, eng-tips) | ✓ usually full | Direct WebFetch |
| Medium / Substack / personal blogs | ✓ full | Direct WebFetch — "Why I switched from X" articles are gold |
| GitHub Issues / Discussions | ✓ full | Direct WebFetch |
| YouTube comments | ⚠ partial | Comment-export sites sometimes work |
| ProductHunt threads | ✓ usually full | Direct WebFetch |

**Implication:** the "Consumer SaaS" source spec naming App Store + Reddit as primary is aspirational. In practice, mine forums + Medium switcher articles + ProductHunt for Consumer SaaS friction, and flag App Store / Reddit limitations in the Gaps section.

When falling back on secondary sources (review aggregator articles that quote App Store/Reddit), mark each quote as `(secondary — original at <primary URL>)` to preserve provenance.

---

## 2. Source Map by Domain

### B2B SaaS

| Source | What It Surfaces | Watchouts |
|--------|------------------|-----------|
| **G2** | Structured pros/cons reviews from verified business buyers. Solid for procurement-stage friction (integration, support, pricing). | Astroturf risk — vendors solicit reviews. Look for unprompted specifics; ignore generic enthusiasm. |
| **Capterra** | Similar to G2; broader long-tail. Better for niche B2B categories. | Owned by Gartner; some review gating. |
| **TrustRadius** | Longer-form B2B reviews. Higher signal per review. Lower volume. | Skews to mid/large enterprise. |
| **Reddit (r/sysadmin, r/devops, r/sales, r/saas)** | Unvarnished frustration. Tool selection threads are gold. | Loud voices skew. Sample size per thread is small. |
| **LinkedIn comments** | When PMs/founders post about their product, the comment section often surfaces honest competitive friction. | Self-curated; people self-censor publicly. |
| **Vendor support forums** | Where users go after the product breaks. Highest-fidelity friction available. | Often gated; vendor moderation. |

### Consumer SaaS

| Source | What It Surfaces |
|--------|------------------|
| **App Store / Play Store reviews** | High volume, low signal individually. Best mined at scale (500+ reviews). |
| **r/[product]** subreddits | Power-user friction. The vocal minority — but their workarounds reveal what's broken at scale. |
| **ProductHunt comment threads** | Launch-day reactions. Good for first-impression friction. |
| **Twitter/X complaint threads** | Real-time friction surfacing during outages, redesigns, pricing changes. |
| **Indie Hackers forum** | Builder-to-builder friction with tools they use to ship. |

### Consumer Hardware

| Source | What It Surfaces |
|--------|------------------|
| **Amazon reviews (1-star and 5-star)** | One-star: precise failure modes at scale. Five-star: what users actually hired the product for (often not what marketing claimed). |
| **Best Buy reviews** | Less volume than Amazon, often more considered. |
| **r/BuyItForLife** | Durability expectations. What real users believe is well-made vs. disposable. |
| **iFixit teardowns + community** | Manufacturing quality, repairability decisions, durability failure patterns at component level. |
| **RTINGS** | Standardized lab testing for TVs, monitors, headphones, appliances. Free competitive benchmarking. Gold standard of what performance attributes matter to sophisticated users. |
| **Wirecutter category picks** | Reading 5 years of picks in your category reveals which attributes have been table stakes for years vs. still differentiators. |
| **Project Farm (YouTube)** | Independent stress-testing. Surfaces failure modes invisible to normal use. |
| **Category-specific forums** | Head-Fi / Audiogon / r/audiophile (audio), AVSForum (home theater), r/homeautomation, Bambu/LulzBot forums (3D printing) |

### Industrial / B2B Hardware

| Source | What It Surfaces |
|--------|------------------|
| **Trade publication review sections** | Domain-specific friction in trade-press write-ups. |
| **Manufacturer-specific user forums** | Where actual operators post when they hit field issues. |
| **r/welding, r/3Dprinting, r/machinist, r/electricians** | Workshop floor friction. |
| **J.D. Power / Consumer Reports** | Quantitative defect rates and reliability studies. Paid but systematic. |
| **YouTube field reviews from working professionals** | A welder's video of a tool review surfaces failure modes lab tests miss. |
| **Trade show feedback** (when accessible) | Why a product was passed over in person. |

### Developer Tools

| Source | What It Surfaces | Notes |
|--------|------------------|-------|
| **Hacker News** | Gold for dev tools. Comment threads on tool announcements are dense with critique and competitive comparison. | High signal-to-noise but loud-voices effect. HN posters skew toward early-adopter / contrarian. |
| **r/programming, r/webdev, r/devops** | Tool selection threads, frustration with incumbents. |
| **GitHub issues** | The friction users care enough about to file. Especially feature-request issues that stay open. |
| **Stack Overflow tag activity** | High tag volume = real friction (people need help). Surge in questions = changed something or surfaced a new pain. |
| **Twitter/X dev communities** | Quick reactions to tool launches and changes. |
| **DevTools podcast and newsletter comment sections** | Considered critiques. |

### Creator / Content Tools

| Source | What It Surfaces |
|--------|------------------|
| **YouTube creator forums + Discord servers** | Creators discussing tools they use to ship. |
| **r/NewTubers, r/PartneredYoutube, r/podcasting** | Workflow friction. |
| **Twitter/X creator communities** | Tool-switching threads. |
| **Notion / Obsidian / Roam community forums** | Knowledge workers building workflows on top of generic tools — friction with the underlying tool surfaces here. |

---

## 3. Extraction Methodology

### Volume Targets

| Goal | Reviews to Code |
|------|-----------------|
| Quick hypothesis generation | 20-40 |
| Coding for a real teardown | 40-60 |
| Pattern reliability at scale | 500-1000 (LLM-assisted) |

Below 20: you have anecdotes, not patterns. Above 1000 manually: you have wasted time — use LLM-assisted clustering.

### Sampling Strategy

- **Sort by recency** for first pass (last 6 months)
- **Sort by helpful-votes** for second pass (high-signal individual reviews)
- **Sample 1-star and 5-star separately.** One-stars surface failure modes; five-stars surface real jobs.
- **Skip the middle ratings.** 3-star reviews are mostly "fine, did the thing" — low information.
- **Avoid sorting by "verified purchase" alone** — astroturf accounts get verified.

### Thematic Coding

For each review, capture (see `competitor-teardown.md` for full version):

- **Functional job:** What were they trying to do?
- **Emotional job:** How did they want to feel?
- **Social job:** How did they want to be perceived?
- **Switch trigger:** What frustrated them enough to look?
- **Anchor phrase:** Verbatim language they use to describe the problem

After coding, look for:
- Themes appearing in >30% of reviews = pattern
- Surprising alternatives mentioned = real competitive landscape
- Frustrated-but-haven't-switched users = high F4 (habit lock-in, brittle moat)

### LLM-Assisted Coding at Scale

When mining 500+ reviews, use LLM-assisted clustering with these rules:

1. Every cluster must surface 2-5 representative verbatim quotes
2. Volume declared in UI ("based on 847 reviews")
3. Human reviews all clusters before they become "themes"
4. Confidence is a function of evidence mass — directional hypotheses from thin data, validated patterns from strong data

See `ai-era-discipline.md` for the full traceability requirements.

---

## 4. Astroturf Detection

The B2B SaaS review sites have known astroturf problems. Signals:

- **Generic enthusiasm** with no specifics ("Great tool! Best in class!")
- **Burst patterns** — many reviews in a short window, especially after a vendor solicitation campaign
- **Identical phrasing** across multiple reviews from different "users"
- **First-time reviewers only** — accounts created to leave one review
- **Missing pros/cons asymmetry** — only positives, no critique
- **Vendor-blessed language** ("game-changer," "synergy," "ROI") — real users use task-specific language

Discount any cluster of reviews that pattern-matches astroturf. Better signal: unprompted specifics, accounts with reviewing history across multiple categories, balanced pros/cons.

See `source-credibility-guide.md` for fuller source-weighting guidance.

---

## 5. Ethical Considerations

- **Public posts are research material.** Reviews, forum posts, public tweets — fair game.
- **Don't identify individuals** in any artifact that leaves the team. Even when names/handles are public, paraphrase or use [SYNTHETIC EXAMPLE] tags for any reproduced narratives.
- **Don't scrape gated forums** without permission. Vendor support forums and private Discords are not public material.
- **Don't post under false identity** to elicit responses. Lurking on a public forum is research; sock-puppet engagement is not.
- **NDA-covered research stays internal.** Don't aggregate friction from research participants and publish it as competitor analysis.

---

## 6. When Friction Mining Beats Interviews

| Situation | Use Friction Mining First | Use Interviews First |
|-----------|--------------------------|---------------------|
| You can't yet access users | Yes — desk research scaffolding | Wait |
| You want to pressure-test hypotheses before fieldwork | Yes | After |
| You need pattern coverage across thousands of users | Yes | Doesn't scale |
| You need causal mechanism (the "why") | No — surface only | Yes |
| You need emotional/social texture | Partial (verbatim quotes carry some) | Yes |
| You need to validate a job statement | No | Yes |

Friction mining is **breadth research**. It gives you the surface map at scale. Switch interviews are **depth research**. They give you the causal story behind any single switch. They complement; neither substitutes.

---

## Sources

- [Apple ML Research — App Store Review Summarization](https://machinelearning.apple.com/research/app-store-review)
- [iFixit](https://www.ifixit.com/)
- [RTINGS](https://www.rtings.com/)
- [Project Farm — YouTube](https://www.youtube.com/c/ProjectFarm)
- [Wirecutter](https://www.nytimes.com/wirecutter/)
- [Mining Consumer Experiences of Repairing Electronics — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S095965261631040X)
- [Klue — Competitive analysis with AI](https://klue.com/blog/how-to-do-competitive-analysis-with-ai)
