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

**Why V1 is already strong.** Thinking was Low, so inference-time compute is unlikely to be the main explanation. Two plausible contributors:
1. The schema carries prompt weight. Required fields (`why_it_lands`, `evidence`) appear to elicit reasoning the instruction did not explicitly request. Structured-output prompting seems to be a two-surface problem: instruction + schema.
2. The inputs are relatively clean — explicit stakeholders, specific metrics, dated events. A noisier corpus would probably expose a weaker floor.

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
- Citation format: 7/7 evidence fields correctly formatted as "Notes p.N" / "Slide N". Spot-check: all 7 locators point to the right page/slide. No hallucinated citations in this sample.
- One contradiction flagged as a dual-source High risk: SLA 48h vs 18h ("Notes p.2 vs Slide 5"). Instruction #3 appears to have worked on the most explicit numeric contradiction.
- Counterparty POV: 3/3 `why_it_lands` fields lead with "For Elena as CFO..." / "For Marcus as CTO..." — named stakeholders, no "we" framing.
- Owners: all three `next_steps[].owner` = "Account Manager". Specific per the rule.

**What it still missed.**
- Only 1 of 3 planted contradictions was promoted to a risk. Still absent: power-user growth celebration (Slide 4) vs Feb layoffs (Notes p.2); "shared roadmap" framing (Slide 6) vs CTO never having seen the roadmap (Notes p.3).
- Notably, the CTO-roadmap tension was surfaced *as a talking point to present to Marcus* ("For Marcus as CTO, seeing 'Advanced anomaly detection'... demonstrates that the vendor is innovating ahead of their internal data science team's current capacity"). That framing sits uneasily alongside what the notes flag — the talking point tees up the landmine rather than defusing it.
- No adversarial reasoning: no competitor framing, no pre-mortem, no surfacing of what the AM's notes failed to ask (custom data export re-deferred, SOC 2 still open, calendar-title change unexplained).

**New issue introduced.**
- All three `next_steps[].deadline` values are fabricated dates (2026-04-12, 04-15, 04-10). The source documents specify no such deadlines. The schema permits `"TBD in meeting"` as a fallback, but the instruction does not route to it. In this run, specificity pressure without an explicit nullability clause produced fabricated dates — a regression worth calling out.

**Interpretation.** Instruction #3 appears to activate most reliably on surface-level numeric mismatches (48h vs 18h — arithmetic). Narrative mismatches (celebration tone vs a contradicting fact on a different page; a framing claim vs an absence) seem to require cross-page inference rather than value comparison. The pattern observed here: contradiction *detection* is easier to elicit than contradictory-claim *inference*.

**Levers for V3.**
- Adversarial check: "what would a competitor like Snowflake or Databricks argue to displace us?" → forces competitive framing.
- Blind-spot check: "what question did the AM's notes fail to ask?" → surfaces deferred items as talking points.
- Pre-mortem: "what would have to be true for this deal to fall through in 90 days?" → intended to address the narrative contradictions V2 missed.
- Deadline-fabrication fix: "if a date is not in the source documents, use 'TBD in meeting'". Aimed at closing the V2 regression.
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

**Diff vs V2.** V2 was grounded and counterparty-aware but reactive. V3 adds three explicit reasoning loops (pre-mortem, adversarial, blind-spot) and addresses the V2 deadline-fabrication regression.

**Artifacts.** `prompts/v3.md`, `sample_outputs/v3.json`, `screens/ai_studio_v3.png`.

**What it caught.**
- Adversarial lever appears to have fired cleanly. New High-severity risk "Vendor Displacement via Competitor X" (Notes p.3) with a concrete mitigation tying Slide 6's roadmap to Acme's EMEA + healthcare expansion as a switching-cost argument. This risk did not surface in V1 or V2.
- Blind-spot lever fired. Third talking point uses `angle: "Question to ask"` as instructed — the AM asking Dev Patel about the Native LLM roadmap as a force-multiplier given the Feb layoffs.
- Deadline fix worked in this run. All three `next_steps[].deadline` = `"TBD in meeting"`. V2 regression closed.
- Grounding, citations, and counterparty POV maintained. No regression on earlier wins.

