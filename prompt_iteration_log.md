# Prompt Iteration Log

## V1 — Baseline

**System prompt**

```
You are a meeting prep assistant. The user will provide a Notes PDF and a slide deck. Read them and produce a structured meeting preparation in the required JSON format. Include meeting summary, risks, talking points, next steps, and a cover image prompt.
```

**User message (in chat).** `Prepare me for this meeting.`

**Settings.** Gemini 3 Flash Preview · Thinking Low · Temp 1.0 · Structured output on · All tools off.

**Artifacts.** `prompts/v1.md`, `sample_outputs/v1.json`, `screens/ai_studio_v1.png`.

**What it caught.** All three planted tensions: CFO pricing pressure, SLA breach (48h vs 24h), internal instability (layoffs, low training attendance).

**What it missed.**
- Evidence fields paraphrase content instead of citing page/slide (e.g., no "Notes p.1" locators).
- Two of three contradictions ignored: roadmap vs CTO alignment (Slide 6 / Notes p.3), power-user growth claim vs layoffs (Slide 4 / Notes p.2).
- `why_it_lands` written from the user's POV, not the counterparty's.
- No adversarial reasoning — what a competitor would argue, what the notes' author failed to ask.

**Why V1 is already strong.** Thinking was Low, so inference-time compute is not the explanation. Two likely causes:
1. The schema carries prompt weight. Required fields (`why_it_lands`, `evidence`) force reasoning the instruction did not request. Structured-output prompting is a two-surface problem: instruction + schema.
2. The inputs are clean — explicit stakeholders, specific metrics, dated events. A noisier corpus would expose a weaker floor.

**Levers for V2 and V3.**
- V2: explicit citation format ("Notes p.X" / "Slide Y"), contradiction flagging as first-class output, counterparty POV in talking points.
- V3: adversarial check — competitor framing, blind spots in the source, what would have to be true for the deal to fall through.

---

## V2 — Grounding and role specificity

**System prompt**

```
You are a meeting prep co-pilot for an account manager at a B2B SaaS vendor. The user is preparing for a client meeting and will provide a Notes PDF (internal account notes) and a slide deck (the customer-facing deck). Produce a structured meeting preparation in the required JSON format.

Grounding rules (strict):
1. Every `evidence` field MUST cite a specific source locator, formatted as "Notes p.N" or "Slide N" (e.g., "Notes p.3", "Slide 5"). Paraphrases of content without a locator are not valid evidence.
2. If a claim cannot be traced to a specific page or slide in the provided documents, do not include it. Omit rather than infer.
3. When the Notes PDF and the slide deck contradict each other, treat the contradiction itself as a High-severity risk. Name both sources in the evidence field (e.g., "Notes p.2 vs Slide 4").

Role and perspective:
- Write `talking_points[].why_it_lands` from the counterparty's perspective, not the user's. Name the specific stakeholder. Do not use "we" framing in this field.
- `mitigation` fields should specify concrete actions the account manager can take before or during the meeting, not vague postures.
- `next_steps[].owner` must be specific: name an individual, not "the team" or "both sides".
```

**User message (in chat).** `Prepare me for this meeting.`

**Settings.** Identical to V1 — Gemini 3 Flash Preview · Thinking Low · Temp 1.0 · Structured output on · All tools off. Token count: 8,586.

**Diff vs V1.** Thin generic assistant → constrained co-pilot with citation format, contradiction policy, counterparty-POV rule, owner specificity.

**Artifacts.** `prompts/v2.md`, `sample_outputs/v2.json`, `screens/ai_studio_v2.png`.

**What it caught.**
- Citation format: 7/7 evidence fields correctly formatted as "Notes p.N" / "Slide N". Spot-check: all 7 locators point to the right page/slide. No hallucinated citations.
- One contradiction flagged as dual-source High risk: SLA 48h vs 18h ("Notes p.2 vs Slide 5"). Instruction #3 worked on the most explicit numeric contradiction.
- Counterparty POV: 3/3 `why_it_lands` fields lead with "For Elena as CFO..." / "For Marcus as CTO..." — named stakeholders, no "we" framing.
- Owners: all three `next_steps[].owner` = "Account Manager". Specific per the rule.

**What it still missed.**
- Only 1 of 3 planted contradictions promoted to a risk. Still absent: power-user growth celebration (Slide 4) vs Feb layoffs (Notes p.2); "shared roadmap" framing (Slide 6) vs CTO never having seen the roadmap (Notes p.3).
- Worse — the CTO-roadmap tension was surfaced *as a talking point to show Marcus* ("For Marcus as CTO, seeing 'Advanced anomaly detection'... demonstrates that the vendor is innovating ahead of their internal data science team's current capacity"). That framing is exactly what the notes warn against. The model weaponized the landmine instead of defusing it.
- No adversarial reasoning: no competitor framing, no pre-mortem, no surfacing of what the AM's notes failed to ask (custom data export re-deferred, SOC 2 still open, calendar-title change unexplained).

**New issue introduced.**
- All three `next_steps[].deadline` values are fabricated dates (2026-04-12, 04-15, 04-10). The source documents specify no such deadlines. The schema permits `"TBD in meeting"` as a fallback but the instruction doesn't route to it. Date fabrication is a specific failure mode of specificity pressure without a nullability clause.

