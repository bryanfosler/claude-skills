# UX Research Complement (Practitioner Reference)

Seven UX research moves that complement JTBD/ODI without duplicating. Load on demand when the plugin needs a method that JTBD/ODI don't cover — usability friction, behavioral observation, organizational research, mental-model excavation.

---

## 1. Why This Reference Exists

JTBD and ODI are foundational for the **discovery** end (what problem is real, what outcomes matter, why people switch). They are not the only methods. Below are seven canonical UX research moves that fill specific gaps JTBD/ODI don't address.

This reference does not duplicate JTBD/ODI content. It surfaces the methods you reach for when those frameworks aren't the right tool.

---

## 2. The Foundational 2x2 — Attitudinal vs. Behavioral, Qual vs. Quant

From Christian Rohrer / NN/g. The single most important framing in UX research practice.

|  | **Qualitative** | **Quantitative** |
|---|---|---|
| **Attitudinal** (what they say) | Focus groups, user interviews, concept testing | Surveys, desirability studies, preference tests |
| **Behavioral** (what they do) | Usability testing, field studies, contextual inquiry | A/B testing, analytics, eye-tracking, tree testing |

**The critical insight:** what people say and what they do routinely contradict each other. Users say they want minimalist interfaces but click on links buried in dense text. They say they care about privacy but share data freely for small conveniences.

**Behavioral data is ground truth. Attitudinal data is self-report.** Both are necessary; neither alone is sufficient.

The classic mistake: using qualitative data to make quantitative claims ("our users prefer X"), or quantitative data to explain causation ("38% dropped off, so they must be confused").

---

## 3. The Generative vs. Evaluative Distinction

The most expensive research mistake in product practice is substituting evaluative research for generative research.

| | Generative | Evaluative |
|---|-----------|------------|
| Goal | Discover what's true | Test if a specific design works |
| Output | New understanding | Verdict on a solution |
| Question | "What is happening, and why does it matter?" | "Does this work for these users?" |
| Methods | Contextual inquiry, ethnography, diary studies, mental-model research, JTBD switch interviews | Moderated usability, A/B testing, first-click, concept testing |

**Substitution trap:** teams run usability tests on solutions to problems they haven't validated exist. They A/B test versions of a feature that serves no real user need. They collect NPS from users who don't understand what they're evaluating. JTBD and ODI exist precisely because they are rigorously generative.

The plugin should detect when a user is reaching for an evaluative method (usability test, A/B, concept test) on a problem that hasn't been generatively validated. Surface: "before testing this design, have you validated the problem is real?"

---

## 4. The Seven Methods

### Method 1: Portigal Behavioral Interviewing

Steve Portigal's *Interviewing Users* (2nd ed., 2023) is the closest thing to a technical manual for the interview itself.

**Seven stages of a research interview:**
1. Threshold crossing (entering the space)
2. Restating objectives ("we're here to learn from you, not test you")
3. Kick-off questions (broad, easy, low-stakes)
4. Accepting awkwardness (silence and stumbling)
5. The tipping point (they stop performing, start talking)
6. Reflection and projection (meaning, priorities, comparisons)
7. Soft closure (doorknob moment — guards fully down)

**Question types, in order:**
- **Grand tour:** "Walk me through what a typical Tuesday looks like for you." Give them latitude to show what they think is important.
- **Behavioral:** "Tell me about the last time you had to [do this thing]." Past behavior, not hypothetical futures. Far more predictive than stated intentions.
- **Opinion probes:** "How did that feel?" Used sparingly, after behavioral grounding. Opinions unanchored to behavior are the least reliable data in the toolkit.
- **Comparison:** "How is this different from how you used to do it?" Surfaces mental models direct questions miss.

**Disclosure ladder:** facts → behavioral specifics → emotional content → evaluation and meaning. Jumping to emotion before behavior produces shallow or defensive responses.

**Anti-patterns:**
- Hypothesis confirmation: "Would you say checkout was confusing?" → "Tell me what happened at checkout."
- Future-hypothetical trap: "Would you use a feature that did X?" Worthless data.
- Silence avoidance: jumping in to fill pauses. Silence is often where the most interesting content lives.

### Method 2: Indi Young Problem-Space Research

Young's critique: the entire UX industry is addicted to the solution space and uses research to rationalize it.

**Problem space vs. solution space.** Standard UX asks "how do users use our product?" — already presupposing the product is the answer. Problem-space research asks: "What is going through someone's mind as they pursue a purpose — before any product enters the picture?"

**Method:** recruit people who share a *goal or purpose* (not users of a specific product). Long-form listening sessions focused entirely on inner thinking, emotional reactions, guiding principles. The product is never mentioned.

**Mental Model Skyline:** the output is a visual artifact laid out like a city skyline. Each "tower" represents a cognitive task cluster; each "window" within it is a verbatim summary of inner thinking from a real person. The skyline is then overlaid with the team's existing product capabilities to reveal gaps.