**What it still missed (the apparent ceiling).**
- **The CTO-roadmap contradiction is still absent.** Notes p.3 is explicit that Marcus has never seen the 2026 roadmap, but Slide 6 ("Shared roadmap: building the next phase together") presents it as aligned. V3's pre-mortem lever did not flag this in this run. It is plausibly the most consequential landmine for the live meeting; the pre-mortem reasoning appears to have favoured competitive and pricing failure modes over stakeholder-alignment ones.
- **The growth-vs-layoffs tension was reframed, not flagged.** V3 surfaced it as a *positive* talking point ("Growth Despite Headcount Contraction" — Slide 3 + Notes p.2) rather than as a contradiction risk. The dual-source evidence format was used, but the framing was promotional rather than risk-oriented. The broadened rule #3 ("framing/tone mismatches") did not, in this run, redirect the model away from a promotional framing.
- Blind-spot check surfaced one question (the Dev Patel one) but missed richer candidates: what is the Competitor X conversation actually about, who added "+ roadmap" to the invite title, is SOC 2 Type II still required. Technically meets "at least one" but leaves yield on the table.

**Interpretation of the asymmetry.** One hypothesis: the example list in rule #5 ("e.g., Snowflake, Databricks, or a competitor referenced in the notes") may have anchored the model on *external* adversaries. Rule #4's pre-mortem was more open-ended, but the output reads as though it was treated as a second adversarial pass rather than a stakeholder-misalignment pass. Named examples appear to teach by pattern — and, on this evidence, also constrain by pattern.

**A tentative structural reading.** Prompt engineering on a clean schema appeared to close evidence hygiene, role framing, and competitive framing efficiently. Contradiction detection was partial — reliable on numeric and narrative mismatches, less reliable on stakeholder-alignment ones. A fourth iteration with stakeholder-level pre-mortem examples would probably narrow the CTO-roadmap gap further. The volume of prompt instruction required to hit every such case points to an open question for productionisation: whether a different architecture (retrieval plus targeted re-prompts) might scale better than a single long system prompt. Material for the reflection section, not a V4 recipe.

**Settings note for reflection.** All three iterations held Thinking = Low. This was deliberate — it isolates the prompt as the varying input, and V1 already showed strong baseline behaviour without thinking-time compute. Running Thinking High on the V3 prompt would be a fourth experiment rather than a fourth iteration.

---

## V3 sweep — thinking-level and model trade-offs

Two additional runs on the **V3 system prompt (unchanged)** and the **same inputs**, to isolate two variables separately.

- **V3 Flash-High.** Gemini 3 Flash Preview, Thinking **High**. Fresh chat.
- **V3 Pro-High.** Gemini **3.1 Pro Preview**, Thinking High. Fresh chat.

Both runs were started as new chats (not branched) to limit prior-turn context pollution from the V1/V2/V3 branched lineage. The token counts below are consistent with this — V3-Low's 9,501 appears to include V1+V2 branch history, whereas V3 Flash-High's 6,478 more closely reflects the cost of a single V3 exchange.

| Run | Model | Thinking | Tokens | CTO-roadmap risk | Growth-vs-layoffs tension | Pricing framing |
|---|---|---|---|---|---|---|
| V3-Low | Flash | Low | 9,501 (branched) | **Missed** | Reframed as positive talking point | Single pricing-pressure risk |
| V3 Flash-High | Flash | High | 6,478 (fresh) | Caught at **Medium**, soft mitigation | Still reframed as positive | Combined with competitor risk |
| V3 Pro-High | Pro | High | 9,984 (fresh) | Caught at **High**, sharp mitigation | Reframed as *clarification question* (diagnostic, not promotional) | Framed as slide-notes **contradiction** (Notes p.3 vs Slide 7) |

