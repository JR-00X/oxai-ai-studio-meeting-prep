# oxai-ai-studio-meeting-prep

Meeting Prep Assistant built with Google AI Studio (Gemini) and Stitch for the Oxford AI Engineering Programme (Week 3 — Google AI Studio assignment). Given a Notes PDF and a QBR slide deck for a fictional enterprise client, the Gem returns structured meeting intelligence (summary, risks, talking points, next steps, cover-image prompt) with citations back to the source documents.

This repo holds the prompt iterations, Stitch screen exports, AI Studio version-history evidence, sample inputs/outputs, and the written reflection required by the brief.

## Live deployment (optional, demo)

A working build is deployed on Google Cloud Run:

**https://meeting-prep-assistant-691081429886.us-west1.run.app**

> ⚠️ **Stability notice.** The deployed app is not fully optimised.
>
> - **PDF uploads above ~1 MB are slow** because no client-side PDF preprocessing was implemented — for the smoothest experience, please use a `.txt` file or a lightweight PDF.
> - Errors may occasionally appear during generation — if that happens, please **retry once**; the second attempt usually completes.
> - If the second retry also fails, please [**open an issue on GitHub**](https://github.com/JR-00X/oxai-ai-studio-meeting-prep/issues/new?title=Cloud+Run+deployment+issue) — a one-line note about what you tried and any error message helps.
>
> Known issues are catalogued in [`qa/stress_test_2026-04-26.md`](qa/stress_test_2026-04-26.md) and addressed in the productionisation section of [`assignment.md`](assignment.md).

## Documents

- Assignment brief: [`Google_AI_Studio_Assignment_Detailed.pdf`](Google_AI_Studio_Assignment_Detailed.pdf)
- Product scope and inlined system prompt: [`spec.md`](spec.md)
- Architecture, design decisions, prompt-engineering narrative, UX, reflection: [`assignment.md`](assignment.md)
- Iteration log with V1 → V2 → V3 + Flash/Pro sweep: [`prompt_iteration_log.md`](prompt_iteration_log.md)
