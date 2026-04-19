"""Render the Acme QBR deck as a PDF mirroring slides.pptx, one slide per page.

Output: sample_inputs/slides.pdf
Kept in lockstep with build_slides_pptx.py — same palette, same content, same layout.
LibreOffice is not installed in this env, so we render directly via ReportLab rather
than converting the .pptx binary.
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = Path(__file__).resolve().parent.parent / "sample_inputs" / "slides.pdf"

# 16:9 at 13.333" x 7.5" — matches python-pptx default widescreen.
PAGE_W = 13.333 * inch
PAGE_H = 7.5 * inch
PAGESIZE = (PAGE_W, PAGE_H)

# Palette (Midnight Executive — matches build_slides_pptx.py)
NAVY = HexColor("#1E2761")
ICE = HexColor("#CADCFC")
WHITE = HexColor("#FFFFFF")
CHARCOAL = HexColor("#22222B")
MUTED = HexColor("#6B7385")
ACCENT = HexColor("#E8B54A")


def rect(c, x, y, w, h, fill):
    c.setFillColor(fill)
    c.setStrokeColor(fill)
    c.rect(x, y, w, h, stroke=0, fill=1)


def text(c, x, y, s, size=14, bold=False, color=CHARCOAL, font="Helvetica",
         align="left", italic=False):
    name = font
    if bold and italic:
        name = f"{font}-BoldOblique" if font == "Helvetica" else f"{font}-BoldItalic"
    elif bold:
        name = f"{font}-Bold"
    elif italic:
        name = f"{font}-Oblique" if font == "Helvetica" else f"{font}-Italic"
    c.setFont(name, size)
    c.setFillColor(color)
    if align == "right":
        c.drawRightString(x, y, s)
    elif align == "center":
        c.drawCentredString(x, y, s)
    else:
        c.drawString(x, y, s)


# Coordinate helpers: convert the pptx's top-down inch coords to ReportLab bottom-up.
def Y(y_inches):  # top-down inches → bottom-up points
    return PAGE_H - (y_inches * inch)


def X(x_inches):
    return x_inches * inch


def page_number_footer(c, n, total=8, dark=False):
    color_muted = ICE if dark else MUTED
    text(c, X(0.5), Y(7.3), "CONFIDENTIAL  ·  ACME CORP QBR  ·  APRIL 2026",
         size=9, color=color_muted)
    text(c, X(12.8), Y(7.3), f"{n} / {total}", size=9, color=color_muted,
         align="right")


def left_bar(c):
    rect(c, 0, 0, X(0.35), PAGE_H, NAVY)


# ----------------- slides -----------------
def slide_1_title(c):
    rect(c, 0, 0, PAGE_W, PAGE_H, NAVY)
    rect(c, X(0.8), Y(2.72), X(0.5) - X(0), 0.12 * inch, ACCENT)

    text(c, X(0.8), Y(3.6), "Acme Corp", size=64, bold=True, color=WHITE)
    text(c, X(0.8), Y(4.5), "Quarterly Business Review", size=32, color=ICE)
    text(c, X(0.8), Y(5.1), "Q1 2026 Review and Path Forward",
         size=20, italic=True, color=ICE)
    text(c, X(0.8), Y(6.9), "April 2026", size=12, color=ICE)
    page_number_footer(c, 1, dark=True)


def slide_2_agenda(c):
    rect(c, 0, 0, PAGE_W, PAGE_H, WHITE)
    left_bar(c)
    text(c, X(0.8), Y(1.1), "Agenda", size=40, bold=True, color=NAVY)
    text(c, X(0.8), Y(1.7), "Six blocks, 60 minutes, discussion over slides.",
         size=14, italic=True, color=MUTED)

    items = [
        ("01", "Value delivered this quarter"),
        ("02", "Usage and adoption trends"),
        ("03", "Support and reliability"),
        ("04", "Roadmap and 2026 vision"),
        ("05", "Renewal and partnership"),
        ("06", "Open discussion"),
    ]
    y = 2.55
    for num, label in items:
        # circle
        c.setFillColor(NAVY); c.setStrokeColor(NAVY)
        c.circle(X(0.9) + 0.275 * inch, Y(y + 0.275), 0.275 * inch,
                 stroke=0, fill=1)
        text(c, X(0.9) + 0.275 * inch, Y(y + 0.42), num,
             size=14, bold=True, color=WHITE, align="center")
        text(c, X(1.7), Y(y + 0.4), label, size=20, color=CHARCOAL)
        y += 0.7

    page_number_footer(c, 2)


def slide_3_value(c):
    rect(c, 0, 0, PAGE_W, PAGE_H, WHITE)
    left_bar(c)
    text(c, X(0.8), Y(1.1), "Value delivered this quarter",
         size=36, bold=True, color=NAVY)
    text(c, X(0.8), Y(1.7), "A strong Q1 on every dimension we measure.",
         size=14, italic=True, color=MUTED)

    stats = [
        ("2.4x", "ROI demonstrated through",
         "reduced analytics team time"),
        ("+38%", "Quarter-over-quarter", "query growth"),
        ("12", "New dashboards deployed", "to production"),
    ]
    card_w = 3.7 * inch
    card_h = 3.2 * inch
    gap = 0.3 * inch
    total_w = card_w * 3 + gap * 2
    start_x = (PAGE_W - total_w) / 2
    y_top = 2.4  # inches from top
    for i, (big, l1, l2) in enumerate(stats):
        x = start_x + (card_w + gap) * i
        # card background
        rect(c, x, Y(y_top + 3.2), card_w, card_h, ICE)
        # top band
        rect(c, x, Y(y_top + 0.15), card_w, 0.15 * inch, NAVY)
        # big number
        text(c, x + 0.3 * inch, Y(y_top + 1.4), big,
             size=72, bold=True, color=NAVY)
        # small lines
        text(c, x + 0.3 * inch, Y(y_top + 2.25), l1, size=14, color=CHARCOAL)
        text(c, x + 0.3 * inch, Y(y_top + 2.55), l2, size=14, color=CHARCOAL)

    page_number_footer(c, 3)


def slide_4_usage(c):
    rect(c, 0, 0, PAGE_W, PAGE_H, WHITE)
    left_bar(c)
    text(c, X(0.8), Y(1.1), "Usage and adoption",
         size=36, bold=True, color=NAVY)
    text(c, X(0.8), Y(1.7), "Growth across every cohort we track.",
         size=14, italic=True, color=MUTED)

    bullets = [
        "Monthly active users up 12% QoQ",
        "Power user cohort growing",
        "Query volume up 38% QoQ — broadening, not just deepening",
        "Dashboard creation velocity at an all-time high",
        "Self-serve adoption expanding beyond the core data team",
    ]
    y = 2.7
    for b in bullets:
        text(c, X(0.9), Y(y), f"•  {b}", size=18, color=CHARCOAL)
        y += 0.55

    # chart card
    chart_x = X(7.3)
    chart_top = 2.5
    chart_w = 5.2 * inch
    chart_h = 4.2 * inch
    rect(c, chart_x, Y(chart_top + 4.2), chart_w, chart_h, ICE)
    text(c, chart_x + 0.3 * inch, Y(chart_top + 0.35),
         "Monthly Active Users — trailing 4 quarters",
         size=12, bold=True, color=NAVY)
    # bars
    bar_heights = [1.8, 2.1, 2.5, 2.8]
    bar_labels = ["Q2'25", "Q3'25", "Q4'25", "Q1'26"]
    baseline_y = chart_top + 3.6  # inches from top for bar bottom
    bar_w = 0.9 * inch
    bar_gap = 0.25 * inch
    base_x = chart_x + 0.5 * inch
    for i, h in enumerate(bar_heights):
        x = base_x + (bar_w + bar_gap) * i
        bh_in = h * 0.9  # inches of height
        rect(c, x, Y(baseline_y), bar_w, bh_in * inch, NAVY)
        text(c, x + bar_w / 2, Y(baseline_y + 0.25), bar_labels[i],
             size=10, color=MUTED, align="center")

    page_number_footer(c, 4)


def slide_5_support(c):
    rect(c, 0, 0, PAGE_W, PAGE_H, WHITE)
    left_bar(c)
    text(c, X(0.8), Y(1.1), "Support and reliability",
         size=36, bold=True, color=NAVY)
    text(c, X(0.8), Y(1.7), "A platform Acme can build on.",
         size=14, italic=True, color=MUTED)

    stats = [
        ("99.2%", "Uptime delivered", ""),
        ("18 hrs", "Average ticket", "resolution"),
        ("0", "Data incidents", ""),
    ]
    card_w = 3.7 * inch; card_h = 3.2 * inch; gap = 0.3 * inch
    total_w = card_w * 3 + gap * 2
    start_x = (PAGE_W - total_w) / 2
    y_top = 2.4
    for i, (big, l1, l2) in enumerate(stats):
        x = start_x + (card_w + gap) * i
        rect(c, x, Y(y_top + 3.2), card_w, card_h, ICE)
        rect(c, x, Y(y_top + 0.15), card_w, 0.15 * inch, NAVY)
        text(c, x + 0.3 * inch, Y(y_top + 1.5), big,
             size=64, bold=True, color=NAVY)
        text(c, x + 0.3 * inch, Y(y_top + 2.35), l1, size=14, color=CHARCOAL)
        if l2:
            text(c, x + 0.3 * inch, Y(y_top + 2.65), l2,
                 size=14, color=CHARCOAL)

    page_number_footer(c, 5)


def slide_6_roadmap(c):
    rect(c, 0, 0, PAGE_W, PAGE_H, WHITE)
    left_bar(c)
    text(c, X(0.8), Y(1.1), "2026 Roadmap",
         size=36, bold=True, color=NAVY)
    text(c, X(0.8), Y(1.7),
         "Shared roadmap: building the next phase together.",
         size=16, italic=True, color=MUTED)

    items = [
        ("H1", "Advanced anomaly detection",
         "Real-time statistical and ML-driven outlier surfacing across ingested streams."),
        ("H1", "Multi-region data residency",
         "EU + APAC primary regions with compliance-aligned routing."),
        ("H2", "Native LLM integration",
         "First-class primitives for semantic search, retrieval, and grounded Q&A."),
        ("H2", "Expanded EMEA coverage",
         "Regional support coverage and a named CSM for the EMEA business unit."),
    ]
    y = 2.5
    for tag, title_, body in items:
        # tag box
        rect(c, X(0.9), Y(y + 0.45), 0.8 * inch, 0.45 * inch, NAVY)
        text(c, X(0.9) + 0.4 * inch, Y(y + 0.3), tag,
             size=14, bold=True, color=WHITE, align="center")
        text(c, X(1.9), Y(y + 0.22), title_, size=18, bold=True, color=CHARCOAL)
        text(c, X(1.9), Y(y + 0.55), body, size=12, color=MUTED)
        y += 1.05

    page_number_footer(c, 6)


def slide_7_renewal(c):
    rect(c, 0, 0, PAGE_W, PAGE_H, WHITE)
    left_bar(c)
    text(c, X(0.8), Y(1.1), "Renewal and partnership",
         size=36, bold=True, color=NAVY)
    text(c, X(0.8), Y(1.7),
         "A proposal designed for the next phase of the partnership.",
         size=14, italic=True, color=MUTED)

    items = [
        ("PROPOSED", "3-year renewal with locked-in rates",
         "Price certainty through 2029. No annual increases."),
        ("EXPANDED ACCESS", "EMEA business unit rollout",
         "Extend platform coverage to the EMEA BU, with regional support."),
        ("EXECUTIVE SPONSOR PROGRAM",
         "Named executive sponsors on both sides",
         "Quarterly executive cadence; priority access for roadmap input."),
    ]
    y = 2.4
    for label, title_, body in items:
        rect(c, X(0.9), Y(y + 1.3), 11.5 * inch, 1.3 * inch, ICE)
        rect(c, X(0.9), Y(y + 1.3), 0.15 * inch, 1.3 * inch, NAVY)
        text(c, X(1.25), Y(y + 0.32), label, size=10, bold=True, color=NAVY)
        text(c, X(1.25), Y(y + 0.7), title_,
             size=18, bold=True, color=CHARCOAL)
        text(c, X(1.25), Y(y + 1.05), body, size=12, color=MUTED)
        y += 1.45

    page_number_footer(c, 7)


def slide_8_discussion(c):
    rect(c, 0, 0, PAGE_W, PAGE_H, NAVY)
    rect(c, X(0.8), Y(2.42), 0.5 * inch, 0.12 * inch, ACCENT)
    text(c, X(0.8), Y(3.4), "Open discussion", size=56, bold=True, color=WHITE)
    text(c, X(0.8), Y(4.4),
         "What would make the next 12 months", size=32, italic=True, color=ICE)
    text(c, X(0.8), Y(5.0),
         "a success for Acme?", size=32, italic=True, color=ICE)
    page_number_footer(c, 8, dark=True)


def build():
    c = canvas.Canvas(str(OUT), pagesize=PAGESIZE)
    c.setTitle("Acme Corp — Quarterly Business Review")
    c.setAuthor("Account Team")

    for fn in [slide_1_title, slide_2_agenda, slide_3_value, slide_4_usage,
               slide_5_support, slide_6_roadmap, slide_7_renewal,
               slide_8_discussion]:
        fn(c)
        c.showPage()

    c.save()
    print(f"Wrote: {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
