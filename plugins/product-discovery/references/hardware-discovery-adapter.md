# Hardware Discovery Adapter (Practitioner Reference)

How discovery methodology adapts when the product is physical. Load on demand when the plugin detects hardware context (BOM mentions, manufacturing, prototyping, fixtures, certification, retail packaging).

---

## 1. Why Hardware Is Different (in Three Sentences)

Manufacturing lead times compress the research window — tooling is 8-16 weeks and $20K-$150K; once cut, you're frozen. Every feature has a per-unit BOM cost, multiplied by every unit built — adding a sensor is not free. A 3% defect rate at 100K units at $200 ASP costs $600K+ before brand damage — the cost of an assumption surviving to manufacturing is asymmetric.

This means: hardware discovery has a hard deadline software doesn't have. Front-load the learning through cheap methods so when you commit to tooling, you commit with high confidence.

---

## 2. Narrative-Before-Spec — The Fadell Press Release

Tony Fadell's central thesis (*Build*, 2022): **the product story must exist before the product.**

> Write the press release for the product before you design it. If you cannot write it, you do not yet understand the problem well enough to build the solution.

The Nest thermostat narrative: "the thermostat is the ugliest, most annoying device in your house, and also the one that controls 50% of your energy bill — yet it hasn't been redesigned in 30 years." Every design decision was evaluated against this story.

What the press release must answer:
- Why must this product exist?
- Who currently suffers from its absence (specifically)?
- How is the world different once it exists?
- What is the single sentence headline?

If a feature cannot be explained inside this narrative, it should not exist.

**Plugin behavior:** for hardware projects, surface the press-release artifact early. If a user is jumping to BOM and component selection without one, prompt: "what's the press release for this?"

---

## 3. The Fidelity Ladder — Match Research to Prototype Stage

Research questions and methods should match the prototype stage. User research is most valuable at stages 1-5. By stage 6, you're validating engineering.

| Stage | Name | Purpose | Research Questions |
|-------|------|---------|-------------------|
| 1 | Sketch / cardboard | Form factor intuition | "Does this shape feel right to hold?" |
| 2 | Foam model | Ergonomics, proportion | "Is this the right size? Where does my thumb go?" |
| 3 | 3D-printed shell | Visual desirability, material sense | "Would I be proud to own this?" |
| 4 | Works-like prototype | Functional validation | "Does it do the job?" |
| 5 | Looks-like + works-like | Integrated validation | "Is this the real experience?" |
| 6 | EVT (Engineering Validation) | Engineering compliance | "Does it meet spec?" |
| 7 | DVT (Design Validation) | Pre-production verification | "Is it ready to build?" |
| 8 | PVT (Production Validation) | Manufacturing validation | "Can we build this at scale?" |

**Critical move:** decide which fidelity dimension to prioritize for each research question. **Looks-like** mockups test desirability, form, ergonomics, packaging (show to retail buyers, designers, investors). **Works-like** mockups test the value proposition and edge cases (ugly, bench-powered, but functional). The mistake teams make is building looks-like-and-works-like simultaneously too early — spending 6 months when they should have separated the two questions.

---

## 4. BOM-Weighted Prioritization

Every feature decision in hardware has a direct dollar cost in the Bill of Materials, multiplied across every unit shipped. A feature that a software team would ship behind a flag has no equivalent in hardware.

**Prioritization adapter:** the ODI opportunity score (`I + max(I−S, 0)`) needs a BOM-weighted variant. A high-opportunity outcome that requires a $40 BOM addition may be lower-priority than a medium-opportunity outcome that's $2.

```
BOM-Adjusted Opportunity = Opportunity Score / BOM Cost Impact
```

Or, more rigorously: rank outcomes by opportunity score, then for each, capture the BOM cost to address. Visualize on a 2x2: opportunity score (y) vs. BOM cost (x). Upper-left (high opportunity, low BOM cost) is the obvious win.

