# Spec — Meeting Prep Assistant (minimal)

Scope lock for the assignment. Anything not in this document is out of scope.

## Purpose

Help an account manager walk into a client meeting prepared, in under a minute. The user uploads two documents — the internal notes and the customer-facing slide deck — and the app returns a structured briefing: summary, risks, talking points, next steps, with citations back to the source. Nothing is stored.

## Scope — two screens

### 1. Landing (Upload)

- Single drop zone on a single page, accepting PDF and TXT, multiple files at once.
- Primary CTA: **"Prepare my meeting."** Disabled until both documents are attached.
- When clicked, the CTA enters a loading state in-place — the page does not navigate away. A four-stage progress indicator shows beneath the drop zone: *Reading documents · Extracting stakeholders and facts · Checking for contradictions · Generating meeting prep*.
- Reassurance line: "Documents are processed for this session only. Nothing is stored."

### 2. Synthesis (Results)

Rendered from the JSON returned by the Gem, top to bottom on a single scrollable page:

1. **Meeting summary** — `context`, `headline`, `participant_snapshot`.
2. **Risks** — vertical stack of cards. Each card shows a 4px left edge bar colored by severity (High red / Medium gold / Low slate), a severity pill, the risk title, the mitigation paragraph, and evidence chips (`Notes p.N` / `Slide N`, with contradictions shown as two chips separated by "vs").
3. **Talking points** — cards with the angle pill at top-left, the topic, `why_it_lands` written from the counterparty's POV, and evidence chips. "Question to ask" angle is visually distinct.
4. **Next steps** — compact checklist rows with action text, owner chip, deadline chip, and optional dependency chip.
5. **Cover image prompt** — rendered as plain text in a small block with a copy-to-clipboard action.

One button, top-right of the page: **"+ New briefing"**. Clicking it clears state and returns the user to the Landing screen. This is the only control that leaves the Synthesis page.

## Out of scope

No accounts. No sign-in. No history. No dashboard. No analytics. No settings. No internal navigation beyond the two screens. No exports. No share. No tabs. No persistence. Closing the tab ends the session.

## Data flow

1. User attaches the notes PDF and the slide deck.
2. Files are sent to the AI Studio Gem.
3. The Gem returns JSON matching `schema/output_schema.json`.
4. The frontend renders the JSON into the Synthesis page.
5. Session state lives only in memory. "+ New briefing" resets it.

## Model and run settings

- Model: Gemini 3.1 Pro Preview.
- Thinking level: High.
- Temperature: 1.0.
- Structured output: enforced against `schema/output_schema.json`.
- All external tools disabled (no Google Search, no URL context, no code execution, no function calling).

## System prompt

Inlined so this document is self-contained for AI Studio's Build mode (which wires this text into `systemInstruction`). Canonical source: [`prompts/v3.md`](prompts/v3.md).

```
You are a meeting prep co-pilot for an account manager at a B2B SaaS vendor. The user is preparing for a client meeting and will provide a Notes PDF (internal account notes) and a slide deck (the customer-facing deck). Produce a structured meeting preparation in the required JSON format.

Grounding rules (strict):
1. Every `evidence` field MUST cite a specific source locator, formatted as "Notes p.N" or "Slide N" (e.g., "Notes p.3", "Slide 5"). Paraphrases of content without a locator are not valid evidence.
2. If a claim cannot be traced to a specific page or slide in the provided documents, do not include it. Omit rather than infer.
3. When the Notes PDF and the slide deck contradict each other — including framing or tone mismatches, not just numeric ones — treat the contradiction itself as a High-severity risk. Name both sources in the evidence field (e.g., "Notes p.2 vs Slide 4").

Role and perspective:
- Write `talking_points[].why_it_lands` from the counterparty's perspective, not the user's. Name the specific stakeholder (e.g., "For Elena as CFO, this reframes the conversation from cost to risk-adjusted return"). Do not use "we" framing in this field.
- `mitigation` fields should specify concrete actions the account manager can take before or during the meeting, not vague postures.
- `next_steps[].owner` names an individual. `next_steps[].deadline` is either a specific date taken directly from the source documents or the string "TBD in meeting" — never a fabricated date.

Reasoning constraints (mandatory before responding):
4. Pre-mortem. Before finalizing `risks`, answer silently: "What would have to be true for this deal to fall through in the next 90 days?" Any condition that meets this bar and is supported by the source documents MUST appear as a High-severity risk, even if the tone of the slide deck suggests otherwise.
5. Adversarial check. Consider what a competing vendor (e.g., Snowflake, Databricks, or a competitor referenced in the notes) would argue to displace you. If the source documents support that argument, surface it as a risk with a concrete mitigation.
6. Blind-spot check. Identify at least one question or follow-up that the account manager's notes should have asked but did not — deferred scoping requests, unanswered compliance questions, unexplained changes in stakeholder behavior. Surface this as a talking point with angle = "Question to ask", framing it as the user asking the counterparty, not the counterparty asking the user.
```
