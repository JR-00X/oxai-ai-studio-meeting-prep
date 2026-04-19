# screens/

Canonical UX deliverables for the assignment, plus the AI Studio version-history screenshots.

## Canonical product screens

Two screens, matching the scope locked in [`/spec.md`](../spec.md):

- **`01-upload.png`** — Landing (Upload). Single page with a unified drag-and-drop zone, "Meeting context (optional)" row, "Prepare my meeting" CTA, and a reassurance line. Loading is handled in-place on this screen; a dedicated loading page is not in the product.
- **`02-synthesis.png`** — Synthesis (Results). Single scrollable page rendering the Gem's JSON output top to bottom: meeting summary, severity-coded risks with evidence citations, talking points with counterparty-POV framing, next steps checklist, cover image prompt. A single "+ New briefing" control returns to the Landing screen.

Each screen is committed with its Stitch-generated HTML (`01-upload.html`, `02-synthesis.html`) alongside the PNG for reference.

## AI Studio run screenshots

Evidence for the prompt iteration log:

- `ai_studio_v1.png` — V1 baseline, Flash Low
- `ai_studio_v2.png` — V2 grounding and role specificity, Flash Low
- `ai_studio_v3.png` — V3 reasoning constraints, Flash Low
- `ai_studio_v3_flash_high.png` — V3 sweep, Flash High (fresh chat)
- `ai_studio_v3_pro_high.png` — V3 sweep, Gemini 3.1 Pro High (fresh chat)

## About the earlier Stitch exploration

An earlier phase of UX generation produced nine screens (Dashboard, History, Analytics, three meeting-detail tabs, plus bonus mitigation detail views) as Stitch workflow experiments. Those outputs were removed from the repo after the spec was locked to two screens, because they represent a broader product surface that is explicitly out of scope. The full exploration set is preserved in the git history at commit `c4d9dda` for anyone wanting to inspect it — including the workflow finding (one-shot comprehensive brief failed, "imagine a new screen" from the Results canvas worked), which is pulled into the reflection.
