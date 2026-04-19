# screens/

Exported UX screens for the Meeting Prep Assistant, plus AI Studio run screenshots.

## Contents

**AI Studio version-history screenshots** (at the root of this folder):
- `ai_studio_v1.png` — V1 baseline, Flash Low
- `ai_studio_v2.png` — V2 grounding and role specificity, Flash Low
- `ai_studio_v3.png` — V3 reasoning constraints, Flash Low
- `ai_studio_v3_flash_high.png` — V3 sweep, Flash High
- `ai_studio_v3_pro_high.png` — V3 sweep, Gemini 3.1 Pro High

**Stitch UX exports** live under `stitch_strategic_meeting_prep_assistant/`, one subfolder per generated screen, each containing `screen.png` and `code.html`. Multiple variants exist for most screens (`_1`, `_2`, `_3`) because generation was iterative — see workflow notes below.

Key subfolders and what they map to in the product flow:
- `unified_upload_screen/` · `updated_upload_screen/` · `upload_screen/` — Upload (landing) variants
- `loading_screen/` — Loading
- `results_screen_1/` · `results_screen_2/` — Results (Briefings hub, Risks tab)
- `briefing_summary_1/` · `briefing_summary_2/` · `briefing_summary_tab_view/` — Summary tab variants
- `talking_points_1/` · `talking_points_2/` · `talking_points_3/` — Talking Points tab variants
- `next_steps_1/` · `next_steps_2/` · `next_steps_briefing_view/` — Next Steps tab variants
- `dashboard_1/` · `dashboard_2/` — Dashboard (workspace) variants
- `history_1/` · `history_2/` · `history_3/` — History (workspace) variants
- `portfolio_insights_1/` · `portfolio_insights_2/` · `portfolio_insights_3/` — Analytics (workspace) variants
- `mitigation_details/` · `mitigation_strategies/` — bonus detail views generated from the "imagine a new screen" flow
- `meeting_prep_assistant_flow_1/` · `meeting_prep_assistant_flow_2/` · `precept_ivory/` — early exploratory outputs kept for reference

## Workflow used (and what worked)

The generation approach evolved in three stages. The evolution is itself a finding worth carrying into the reflection.

1. **Three focused briefs, one screen each.** The initial approach — one natural-language brief per screen (Upload, Loading, Results), giving Stitch concrete layout intent but leaving aesthetic judgment to the model — produced clean, on-brand outputs that could anchor the rest of the project.
2. **One comprehensive one-shot brief covering all nine screens.** An attempt to consolidate everything — design tokens, shell, flow, per-screen content — into a single pasted brief produced less coherent outputs in practice. Screens drifted from each other aesthetically despite the shared tokens, and information density dropped. Not the right abstraction for Stitch's current workflow.
3. **"Imagine a new screen" from the Results canvas.** Selecting a button inside the Results screen (e.g., the "Summary" tab, the "New Briefing" button, a severity pill) and using Stitch's "imagine a new screen" feature produced the strongest outputs of the three approaches. The source-screen context is carried forward automatically — sidebar, color tokens, typography, navigation chrome — so Stitch does not have to re-derive the system prompt for each generation. Each downstream screen was generated this way, with 2–3 variants per target screen to pick the best.

Why the third approach worked better is worth noting for the reflection: it mirrors how a designer actually works (branch from an existing frame, keep the system, explore one variable) rather than asking the tool to hold the entire product in memory at once. A single comprehensive brief is legible to a human reviewer but appears to exceed the "working memory" Stitch brings to a single generation.

Consequence for the reflection's "Stitch accelerate/constrain" question:
- **Accelerates** — producing nine polished screens in a short session, all sharing a coherent visual system, would have taken far longer in a traditional design tool.
- **Constrains** — the one-shot comprehensive brief did not scale, so the workflow still requires a human-in-the-loop sequencing of generations (base frame → branch → variant → pick). Multi-screen coherence is earned through provenance, not described up-front.

## Reusing this folder

Pick one canonical variant per screen when we write `assignment.md`. The rest stay in the repo as workflow evidence and for the reflection's "how did Stitch constrain UX design" discussion.
