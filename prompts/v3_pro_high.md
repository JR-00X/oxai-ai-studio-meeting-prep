# V3 Pro-High — Model sweep

## System prompt

Identical to V3 (`prompts/v3.md`). No prompt changes.

## User message (in chat)

`Prepare me for this meeting.`

## Inputs

- `sample_inputs/notes.pdf`
- `sample_inputs/slides.pdf`

## Run settings

| Setting | Value |
|---|---|
| Model | **Gemini 3.1 Pro Preview** (`gemini-3.1-pro-preview`) (sweep variable) |
| Thinking level | High |
| Temperature | 1.0 |
| Structured output | Enabled |
| All tools | Disabled |

Token count: **9,984**. Chat was started **fresh** (not branched) to isolate model as the varying input. AI Studio renders a "Thoughts" panel showing the Pro reasoning trace.

## Design intent

Isolate model family as the varying input, holding prompt and thinking level constant (vs V3 Flash-High). If Pro-High catches what Flash-High missed, the Flash architecture is the ceiling. If both land in the same place, the prompt is the ceiling.

## Output

`sample_outputs/v3_pro_high.json`

## Diagnosis

See `prompt_iteration_log.md`.
