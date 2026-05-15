# Source Credibility Guide (Practitioner Reference)

How to weight the signal coming from different review and feedback sources. Load on demand when running friction mining, competitor teardowns, or anywhere the plugin is interpreting third-party voice-of-customer data.

---

## 1. The Core Discipline

Different sources have different selection biases and astroturf risks. A theme appearing 30 times on G2 is not equivalent to 30 mentions on Reddit or 30 mentions on Hacker News. The plugin should **declare source mix** and **weight signals by source character** — not just count mentions.

---

## 2. Source-by-Source Weights

### G2 (B2B SaaS Reviews)

**Signal type:** Verified business buyers writing structured pros/cons reviews. Solid for procurement-stage friction (integration, support, pricing, deployment).

**Strengths:**
- Verified employer/title fields
- Structured pros/cons schema forces some balance
- Volume is significant for mid-to-large B2B products
- Includes deployment context (company size, industry, role)

**Astroturf risk:** **Medium-high.** Vendors actively solicit reviews. Look for:
- Burst patterns (many reviews in short windows after a solicitation campaign)
- Generic enthusiasm with no specifics
- Identical phrasing across "different" reviewers
- First-time reviewer accounts only
- Missing critique on the cons side (or generic critique like "could have more integrations")

**Weighting move:** Discount any cluster of reviews matching astroturf signals. High-signal G2 reviews use task-specific language, have balanced pros/cons, and come from accounts with history across multiple product reviews.

### Capterra / TrustRadius

Similar to G2 but with different selection biases:
- **Capterra:** broader long-tail; better for niche B2B; owned by Gartner with some review gating
- **TrustRadius:** longer-form reviews, higher signal per review, lower volume; skews mid/large enterprise

**Weighting:** Generally higher trust per review than G2 (more effort to write), but smaller corpus.

### App Store / Play Store Reviews

**Signal type:** Consumer app reviews. High volume, low signal individually.

**Strengths:**
- Volume (often thousands of reviews per app)
- One-star reviews surface precise failure modes at scale
- Five-star reviews reveal what users actually hired the product for

**Weaknesses:**
- Individual reviews are short and low-context
- Star ratings spike after updates and prompts
- "Verified purchase" / install is automatic; doesn't filter accounts well
- App review prompts (in-app "rate us") skew toward positive ratings when users are happy with a specific moment

**Weighting move:** Treat at scale, not individually. 500+ reviews mined for patterns gives directional signal. Single reviews are anecdote. Always read 1-star and 5-star separately — middle ratings are mostly "fine, did the thing" with low information.

### Reddit

**Signal type:** Unvarnished frustration. Tool selection threads can be gold. Workflow discussions reveal mental models.

**Strengths:**
- No vendor incentive to write (low astroturf risk for organic threads)
- Long-form, conversational, often technical
- Subreddit specialization gives domain context (r/sysadmin, r/devops, r/audiophile, r/3dprinting, etc.)
- Comments build on each other — patterns emerge in thread structure

**Weaknesses:**
- **Loud-voices skew:** vocal minority drives threads
- Subreddit culture biases (r/programming skews early-adopter; r/sysadmin skews curmudgeonly)
- Sample size per thread is small
- Karma incentives favor strong opinions
- Astroturf risk for specific vendor mentions (paid commenters)

