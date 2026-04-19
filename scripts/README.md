# scripts/

Generators for the fictional QBR sample inputs under `/sample_inputs/`. These scripts are the source of truth — edit them rather than the binary `.pdf`/`.pptx` outputs.

- `build_notes_pdf.py` — builds `sample_inputs/notes.pdf` (3 pages) using ReportLab.
- `build_slides_pptx.py` — builds `sample_inputs/slides.pptx` (8 slides) using `python-pptx`.

Run either script from the repo root: `python3 scripts/build_notes_pdf.py`.
