# Meeting Prep Assistant — OxAI AI Studio Assignment

## Table of Contents
- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. Design decisions](#3-design-decisions)
- [4. Prompt engineering](#4-prompt-engineering)
- [5. UX design](#5-ux-design)
- [6. Reflection](#6-reflection)

---

## 1. Overview

A production-intent Meeting Prep Assistant built on Google AI Studio (Gemini 3.1 Pro Preview) with a two-screen UI generated in Stitch. Given a Notes PDF (internal account notes) and a slide deck (the customer-facing QBR deck), the Gem returns structured meeting intelligence — summary, risks, talking points, next steps, cover-image prompt — with every claim cited back to the source.

**Scope is locked to two screens** (Landing / Upload and Synthesis / Results) per [`spec.md`](spec.md). Everything else — dashboards, history, analytics, tabbed detail views — is explicitly out of scope and was trimmed out of the repo after being produced as Stitch workflow evidence.

**Headline finding.** Three prompt iterations (V1 → V2 → V3) held model, thinking level, and temperature constant so the prompt was the only varying input. A follow-up sweep varied thinking level and model on the V3 prompt. V3 on Gemini 3.1 Pro with Thinking High caught all three planted contradictions in the test inputs, including the single most consequential landmine (a CTO being blindsided by an unaligned roadmap). V3 on Flash with the same prompt and Thinking Low caught only one. The conclusion is written up in section 4 — prompt engineering reliably closes evidence hygiene, role framing, and competitive framing; model capacity matters materially for stakeholder-alignment contradictions.

**Assignment brief.** [`Google_AI_Studio_Assignment_Detailed.pdf`](Google_AI_Studio_Assignment_Detailed.pdf) (Oxford edition, graded Complete / Not Complete).

**Repository.** [`JR-00X/oxai-ai-studio-meeting-prep`](https://github.com/JR-00X/oxai-ai-studio-meeting-prep) on GitHub. Every artefact referenced in this document is committed to `main`.

**Live deployment (optional bonus).** The app is deployed on Google Cloud Run:
**https://meeting-prep-assistant-691081429886.us-west1.run.app**

> ⚠️ **Stability notice.** The deployed app is not fully optimised — known issues are catalogued in [`qa/stress_test_2026-04-19.md`](qa/stress_test_2026-04-19.md) and addressed in section 6. Errors may occasionally appear during generation; if that happens please **retry once** (the second attempt usually completes). If the second retry also fails, please contact me at **contact@example.com**.

---

## 2. Architecture

Two user inputs → one Gem → one JSON contract → two screens. Nothing else.

```
┌────────────────────────────┐
│      Landing (Upload)      │   User attaches notes.pdf + slides.pdf
│      screens/01-upload.png │
└──────────────┬─────────────┘
               │ files + user message
               ▼
┌──────────────────────────────────────────────────────┐
│            AI Studio Gem — "Meeting Prep"            │
│  Gemini 3.1 Pro Preview · Thinking High · Temp 1.0   │
│  System prompt: prompts/v3.md (also inlined in spec) │
│  Structured output: schema/output_schema.json        │
│  All external tools disabled                         │
└──────────────┬───────────────────────────────────────┘
               │ JSON conforming to the schema
               ▼
┌────────────────────────────┐
│    Synthesis (Results)     │   Single scrollable page, rendered
│    screens/02-synthesis.png│   top to bottom. "+ New briefing"
└────────────────────────────┘   returns to Landing.
```

**Repository layout** (only what the grader needs to navigate):

```
.
├── Google_AI_Studio_Assignment_Detailed.pdf   Assignment brief
├── spec.md                                     Product scope lock + inlined system prompt + API wiring
├── assignment.md                               This document
├── prompt_iteration_log.md                     V1→V2→V3 diff, diagnosis, and Flash/Pro sweep
├── prompts/
│   ├── v1.md / v2.md / v3.md                   The three iterations (full system prompt + run settings each)
│   └── v3_flash_high.md / v3_pro_high.md       Sweep variants
├── sample_inputs/
│   ├── notes.pdf                               Fictional Acme Corp internal notes (3 pages)
│   ├── slides.pptx / slides.pdf                Fictional Acme Corp QBR deck (8 slides)
│   └── README.md                               Scenario + designed contradictions
├── sample_outputs/
│   ├── v1.json / v2.json / v3.json             Gem outputs per iteration
│   └── v3_flash_high.json / v3_pro_high.json   Sweep outputs
├── schema/
│   ├── output_schema.json                      The JSON contract
│   └── README.md                               Schema design rationale
├── screens/
│   ├── 01-upload.png / .html                   Canonical Landing screen
│   ├── 02-synthesis.png / .html                Canonical Synthesis screen
│   └── ai_studio_v1..v3_pro_high.png           AI Studio version-history screenshots
└── scripts/
    ├── build_notes_pdf.py                      Reproducible notes generator
    └── build_slides_pptx.py / build_slides_pdf.py   Reproducible deck generators
```

---

## 3. Design decisions

### Schema shape forces behaviour the prompt does not have to re-request

The contract in [`schema/output_schema.json`](schema/output_schema.json) is the first line of defence. Four choices matter (rationale expanded in [`schema/README.md`](schema/README.md)):

- **Required `evidence` on every risk and talking point.** Locator or omission — no paraphrase. This is the single strongest grounding lever available without RAG.
- **`severity` as an enum** (`High | Medium | Low`). Collapses unbounded adjective drift ("moderate", "elevated") into a triageable field.
- **Three-part `meeting_summary`** (`context` / `headline` / `participant_snapshot`). Splits a single blob into three unavoidable commitments; the headline in particular forces a one-sentence stance.
- **`why_it_lands` on every talking point.** The dialectical check — the model has to reason about the counterparty, not the user.

A finding from V1: structured-output prompting is a two-surface problem. The V1 instruction was deliberately thin, yet V1 still produced counterparty-oriented reasoning and severity triage — because the schema's required fields did the work. The instruction and the schema both carry prompt weight.

### Two screens — everything else is out of scope

[`spec.md`](spec.md) locks the product to Landing and Synthesis, with a single "+ New briefing" button as the only control back to Landing. No persistence, no accounts, no dashboard, no history, no analytics. The broader product surface (Dashboard, History, Analytics, detail tabs, mitigation views) was produced in Stitch as workflow evidence, then trimmed from the repo. The reasoning: the assignment brief does not call for those surfaces, and carrying them forward as "kind-of deliverables" would have blurred what is being evaluated.

### Isolation protocol for the iteration experiment

The V1 → V2 → V3 lineage holds model, thinking level, temperature, and structured-output settings constant. The prompt is the only varying input. This matters because many prompt-engineering write-ups confound two things — "my prompt got better" and "I also bumped the model" — and produce findings that are un-attributable.

For the Flash/Pro sweep (section 4), the protocol goes further: the Flash-High and Pro-High runs were started as **fresh chats**, not branches. A branched chat preserves the prior conversation turns in context, which both behaviourally and economically pollutes the comparison. The token-count delta (9,501 on the branched V3-Low vs 6,478 on the fresh V3 Flash-High, identical prompt) quantifies the pollution.

### Test inputs with planted contradictions

The fictional Acme Corp QBR (see [`sample_inputs/README.md`](sample_inputs/README.md)) contains three deliberate contradictions between the Notes PDF and the slide deck, plus several softer signals that require reading between the lines. These are the test terrain — the whole point of iterating the prompt is to see which ones the model surfaces and at what severity.

| # | Contradiction | Source locators |
|---|---|---|
| 1 | SLA breach — deck claims 18h avg ticket resolution; notes record 48h on recent P1s (SLA is 24h) | Notes p.2 vs Slide 5 |
| 2 | Growth celebration vs headcount cuts — deck celebrates +12% MAU growth; notes record Feb layoffs of Dev Patel's data science team | Notes p.2 vs Slide 4 |
| 3 | Shared-roadmap framing vs CTO never having seen it — deck uses "Shared roadmap: building the next phase together"; notes record Marcus has never been shown the roadmap slide | Notes p.3 vs Slide 6 |

Each contradiction tests a different kind of inference — numeric comparison, celebration-vs-fact narrative, and stakeholder-alignment framing — and the three iterations plus the sweep produce measurably different behaviour on each.

---

## 4. Prompt engineering

Three iterations, one sweep, one conclusion. Full diffs, outputs, and run-by-run diagnoses in [`prompt_iteration_log.md`](prompt_iteration_log.md).

### V1 — Baseline

Thin generic instruction: *"You are a meeting prep assistant. Read [the files] and produce a structured meeting preparation in the required JSON format."* No grounding rule, no role, no reasoning constraint. Purpose: establish a floor.

**Result.** All three planted tensions surfaced at some level. But evidence fields paraphrased content instead of citing page/slide; two of three contradictions were not flagged as risks; `why_it_lands` was written from the user's POV, not the counterparty's; no adversarial reasoning at all.

**Why V1 was already strong.** The schema's required fields carry prompt weight on their own.

### V2 — Grounding and role specificity

Three levers stacked on the thin baseline:

1. Citation format enforced — `Notes p.N` / `Slide N`, no paraphrase permitted.
2. Contradictions promoted to first-class risks with dual-source evidence format (`Notes p.2 vs Slide 4`).
3. Counterparty POV for `why_it_lands`, named stakeholders, no "we" framing.

**Result.** 7/7 evidence fields correctly formatted with no hallucinated locators. 3/3 `why_it_lands` fields from counterparty POV with named stakeholders. One contradiction (SLA 48h vs 18h) promoted to High risk with dual-source evidence. But two of three contradictions still missed — including the CTO-roadmap tension, which V2 actually surfaced *as a talking point to present to Marcus*, reading as a landmine tee-up rather than a defusal. V2 also introduced a deadline-fabrication regression (three invented dates).

### V3 — Reasoning constraints and adversarial check

Three numbered reasoning constraints stacked on V2's grounding and role rules:

4. Pre-mortem: *"What would have to be true for this deal to fall through in the next 90 days?"*
5. Adversarial check: *"What would a competing vendor argue to displace us?"*
6. Blind-spot check: *"What question did the notes fail to ask?"* → surface as a talking point with angle = "Question to ask".

Plus a deadline-fabrication fix: `"TBD in meeting"` as the explicit fallback when a date is not in the source.

**Result.** Adversarial lever fired cleanly — new High-severity Competitor X displacement risk with a concrete switching-cost mitigation. Blind-spot lever fired — the "Question to ask" angle appeared exactly as instructed. Deadline fix closed the V2 regression. No regression on citation format, counterparty POV, or mitigation specificity.

**Ceiling.** The CTO-roadmap contradiction was still absent. The growth-vs-layoffs tension was reframed as a *positive* talking point rather than as a risk. V3's pre-mortem lever appeared to have been interpreted as a second adversarial pass rather than a stakeholder-alignment pass. A plausible explanation: the named examples in rule #5 ("e.g., Snowflake, Databricks, or a competitor referenced in the notes") anchored the model on external adversaries.

### V3 sweep — thinking-level and model trade-offs

Same V3 prompt, same inputs, two additional runs. Both started as fresh chats to isolate the varying input.

| Run | Model | Thinking | Tokens | CTO-roadmap landmine | Growth-vs-layoffs tension | Pricing framing |
|---|---|---|---|---|---|---|
| V3-Low | Flash | Low | 9,501 (branched — context-polluted) | **Missed** | Reframed as positive talking point | Single pricing-pressure risk |
| V3 Flash-High | Flash | High | 6,478 (fresh) | Caught at **Medium**, soft mitigation | Still reframed as positive | Combined with competitor risk |
| V3 Pro-High | Pro | High | 9,984 (fresh) | Caught at **High**, sharp mitigation | Reframed as a *clarification question* — diagnostic, not promotional | Framed as a slide-notes **contradiction** (Notes p.3 vs Slide 7) |

### What the sweep suggests

Prompt engineering reliably closes citation hygiene, role framing, and competitive framing on this task. Narrative and stakeholder-alignment contradictions were closed less consistently — adding thinking time to Flash narrowed the gap but did not change the model's promotional framing instinct on the growth-vs-layoffs story; switching to Pro closed the remaining gap in our sample. Pro also produced multi-step mitigations and reasoned about causal connections across notes pages (linking the Competitor X threat to the repeatedly-delayed integration ask), where Flash treated those as separate risks.

The ~54% token overhead of Pro-High vs Flash-High is readily justifiable for a single high-stakes meeting prep. At batch scale a routed architecture (Flash by default, Pro on flagged deals) is the natural production answer.

---

## 5. UX design

Two canonical Stitch-generated screens, in [`screens/`](screens/).

### Landing (Upload) — [`screens/01-upload.png`](screens/01-upload.png)

Single page, no sidebar. Top bar is a spaced-caps "MEETING PREP" wordmark on the left and a small avatar on the right. Centered hero headline "Prepare for your next meeting in 30 seconds." A unified dashed drop zone accepts PDF / DOCX / PPTX, up to 50 MB. Optional collapsible "Meeting context" section for meeting title and date. Primary CTA "Prepare my meeting" is disabled until both files are attached. A reassurance line below the CTA notes documents are processed for this session only and are not retained. When the CTA is clicked, loading is handled in-place with a four-stage progress indicator — the page does not navigate away.

### Synthesis (Results) — [`screens/02-synthesis.png`](screens/02-synthesis.png)

Single scrollable page, top-right **"+ New Briefing"** button as the only control back to Landing. Rendered top to bottom:

- **Meeting summary** — oversized navy headline quote, a small-caps gold "CONTEXT" label with the context paragraph, and a "Key Participants" row showing stakeholder cards with avatar, name, role, and one-line stance.
- **Risks** — vertical stack of cards. Each card has a severity pill, the risk title, a "Mitigation Strategy" labelled paragraph, and an evidence chip at the bottom ("Usage Report p.12", "Jenkins Email 03/02", etc. in the demo content).
- **Talking Points** — cards with an angle pill at top-left ("Value Validation", "Future-Proofing"), the topic quote, a "Why it lands" block, and evidence chips at the bottom.
- **Next Steps** — checklist rows with checkbox, action title, owner and deadline chips.

### Stitch generation workflow (finding for the reflection)

Three approaches were attempted, in order, each building on what the previous one revealed. The evolution is itself a finding.

1. **Three focused briefs, one screen each** — produced clean, on-brand outputs that anchored the visual system for the rest of the project.
2. **One comprehensive one-shot brief covering all nine screens** (the broader product surface, pre-scope-lock) — failed. Screens drifted aesthetically despite shared design tokens, and information density dropped. Not the right abstraction for Stitch's current workflow.
3. **"Imagine a new screen" from the Results canvas** — Stitch's feature for branching from an existing screen. Selecting a button inside the Results screen and asking it to imagine the target screen produced the strongest outputs of the three approaches, because the source-screen context (sidebar, color tokens, typography, chrome) is carried forward automatically.

The pattern: Stitch works best when asked to branch from an existing frame and vary one thing, which mirrors how a human designer actually works. A single comprehensive brief is legible to a human reviewer but appears to exceed Stitch's single-generation working memory. This is reflection material (section 6).

After the scope was locked to two screens, the broader exploration was trimmed. The full set (nine Stitch outputs plus variants) is preserved in git history at commit `c4d9dda` for anyone inspecting the UX workflow evidence behind the reflection.

---

## 6. Reflection

(≤ 800 words.)

### How did the prompt evolve across iterations?

Each iteration closed an easier class of failure and revealed a harder one. V1 was deliberately thin — generic instruction, no grounding, no role, no reasoning constraint. It still produced counterparty-oriented reasoning and severity triage, because the schema's required fields (`evidence`, `severity`, `why_it_lands`) carry prompt weight on their own. The first finding was structural: structured-output prompting is a two-surface problem — the instruction *and* the schema both teach the model what to do.

V2 added grounding rules (citation format, contradictions as first-class risks), counterparty-POV framing, and owner specificity. It closed citation hygiene cleanly (7/7 evidence fields correctly formatted, all locators correct) and shifted talking points to named-stakeholder framing. But it also caught only one of three planted contradictions, surfaced the CTO-roadmap landmine *as a talking point to present to the CTO* (the inverse of what was needed), and introduced a deadline-fabrication regression — three invented dates appearing where the source had none.

V3 stacked three reasoning constraints: a pre-mortem ("what would have to be true for this deal to fall through?"), an adversarial check, and a blind-spot check that routed unasked questions into talking points with a dedicated angle. Plus an explicit `"TBD in meeting"` fallback to close the V2 deadline regression. The adversarial and blind-spot levers fired cleanly. The pre-mortem partially fired — the CTO-roadmap contradiction stayed missed, and the growth-vs-layoffs tension was reframed as a *positive* talking point rather than a risk. The pattern: prompt levers reliably close pattern-matchable behaviour (formats, framings, presence-of-X) and unreliably close cross-document narrative inference.

### What model-selection trade-offs did you observe?

The Flash-vs-Pro sweep on the V3 prompt produced the assignment's clearest finding. Flash with Thinking Low caught one of three contradictions; Flash with Thinking High caught two (including the CTO-roadmap landmine, but at Medium severity with a soft mitigation); Pro with Thinking High caught all three at the right severity, with multi-step mitigations, and reasoned about causal connections across pages — linking the Competitor X threat to the repeatedly-deferred integration ask, where Flash treated those as separate risks. Pro also reframed the growth-vs-layoffs tension as a *clarification* question (epistemic, asking what the metric actually measures) rather than a sales pitch.

Pro carries roughly 54% token overhead over Flash-High on the same task. For a single high-stakes meeting prep, that overhead is trivially justified. For batch use cases the trade-off looks less favourable, and the natural production answer is a routed architecture — Flash by default, Pro on flagged deals — not Pro everywhere.

A second, quieter finding from the sweep: branched chats leak context into experiments meant to be clean. The 9,501 → 6,478 token delta on an identical V3 prompt is consistent with the V1 + V2 turns being carried in the V3-Low context. For any model-behaviour comparison hinging on a single varying input, fresh chats are the more defensible protocol.

### How did Stitch accelerate or constrain UX design?

Three approaches were tried, in order. Three focused per-screen briefs anchored the visual system cleanly. A single comprehensive brief covering nine screens — legible to a human reviewer — produced incoherent outputs in practice; screens drifted aesthetically despite shared design tokens. The third approach, Stitch's *"imagine a new screen"* feature applied to a button inside an existing canvas, produced the strongest outputs because the source-screen context (sidebar, palette, typography, chrome) was carried forward automatically.

The pattern: Stitch works when asked to branch from an existing frame and vary one thing — much as a human designer does. A single comprehensive brief appears to exceed Stitch's single-generation working memory. The acceleration is real (nine polished screens in a session, where the same in Figma would have taken days). The constraint is that multi-screen coherence is earned through provenance, not described upfront.

### What would you change to productionise this system?

The live Cloud Run deployment was retested independently ([`qa/stress_test_2026-04-19.md`](qa/stress_test_2026-04-19.md)). Core generation works (~27s for a small upload), prompt-injection resistance held, mobile layout passed. Eight client-side issues remain — the priority list is the productionisation roadmap.

Highest-value fixes are the ones that affect reliability and cost exposure: enforcing the stated 15 MB upload limit at the boundary instead of letting 16 MB files through to base64 encoding; clearing stale file state after invalid uploads; replacing the indefinite cover-art spinner with a timeout fallback; adding cancel/retry/elapsed-time controls during generation. After that come the polish and accessibility fixes — `aria-label` on icon-only remove buttons, real `<title>` and meta description, softening the "in under a minute" copy that the SLA cannot guarantee.

Architecturally, two changes follow from the prompt-engineering work: a routed model (Flash by default, Pro on flagged deals) instead of one model for all calls, and explicit contradiction-class handling at the prompt layer with stakeholder-alignment examples, since the V3 sweep showed that without them the model treats the pre-mortem as a second adversarial pass.