**The plugin should not let users treat hardware features as toggle-able.** When a user is treating a hardware feature as "we can add it later," surface: this is permanent. Whatever ships in manufacturing is what the customer receives for the product's entire life. No flags, no patches, no rollback.

---

## 5. Customer-Journey Prototyping (Fadell's Screwdriver)

Fadell's Nest team famously prototyped **the installation experience** — not just the thermostat itself. They sourced every screwdriver on the market, realized users would struggle with their existing tools, and designed a custom screwdriver that shipped with every unit.

**This was not ergonomics research; it was journey research.** The job was "get my home comfortable," and that job starts with taking the old thermostat off the wall.

**Adapter rule:** for hardware, the product is not just the device. It's the unboxing, the installation, the first use, the integration with existing systems, the maintenance, the failure scenarios, the disposal. Discovery must encompass the full journey.

Map the journey explicitly:
1. **Discovery / consideration** — how do they hear about this? What competitors do they compare to?
2. **Purchase** — retail or D2C? What price point? What packaging encounter?
3. **Unboxing** — first physical touch. Most emotionally loaded moment in the journey.
4. **Setup / installation** — what do they need? What's their existing toolkit?
5. **First use** — does it deliver the press release?
6. **Daily use** — habit formation. Where does it live? How does it integrate with their other devices?
7. **Maintenance** — cleaning, recharging, replacement parts.
8. **Failure / repair** — what happens when it breaks?
9. **Disposal / upgrade** — end of life.

Friction at any stage kills the journey. Returns happen at unboxing and setup as often as during use.

---

## 6. iFixit and Repair-Forum Friction Mining

Hardware-specific sources for friction at scale:

- **iFixit teardowns:** manufacturing quality, repairability decisions, component sourcing, thermal management, internal assembly. Surfaces competitor constraints you can potentially avoid.
- **iFixit community forums:** users post after the product fails in the field. Highest-fidelity friction data outside your own returns database.
- **Reddit r/fixit, r/BuyItForLife:** durability expectations and failure patterns.
- **Manufacturer-specific forums** (Bambu Lab, LulzBot, audio brands, etc.): post-purchase friction from owners.
- **Project Farm (YouTube):** independent stress testing. Free durability research for your category.
- **RTINGS:** standardized lab testing for TVs/monitors/headphones/appliances. Gold-standard performance attributes.
- **Wirecutter pick archives:** five years of picks in your category reveals which attributes have been table stakes for years.
- **J.D. Power / Consumer Reports:** quantitative defect rates at scale (paid).

See `friction-mining-sources.md` for the full source map.

---

## 7. B2B Dual-User Flag

In B2B / industrial hardware, **the person who signs the purchase order is almost never the person who uses the product daily.** Discovery must interview both.

| Role | Cares About |
|------|-------------|
| **Economic buyer** (VP Ops, Plant Manager, Procurement) | ROI, TCO, integration, support SLA, regulatory compliance |
| **End user** (technician, nurse, operator) | Ergonomics, speed, reliability, training burden, what breaks |

These parties often have **opposing preferences**. Discovery that only reaches one level produces a product that wins the sale and fails in the field, or vice versa.

**Plugin behavior:** when the project is B2B hardware, flag the dual-user requirement and prompt for both interview pools. Do not let users substitute one for the other.

Additional B2B-hardware notes:
- Small-N, high-stakes: 5-15 customers may represent the entire addressable market. Each conversation carries enormous weight.
- On-site research is non-negotiable. The environment is the context. Lighting, noise, glove-wearing, supervisor visibility — none of this surfaces in a research facility.
- Sales cycles are 3-18 months. Discovery should be proportionally patient: multiple on-site visits over weeks.

---

## 8. Smoke Tests That Work for Hardware