**Thinking Styles replace personas.** Young's critique of personas: demographic-based personas introduce stereotyping and carry "flavor like a horoscope" — they feel real but don't reliably predict behavior. Thinking styles are 3-5 sentence archetypes defined purely by **how people approach a specific purpose**: cognitive approach (systematic vs. intuitive), characteristic emotional reactions under stress, guiding principles. Demographics-free. Two people with completely different demographics can share a thinking style.

### Method 3: Contextual Inquiry

A hybrid of field observation and interview. Researcher shadows the participant while they work and asks questions **in context**: "I see you just opened a spreadsheet there, what's that for?"

**When to use:** complex workflows; expert users whose tacit knowledge is hard to surface through interview alone; when you need both behavioral data (what they do) and cognitive data (why they do it) in a single session.

**When not:** when you have limited time and need breadth across many participants (expensive per participant); when behavior is intermittent or time-distributed (diary studies fit better).

**Critical move:** validate observations in real time. "I noticed you skipped that step — was that intentional?" Don't wait for synthesis to ask.

### Method 4: Torres OST + Assumption Mapping

Teresa Torres' Opportunity Solution Tree (from *Continuous Discovery Habits*, 2021). A visual decision tool with four levels:

1. **Desired outcome (root):** specific, measurable product metric the team controls. Not a business goal — a user behavior metric. "Increase weekly active users," not "grow revenue."
2. **Opportunity space (branches):** unmet customer needs discovered through ongoing interviews.
3. **Solutions (leaves):** specific product ideas. **Generate at least three solutions per opportunity before evaluating any** — avoid falling in love with the first idea.
4. **Assumption tests (experiments):** surgical tests of the specific beliefs each solution depends on.

**Assumption mapping** is the operational mechanism that makes continuous discovery fast:
- Plot assumptions on a 2x2: how important is this to the solution's success vs. how much evidence do we have that it's true?
- The quadrant with **high importance + low evidence** is where you test first.
- Most assumption tests run in 1-2 days; most full-prototype tests take weeks.

**Weekly customer interviews as keystone habit.** Not a research project — a team habit like standup. Goal is continuous, low-overhead exposure to customer thinking.

### Method 5: Hall Organizational Research

Erika Hall (*Just Enough Research*, 2013, 2nd ed. 2019): before researching users, research **yourself.**

Teams build products that reflect internal politics and assumptions more than user needs. Hall treats organizational research as the essential first step:
- What does your organization believe about its users?
- What assumptions are baked into your processes, roadmap, success metrics?
- What stakeholder beliefs and incentives is the team actually working against?

**Why this matters:** if the team's stated user model conflicts with the implicit user model the organization rewards, research will produce findings that get ignored. The team needs to know what mental models they're actually operating within.

Hall's framing: "just enough research" is not permission to do less — it's an argument against research as bureaucratic cover. Enough research is what reduces uncertainty enough to make better decisions.

### Method 6: Affinity Diagramming + Five Whys

**Affinity diagramming** is the primary synthesis method for converting raw observations into themes.

Process:
1. One observation per card — verbatim quotes or direct behavioral observations preferred
2. Group silently in parallel (multiple researchers), then discuss outliers
3. Name clusters at the highest level of abstraction that remains honest
4. Identify second-order patterns across clusters

Critical discipline: **name clusters with insight statements, not category labels.** "Users abandon checkout when surprised by shipping costs" — not "checkout."

**Five Whys** is the causal-chain technique applied after affinity diagramming. When a theme surfaces, ask "why?" five times recursively to trace from symptom to root cause.

Example:
- Users abandon the setup flow. → Why?
- They hit a required field they don't know how to fill. → Why?
- The field label is ambiguous. → Why?
- The design team didn't know users' terminology. → Why?
- No early-stage research was done with target users. → Why?
- The team assumed users shared their mental model.

The five whys don't guarantee finding the right root cause, but they reliably push past first-order symptoms into structural explanations.

**Synthesis anti-patterns:**
- Theming without evidence (naming clusters before reading all the data)
- Outlier suppression (treating edge cases as noise — they often contain the most actionable signal)
- Level confusion (mixing behavioral observations with inferences in the same cluster)

### Method 7: Diary Studies

Participants self-document experiences over days or weeks — prompted journal entries, photos, structured logs.

**When to use:**
- Behavior is distributed over time or episodic
- Tied to triggering conditions that don't happen in lab sessions
- Health behaviors, financial decisions, planning cycles, fluctuating emotional states
- Hardware products with irregular use patterns
- Understanding how usage evolves once novelty wears off

**Core tradeoff:** diary studies sacrifice observational validity (self-report = attitudinal) for temporal breadth. They capture what field studies miss: the full arc over time, including quiet moments between touchpoints.

---

## 5. Method-for-the-Question Decision Tree