**Weighting move:** Use for **breadth of pain language** and **competitive alternative discovery** (what do users mention as substitutes you didn't know existed?). Don't use for prevalence estimates. A thing being discussed on Reddit means people care; it doesn't mean most users feel that way.

### Hacker News

**Signal type:** Developer-tool gold mine. Considered critiques. Comment threads on tool announcements are dense with competitive analysis.

**Strengths:**
- Technical depth in critique
- Competitive comparison is the cultural default in comment threads
- High signal per comment for dev-tool decisions
- Submitter accounts have visible history

**Weaknesses:**
- **HN posters skew early-adopter, contrarian, security-paranoid, anti-VC**
- Vocal minority is even more vocal than Reddit
- "Things HN hates" often correlate weakly with mainstream user reactions
- Top-comment effects bias subsequent commentary

**Weighting move:** Use for dev-tool category understanding and surfacing technical critique angles. Don't generalize HN sentiment to consumer or non-developer audiences. A product can be hated on HN and beloved by its actual users.

### Trustpilot

**Signal type:** B2C and B2B service reviews. Often used for SaaS contracts, financial services, e-commerce.

**Strengths:**
- Verified purchase/contract checks (some)
- Long-form reviews with star ratings

**Weaknesses:**
- **Astroturf risk: high.** Trustpilot has documented manipulation problems
- Vendors can flag and remove reviews
- Selection bias toward angry users (review-after-bad-experience pattern)
- B2B contract reviews skew toward post-cancellation grievance

**Weighting move:** Treat as one data source among many. Cross-reference patterns against other sources before treating Trustpilot signal as primary.

### Niche Forums (Head-Fi, AVSForum, manufacturer-specific)

**Signal type:** Deep domain expertise. Long-tenured users with strong opinions and reference points.

**Strengths:**
- Long-form, technically detailed
- Cross-product comparisons by users who've owned many
- Failure-mode documentation at component level
- Cultural memory (decade-old threads still referenced)

**Weaknesses:**
- **Enthusiast skew:** these users are not typical buyers
- Pricing tolerance is wildly different from mainstream (audiophiles spending $5K+ on headphones is normal)
- Tribal affiliations bias opinions
- "Burn-in" / placebo cultures in some communities

**Weighting move:** Use for **failure modes**, **technical critique**, **competitive landscape** (what do enthusiasts compare against?). Don't use for mainstream pricing or feature decisions.

### Wirecutter / RTINGS / Project Farm

**Signal type:** Structured editorial/lab review. Third-party with stated methodology.

**Strengths:**
- **Wirecutter:** clear methodology, broad consumer perspective, longitudinal updates
- **RTINGS:** standardized lab tests with raw data published, free competitive benchmarking
- **Project Farm:** independent stress testing on YouTube, methodology visible

**Weaknesses:**
- Affiliate revenue creates some pressure (Wirecutter)
- Lab tests don't capture daily-use friction
- Single reviewer's preference still influences (Wirecutter picks reflect a perspective)

**Weighting move:** **High trust per source, low volume.** Use as anchor points for "what attributes matter in this category" — read 5 years of picks to see what's table stakes vs. still differentiator.

### GitHub Issues / Stack Overflow

**Signal type:** Friction users care enough about to file or ask publicly.

**Strengths:**
- **GitHub issues:** feature-request issues that stay open are the friction users care about most
- **Stack Overflow tag activity:** surge in questions = changed something or new pain surfaced

**Weaknesses:**
- Skews to technical users
- Comment quality varies wildly
- Closed-as-duplicate doesn't mean solved
- Stack Overflow can have answer-quality decay (old top answers no longer correct)

**Weighting move:** **High signal for dev tools.** Open issues with many upvotes/comments are gold. Stack Overflow tag velocity is a leading indicator of friction.

---

## 3. Astroturf Detection (Cross-Source)

Universal signals of fake or solicited reviews:

- **Generic enthusiasm with no specifics:** "Great tool!" "Best in class!"
- **Burst patterns:** many reviews in short windows
- **Identical phrasing** across "different" reviewers
- **First-time reviewers only** with no other review history
- **Missing critique:** all positives, no genuine cons
- **Vendor-blessed language:** "game-changer," "synergy," "ROI," "best-of-breed"
- **Accounts created just before review** (Reddit, G2, Trustpilot)
- **Posting from corporate IP ranges** (when detectable in metadata)

**The opposite signature — high-trust indicators:**
- Specific dates, specific feature names, specific edge cases
- Balanced pros/cons (real users have mixed feelings)
- Account has reviewing history across multiple products in the category
- Task-specific language users in the domain actually use
- Comparisons to unexpected alternatives (real users mention what they actually considered)

---

## 4. The Cross-Source Triangulation Rule

A pattern appearing in **one source** is hypothesis. A pattern appearing across **three different source types** (e.g., G2 + Reddit + niche forum) is validated.

**Single-source themes:** flag with caveat ("based only on G2 reviews — verify against forum discussion").

**Multi-source themes:** can be presented with higher confidence.

**Contradictory-across-sources:** the most interesting case. Often surfaces that the product has different reputations among different audiences (loved by power users on r/X, hated by mainstream on App Store). This is strategic signal, not noise.

---

## 5. Quick Reference Table

| Source | Astroturf Risk | Signal Type | Best For |
|--------|---------------|-------------|----------|
| G2 | Medium-high | Verified B2B reviews | Procurement friction |
| Capterra | Medium | Long-tail B2B | Niche categories |
| TrustRadius | Low-medium | Long-form B2B | Enterprise decisions |
| App Store | Low | Consumer at volume | Scale failure mode mining |
| Reddit | Low (specific vendors: medium) | Vocal minority | Pain language, competitive discovery |
| Hacker News | Low | Early-adopter dev critique | Dev tool decisions only |
| Trustpilot | **High** | B2C / B2B contract | Cross-reference only |
| Niche forums | Low | Enthusiast deep dive | Failure modes, technical critique |
| Wirecutter | Low (affiliate pressure exists) | Curated editorial | Category table stakes |
| RTINGS | Very low | Lab measurement | Performance benchmarking |
| Project Farm | Very low | Independent stress test | Durability |
| GitHub Issues | Very low | Self-filed friction | Dev tool feature gaps |
| Stack Overflow | Very low | Help-seeking signal | Friction velocity |

---

## Sources

- [Apple ML Research — App Store Review Summarization](https://machinelearning.apple.com/research/app-store-review)
- [Mining Consumer Experiences of Repairing Electronics — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S095965261631040X)
- [Klue — Competitive analysis with AI](https://klue.com/blog/how-to-do-competitive-analysis-with-ai)
- [G2 Trust & Verification](https://www.g2.com/about/trust)
- [Trustpilot Transparency Report](https://www.trustpilot.com/trust/transparency-report)
