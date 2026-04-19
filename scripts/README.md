# scripts/

Generators for the fictional QBR sample inputs under `/sample_inputs/`. These scripts are the source of truth — edit them rather than the binary `.pdf`/`.pptx` outputs.

- `build_notes_pdf.py` — builds `sample_inputs/notes.pdf` (3 pages) using ReportLab.
- `build_slides_pptx.py` — builds `sample_inputs/slides.pptx` (8 slides) using `python-pptx`.
- `build_slides_pdf.py` — builds `sample_inputs/slides.pdf` (8 pages, one per slide) using ReportLab. Mirrors the `.pptx` layout so uploads into Google AI Studio (which prefers PDF) match what is presented in PowerPoint.

Run any script from the repo root: `python3 scripts/build_notes_pdf.py`. When you change `build_slides_pptx.py`, change `build_slides_pdf.py` in lockstep.