**Artifacts.** `prompts/v3_flash_high.md`, `prompts/v3_pro_high.md`, `sample_outputs/v3_flash_high.json`, `sample_outputs/v3_pro_high.json`, `screens/ai_studio_v3_flash_high.png`, `screens/ai_studio_v3_pro_high.png`.

**Flash-High vs Flash-Low — what High thinking appears to add on the same model.**
- *Partial close on CTO-roadmap.* Flash-High flags the roadmap-alignment risk, but at Medium severity and with a mitigation that reads as defensive ("briefly pause before presenting Slide 6 to ask Marcus if H1 priorities align"). The risk is acknowledged; it is not fully defused.
- *Little change on the growth-vs-layoffs framing.* Flash-High still routes the tension into a positive talking point ("Dev needs to show his team is delivering more output with 3 fewer heads"). In this run, additional thinking time did not change the promotional framing.
- *Minor regression.* `next_steps[1].owner` = "Sarah Chen" (the counterparty), not "Account Manager". The V3 prompt requires an individual owner but not specifically the AM, so the output is technically compliant. It does, however, move the accountability outside the user — worth watching.

**Pro-High vs Flash-High — what the larger model appears to add at identical thinking level.**
- *CTO-roadmap landmine caught at High severity.* Pro-High flags this as High, with a concrete mitigation that aims to defuse the landmine in the room: "Frame Slide 6 verbally as a 'draft roadmap for CTO input' rather than a finalized plan. Give Marcus the floor immediately after presenting the slide." This was the most visible behavioural gap we observed between Flash and Pro on this task.
- *Growth-vs-layoffs reframed as a diagnostic question.* Pro surfaces the tension as a `Clarification` talking point: "Dev needs to understand if his remaining, smaller team is simply working heavier hours to inflate these metrics, or if self-serve capabilities are genuinely expanding to other departments." The output reads as reasoning about what the metric actually measures, rather than asserting a direction.
- *Pricing framed as a true contradiction.* Pro appears to apply rule #3 more broadly, flagging the 3-year flat-rate proposal (Slide 7) as a contradiction to Elena's documented usage-based-pricing ask (Notes p.3) — with a mitigation that instructs the AM to bring the usage-based comparison and be ready to pivot.
- *Causal reasoning across notes pages.* Pro connects the competitor threat (Notes p.3) to the repeatedly-delayed custom data export (Notes p.2) — "they can leverage the vendor's unresponsiveness... to steal the account." Flash treats these as separate risks; Pro articulates why one is material *because of* the other.
- *Mitigations tended to be multi-step.* Pro frequently produced two-clause mitigations ("Position X as anchor... but be prepared to pivot to Y if Z"); Flash's mitigations in this run were predominantly single-step.

**What the sweep suggests for model selection.**
- In our runs, prompt engineering on a clean schema closed citation hygiene, role framing, and competitive framing well. Narrative and stakeholder-alignment contradictions were closed less consistently.
- Adding thinking time to Flash narrowed the gap on the CTO-roadmap risk, but did not alter the promotional framing of the growth-vs-layoffs tension.
- Pro-High closed the remaining gap in this sample — the CTO-roadmap landmine, arguably the most consequential risk for the live meeting, was caught at High severity with a concrete mitigation.
- The ~54% token overhead of Pro-High (9,984) over Flash-High (6,478) on the same task is readily justifiable for a single high-stakes meeting prep. At high-volume batch scale, the trade-off looks less favourable, and a routed architecture (Flash by default, Pro on flagged deals) would be worth exploring.

**Two findings worth carrying into the reflection.**
1. **Prompt engineering is a necessary but, on its own, incomplete lever** for tasks requiring cross-document narrative inference. Model capacity appears to matter materially here. Further prompt work could narrow the gap — how much is an open question — but fully compensating on the hardest contradictions via prompt alone looks unlikely on this evidence.
2. **Branched chats can leak context into what are meant to be clean experiments.** The token delta (9,501 → 6,478 on an identical V3 prompt) is consistent with the V1+V2 turns being carried in the V3-Low context. For model-behaviour comparisons that hinge on a single varying input, fresh chats look like the more defensible protocol.
