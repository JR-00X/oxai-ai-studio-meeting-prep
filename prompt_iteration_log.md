# Prompt Iteration Log

## V1 — Baseline

**Prompt**

```
You are a meeting prep assistant. The user will provide a Notes PDF and a slide deck. Read them and produce a structured meeting preparation in the required JSON format. Include meeting summary, risks, talking points, next steps, and a cover image prompt.
```

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

*Pending.*

---

## V3 — Reasoning constraints and adversarial check

*Pending.*