**Why V2 cleared citations but missed two contradictions.** Instruction #3 activates on surface-level numeric mismatches (48h vs 18h — arithmetic). Narrative mismatches (a celebration tone vs a contradicting fact on a different page; a framing claim vs an absence) require the model to read between pages, not just compare values. Pattern-matched contradiction detection ≠ contradictory-claim inference.

**Levers for V3.**
- Adversarial check: "what would a competitor like Snowflake or Databricks argue to displace us?" → forces competitive framing.
- Blind-spot check: "what question did the AM's notes fail to ask?" → surfaces deferred items as talking points.
- Pre-mortem: "what would have to be true for this deal to fall through in 90 days?" → directly addresses the narrative contradictions V2 missed.
- Deadline-fabrication fix: "if a date is not in the source documents, use 'TBD in meeting'". Closes the V2 regression.
- Optional: run V3 on Gemini Pro (not Flash) to produce the model-trade-offs finding required by the reflection section.

---

## V3 — Reasoning constraints and adversarial check

**System prompt** (deltas over V2 only; full prompt in `prompts/v3.md`)

```
Grounding rule #3 broadened:
"...when the Notes PDF and the slide deck contradict each other — including framing or tone mismatches, not just numeric ones — treat the contradiction itself as a High-severity risk."

Deadline clause added:
"next_steps[].deadline is either a specific date taken directly from the source documents or the string 'TBD in meeting' — never a fabricated date."

Reasoning constraints (mandatory before responding):
4. Pre-mortem: 'What would have to be true for this deal to fall through in the next 90 days?' Any supported condition → High-severity risk.
5. Adversarial check: what would a competing vendor (e.g., Snowflake, Databricks, or a competitor referenced in the notes) argue to displace us? → risk with mitigation.
6. Blind-spot check: identify at least one question the notes failed to ask. Surface as a talking point with angle = "Question to ask".
```

**User message (in chat).** `Prepare me for this meeting.`

**Settings.** Identical to V1/V2 — Gemini 3 Flash Preview · Thinking Low · Temp 1.0 · Structured output on · All tools off. Token count: 9,501.

**Diff vs V2.** V2 was grounded and counterparty-aware but reactive. V3 forces three explicit reasoning loops (pre-mortem, adversarial, blind-spot) and fixes the V2 deadline-fabrication regression.

**Artifacts.** `prompts/v3.md`, `sample_outputs/v3.json`, `screens/ai_studio_v3.png`.

**What it caught.**
- Adversarial lever fired cleanly. New High-severity risk "Vendor Displacement via Competitor X" (Notes p.3) with a concrete mitigation tying Slide 6's roadmap to Acme's EMEA + healthcare expansion as a switching-cost argument. This risk did not exist in V1 or V2.
- Blind-spot lever fired. Third talking point uses `angle: "Question to ask"` exactly as instructed — the AM asking Dev Patel about the Native LLM roadmap as a force-multiplier given the Feb layoffs.
- Deadline fix worked. All three `next_steps[].deadline` = `"TBD in meeting"`. V2 regression closed.
- Grounding, citations, and counterparty POV all maintained. No regression on earlier wins.

**What it still missed (the ceiling).**
- **The CTO-roadmap contradiction is still absent.** Notes p.3 is explicit that Marcus has never seen the 2026 roadmap, but Slide 6 ("Shared roadmap: building the next phase together") presents it as aligned. V3's pre-mortem lever did not flag this — arguably the single biggest landmine for the live meeting. The model's pre-mortem reasoning found competitive and pricing failure modes but not stakeholder-alignment failure modes.
- **The growth-vs-layoffs tension was reframed, not flagged.** V3 surfaced it as a *positive* talking point ("Growth Despite Headcount Contraction" — Slide 3 + Notes p.2) rather than as a contradiction risk. Dual-source evidence format used, but severity inverted from risk to sales pitch. The broadened rule #3 ("framing/tone mismatches") didn't override the sales instinct.
- Blind-spot check surfaced one question (the Dev Patel one) but missed richer candidates: what is the Competitor X conversation actually about, who added "+ roadmap" to the invite title, is SOC 2 Type II still required. Technically meets "at least one" but leaves yield on the table.

**Why V3 found competitive landmines but not internal ones.** Hypothesis: the example list in rule #5 ("e.g., Snowflake, Databricks, or a competitor referenced in the notes") anchored the model on *external* adversaries. Rule #4's pre-mortem was more open-ended but the model appears to have treated it as "a second adversarial pass" rather than "a stakeholder-misalignment pass". Named examples teach by pattern — they also constrain by pattern.

**The structural finding.** Prompt engineering on a clean schema closes evidence hygiene, role framing, and competitive framing efficiently. It partially closes contradiction detection (numeric: yes; narrative: yes; stakeholder-alignment: no). A fourth iteration with stakeholder-level pre-mortem examples would likely close the CTO-roadmap gap — but the marginal prompt instruction required to hit every such case suggests a different architecture: retrieval + targeted re-prompts over a single long system prompt. That's a reflection-section finding, not a V4 recipe.

**Settings note for reflection.** All three iterations held Thinking = Low. This was deliberate — it isolates the prompt as the varying input, and V1 already showed strong baseline behavior without thinking-time compute. Running Thinking High on the V3 prompt would be a fourth experiment, not a fourth iteration.
