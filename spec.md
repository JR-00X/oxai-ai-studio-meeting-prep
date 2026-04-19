# Spec — Meeting Prep Assistant (minimal)

Scope lock for the assignment. Anything not in this document is out of scope.

## Purpose

Help an account manager walk into a client meeting prepared, in under a minute. The user uploads two documents — the internal notes and the customer-facing slide deck — and the app returns a structured briefing: summary, risks, talking points, next steps, with citations back to the source. Nothing is stored.

## Scope — two screens

### 1. Landing (Upload)

- Single drop zone on a single page, accepting PDF and PPTX, multiple files at once.
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

## Model and prompt

- Model: Gemini 3.1 Pro Preview, Thinking High, Temperature 1.0.
- Structured output enforced to `schema/output_schema.json`.
- System prompt: `prompts/v3.md`.
- All external tools disabled (no search, no URL fetch, no code execution, no function calling).

## Why this spec and not the nine-screen Stitch set

The Stitch screens (Dashboard, History, Analytics, detail tabs, mitigation views) explored the broader product surface as workflow evidence for the reflection section. A full dashboard-style app is a natural evolution, not a requirement of the assignment brief. The brief asks for a Gem, a schema, UX screens, and an iteration narrative — two screens cover that scope. Everything else is optional and has been generated only to exercise Stitch and inform the reflection.
