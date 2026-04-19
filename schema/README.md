# schema/

This directory defines the structured JSON contract the Gem must return — `output_schema.json`. Every shape here exists for a reason: the assignment demands grounding and anti-hallucination, and the schema is the primary enforcement mechanism before any prompt text.

**Why this shape:**

- **Required `evidence` fields on every risk and talking point** force the model to cite the source document (e.g., `"Notes p.3"`, `"Slide 7"`). If the model cannot produce a citation, the field is empty and the hallucination is visible rather than hidden inside fluent prose. This is the single strongest grounding lever available without RAG.
- **`severity` as an enum (`High | Medium | Low`)** collapses an unbounded adjective space into three buckets the user can triage on. Without the enum, the model drifts into "moderate", "somewhat concerning", "elevated" — useless for prioritisation.
- **Three-part `meeting_summary` (`context` / `headline` / `participant_snapshot`)** mirrors how a prepared person actually walks into a room: *why am I here, what is the one thing, who am I talking to*. A single summary blob would let the model hide behind generality; splitting it forces a one-sentence headline commitment.
- **`why_it_lands` on each talking point** is the dialectical check — the model has to reason about the counterparty's interests, not just the user's. It turns "things I want to say" into "things that will move them", which is the actual job of meeting prep.
- **`cover_image_prompt` is an instruction, not an asset.** The Gem returns a text prompt for a downstream image generator rather than trying to produce the image itself. This keeps the Gem focused on reasoning and defers the wrong-tool-for-the-job problem to a specialised model.