- **Kickstarter as market research:** if a product concept in your category has Kickstarter history, the campaign pages, backer comments, and update threads are a research archive. What did backers ask about? What did the creator get wrong in v1?
- **Landing-page smoke test:** describe the product, show renders or mockups, state the price, include a pre-order/waitlist button. Drive targeted traffic. Measure CTR. Tests resonance, price friction, and value-prop angles without a working prototype. Runs in days.
- **Concierge MVP:** before building the automated system, can a person deliver the outcome manually? Validates the outcome's value before committing engineering investment. Example: before building a smart home sensor network, hire someone to manually check readings and send homeowners daily reports.
- **Mock packaging tests:** show participants the packaged product on a shelf, next to competitors, at real retail price. Packaging is the first physical touchpoint; the emotions it generates predict return rates.

---

## 9. Three Software-Only Moves That Do NOT Translate

The plugin should **block or warn** when a user treats these as available in hardware:

### Move 1: A/B Testing Is Mostly Impossible
Software A/B testing assumes two versions ship simultaneously, users randomly assigned, results in days, losing version discarded at zero cost. None of this works in hardware. The closest hardware analog is sequential cohort testing — much lower confidence, higher methodological caveats.

### Move 2: "Fail Fast" Is Wrong — "Learn Fast, Fail Early"
Hardware iteration cycles are 6-12 weeks minimum (board respins, tooling changes, mechanical revisions). Cost of a design change at EVT stage is 10-100x the cost of the same change at concept stage. "Fail fast" must be translated to: **fail early in the fidelity ladder, not late.** Front-load learning through cheap methods (foam, cardboard, renders, customer conversations).

### Move 3: Feature Flags / Continuous Deployment — Doesn't Exist
You cannot flag a button into existence or toggle a speaker's frequency response. **Whatever ships in manufacturing is what the customer receives, for the product's entire life.** The discovery phase must surface **complete** requirements, not minimum requirements. A software MVP can ship without search and add it later. A hardware MVP cannot ship without a microphone and add one later.

The plugin should surface this constraint explicitly when a user is treating a hardware feature as optionally deferrable.

---

## 10. Quick Plugin Adapter Rules

When hardware context is detected (BOM, tooling, manufacturing, certification, packaging mentioned):

1. **Require press release** as an artifact before deep planning
2. **Surface fidelity ladder** and ask which stage they're at
3. **Add BOM-cost dimension** to opportunity scoring
4. **Require customer-journey map** that includes unboxing/install/maintenance/disposal
5. **Flag dual-user requirement** for B2B hardware
6. **Block "fail fast" framing** — replace with "learn fast, fail early"
7. **Block feature-flag mental model** — surface that hardware features ship permanent
8. **Suggest iFixit / RTINGS / Project Farm** as competitive friction sources
9. **Surface regulatory feasibility check** (FCC, CE, UL, FDA, RoHS/REACH) as a gate, not an afterthought

---

## Sources

- *Build* — Tony Fadell (2022). [Andrew Clark summary](https://andrewclark.co.uk/product-book-summaries/build)
- [IDEO Human-Centered Design — UserTesting](https://www.usertesting.com/blog/how-ideo-uses-customer-insights-to-design-innovative-products-users-love)
- [Apple Industrial Design Group — IxDF](https://ixdf.org/literature/article/apple-s-product-development-process-inside-the-world-s-greatest-design-organization)
- [Dyson Innovation Journey — Enle Innovations](https://innovate.enle.org/dysons-engineering-revolution-the-journey-of-james-dyson-in-building-a-billion-dollar-brand/)
- [Hardware/Software Discovery — Encata](https://www.encata.net/blog/discovery-phase-in-software-and-hardware-projects)
- [Nest Thermostat — IEEE Spectrum](https://spectrum.ieee.org/the-consumer-electronics-hall-of-fame-nest-thermostat)
- [Hidden Challenges of Agile in Hardware — PRG](https://prgnpi.com/the-hidden-challenges-of-agile-in-hardware-development/)
- [Prototype Fidelity for Startups — FasterCapital](https://fastercapital.com/content/Prototype-fidelity--Prototype-Fidelity-for-Startups--How-to-Choose-the-Right-Level-of-Detail-for-Your-Prototype.html)