```
WHAT ARE YOU TRYING TO DO?

Is the problem validated?
├── NO → Generative research first
│   ├── Need user's context/environment? → Contextual inquiry or ethnographic field study
│   ├── Need time-distributed behavior? → Diary study
│   ├── Need mental model / inner thinking? → Long-form behavioral interviews (Portigal) or
│   │                                          Mental model research (Indi Young)
│   ├── Need to know why they switched? → Switch interview (Moesta — see switch-interview-guide.md)
│   ├── Need to know what outcomes matter and how many? → ODI survey (Ulwick — see odi-ulwick.md)
│   └── Need strategic framing across many users? → Problem-space research → OST (Torres)
│
└── YES → What question do I have about the solution?
    ├── Can users accomplish the task? → Qualitative usability testing (≥5 per segment)
    ├── How many succeed? → Quantitative usability testing (≥30-40)
    ├── Which version performs better? → A/B testing
    ├── How do users navigate IA? → Tree testing, card sorting
    ├── Do users understand the concept? → Concept testing
    └── What do users think? → Survey (attitudinal, large n)

SYNTHESIS QUESTION:
├── Pile of raw observations → Affinity diagramming
├── Themes need root causes → Five Whys per theme
├── Data across time stages → Journey synthesis → journey map
└── Connect problem space to solution space → OST overlay
```

---

## 6. The "5 Users" Question — When It Holds and When It Doesn't

Jakob Nielsen's 1993 claim: qualitative usability testing with five participants identifies ~85% of usability problems.

**Holds when:**
- Study is qualitative (find problems to fix, not measure success rates)
- User group is relatively homogeneous (single, well-defined population)
- Goal is iterative formative testing — five users, fix what you find, five more
- Problems are discoverable within a single session

**Doesn't hold when:**
- Study is quantitative (need 30-40+ for statistical validity)
- Multiple user segments with different mental models (five per segment is the floor, not five total)
- Generative discovery (you can't discover what you don't know from five users)

**The misuse pattern:** "5 users" is routinely cited out of context to justify minimal research. It was an argument for iterative small tests over single large tests, not that five people is enough for any question.

---

## 7. Where Design Thinking Fits — and Its Limits

The Stanford d.school / IDEO five-stage process: **Empathize → Define → Ideate → Prototype → Test.**

**Strengths:** teachable to non-designers; cross-functional alignment; accessible artifacts; good for early-stage exploration.

**Documented criticisms** (from researchers and practitioners):
- **Innovation theater:** post-its accumulate; decisions don't change
- **Conservative by default:** privileges existing user contexts over questioning the systems that create them (HBR, 2018)
- **Process fetish:** clean five-stage model creates false impression that design is linear
- **Persona problem:** empathy methods often generate demographic personas, the same artifact Indi Young argues is actively harmful
- **Scalability gap:** good at idea generation; poor at moving from insights to organizational commitment

The plugin should treat design thinking as one option among many, not the default frame.

---

## 8. Cagan's Four Risks (Discovery vs. Delivery Frame)

Marty Cagan / SVPG: every product idea carries four risks that must be killed **before** significant engineering investment.

| Risk | Question | Owned by | Method |
|------|---------|----------|--------|
| **Value** | Will customers buy / use it? | PM | Customer research, demand testing, concierge MVP |
| **Usability** | Can users figure it out? | Designer | Usability testing, prototype walkthroughs |
| **Feasibility** | Can engineers build it? | Tech lead | Technical spikes, engineer involvement in discovery |
| **Business viability** | Does it work for legal, finance, sales, marketing, brand? | PM | Stakeholder review, constraint mapping |

**Discovery vs. delivery are separate activities:**
- Discovery uses prototypes — cheap, fast, disposable, designed to answer specific risk questions. A good discovery team tests 10-20 ideas per week.
- Delivery builds products — production-quality, scalable, reliable. Commitment to build follows only after discovery clears the four risks.

The pathology Cagan diagnoses: teams jump to delivery without discovery, then commission research retroactively to explain why something didn't work.

---

## Sources

- [NN/G — Which UX Research Methods](https://www.nngroup.com/articles/which-ux-research-methods/)
- [NN/G — Attitudinal vs. Behavioral](https://www.nngroup.com/articles/attitudinal-behavioral/)
- [NN/G — Contextual Inquiry](https://www.nngroup.com/articles/contextual-inquiry/)
- [NN/G — Affinity Diagram](https://www.nngroup.com/articles/affinity-diagram/)
- [NN/G — Why 5 Users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/)
- [Indi Young — Method](https://indiyoung.com/method/)
- [Portigal — Interviewing Users 2nd ed.](https://rosenfeldmedia.com/books/interviewing-users-second-edition/)
- [Teresa Torres — Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/)
- [SVPG — Four Big Risks](https://www.svpg.com/four-big-risks/)
- [Just Enough Research — Erika Hall](https://abookapart.com/products/just-enough-research)
- [HBR — Design Thinking Is Conservative](https://hbr.org/2018/09/design-thinking-is-fundamentally-conservative-and-preserves-the-status-quo)
