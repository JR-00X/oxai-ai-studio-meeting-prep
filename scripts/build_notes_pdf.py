"""Generate the fictional Acme Corp QBR notes PDF.

Output: sample_inputs/notes.pdf
Voice: informal internal CRM/Notion notes from the account manager — NOT polished prose.
"""
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)

OUT = Path(__file__).resolve().parent.parent / "sample_inputs" / "notes.pdf"

styles = getSampleStyleSheet()

H1 = ParagraphStyle(
    "H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=14, spaceAfter=8, textColor="#222222",
)
H2 = ParagraphStyle(
    "H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=11, spaceBefore=10, spaceAfter=4, textColor="#333333",
)
BODY = ParagraphStyle(
    "Body", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=10, leading=14, spaceAfter=4,
)
BULLET = ParagraphStyle(
    "Bullet", parent=BODY, leftIndent=16, bulletIndent=4, spaceAfter=2,
)
FOOTER = ParagraphStyle(
    "Footer", parent=BODY, fontSize=8, textColor="#888888", spaceBefore=12,
)


def bullet(text: str) -> Paragraph:
    return Paragraph(f"&bull; {text}", BULLET)


def build():
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="Acme Corp — QBR Prep Notes",
        author="Account Manager (internal)",
    )

    story = []

    # ---------------- PAGE 1 ----------------
    story.append(Paragraph("Acme Corp — QBR prep (internal notes)", H1))
    story.append(Paragraph(
        "Draft scratchpad before the Apr QBR. Don't share externally.",
        BODY,
    ))

    story.append(Paragraph("Account background", H2))
    story.append(bullet(
        "Acme Corp — mid-market SaaS, ~800 FTE. Customer since Oct 2024 (~18 months in)."
    ))
    story.append(bullet(
        "We ingest their operational data and power their internal analytics layer. "
        "Core use case: product analytics + finance reporting."
    ))
    story.append(bullet(
        "Contract: <b>$1.2M ARR</b>. Renewal in ~90 days. Auto-renew clause in the MSA — "
        "we do NOT want them to invoke it; want a real conversation."
    ))

    story.append(Paragraph("Stakeholder map", H2))
    story.append(bullet(
        "<b>Sarah Chen</b> — VP Data. Our champion, main day-to-day contact. "
        "Has political capital but spends it carefully."
    ))
    story.append(bullet(
        "<b>Marcus Webb</b> — CTO. Quiet supporter. Rarely pushes back but doesn't "
        "evangelize us either. Was on one of the P1 tickets last month (see p.2)."
    ))
    story.append(bullet(
        "<b>Elena Rodriguez</b> — CFO. <b>Has joined the last 2 calls UNPROMPTED.</b> "
        "Unusual — CFOs don't show up to vendor reviews unless something's brewing. Flag."
    ))
    story.append(bullet(
        "<b>Dev Patel</b> — Head of Data Science. Newer (joined summer 2025). "
        "Stance unclear. Haven't had a 1:1 yet."
    ))

    story.append(Paragraph("Offhand / parked items", H2))
    story.append(bullet(
        "Elena asked about 'multi-year pricing flexibility' on the last call — "
        "didn't follow up. Probably should have."
    ))
    story.append(bullet(
        "Sarah's calendar invite title changed from just 'QBR' to 'QBR + roadmap'. "
        "The 'roadmap' addition is new. Not sure who's driving that — her? Elena? Marcus?"
    ))

    story.append(Paragraph("Page 1 of 3 — internal prep notes", FOOTER))

    # ---------------- PAGE 2 ----------------
    story.append(PageBreak())
    story.append(Paragraph("Recent activity — last 90 days", H1))

    story.append(Paragraph("Usage metrics (good news)", H2))
    story.append(bullet("Queries: <b>+38% QoQ</b>. Real growth, not a backfill spike."))
    story.append(bullet("Monthly active users: <b>+12% QoQ</b>."))
    story.append(bullet("12 new dashboards deployed to prod (their count, not ours)."))

    story.append(Paragraph("Usage metrics (the wrinkle)", H2))
    story.append(bullet(
        "Acme's data science team had layoffs in Feb. Heard it offhand in a Slack "
        "thread — 'heard Dev lost 3 of his 8 people'. We've never officially been told. "
        "Means the +12% MAU growth is happening even as headcount shrank — "
        "or it's being inflated by a few heavy users."
    ))
    story.append(bullet(
        "Training session for their new analysts: <b>3 of 12 registered</b>. "
        "Low engagement. Sarah didn't comment on the low number when I sent her the list."
    ))

    story.append(Paragraph("Support and reliability (awkward)", H2))
    story.append(bullet(
        "2 P1 tickets last month. Both resolved, but avg time-to-resolution was <b>~48h</b>. "
        "Our SLA is 24h. We breached it."
    ))
    story.append(bullet(
        "<b>Marcus was on one of the P1s.</b> He didn't escalate publicly but he saw the "
        "slow response first-hand. That's the kind of thing a CTO remembers at renewal."
    ))
    story.append(bullet(
        "Our deck says 'avg ticket resolution 18h' — that's the all-tickets average. "
        "For P1s specifically it was 48h. Know the difference before they ask."
    ))

    story.append(Paragraph("Open integration request", H2))
    story.append(bullet(
        "Custom data export format — they asked in Q2 2025. We scoped it. Never quoted. "
        "Sarah reminded us on the March call. We said 'next quarter' again. Third time."
    ))

    story.append(Paragraph("Page 2 of 3 — internal prep notes", FOOTER))

    # ---------------- PAGE 3 ----------------
    story.append(PageBreak())
    story.append(Paragraph("Competitive intel and open threads", H1))

    story.append(Paragraph("Competitive", H2))
    story.append(bullet(
        "Sarah DM'd me 2 weeks ago: 'someone reached out from [Competitor X]'. "
        "She played it cool. I played it cool. Neither of us followed up. "
        "Assume they're in at least an exploratory conversation."
    ))

    story.append(Paragraph("Pricing pressure signals", H2))
    story.append(bullet(
        "Elena asked for a 'usage-based pricing options' comparison. I sent a one-pager, "
        "no follow-up from her. Our current deal is flat-rate annual."
    ))
    story.append(bullet(
        "<b>Procurement is now CC'd on all emails.</b> This is new — they weren't "
        "involved in Q4. That's a renewal signal, not a value-review signal."
    ))

    story.append(Paragraph("Open questions we haven't answered", H2))
    story.append(bullet(
        "Q4 ask: custom data export format. Scoped, never quoted. See p.2."
    ))
    story.append(bullet(
        "SOC 2 Type II — Sarah mentioned in Feb that their new healthcare client "
        "might require it. Never confirmed with her whether it's still a live requirement."
    ))

    story.append(Paragraph("Our open asks", H2))
    story.append(bullet(
        "Want to expand into their EMEA business unit. Raised in Q4, no traction since. "
        "Putting it in the deck for Tuesday anyway (slide 7)."
    ))

    story.append(Paragraph("Things to clarify on the day", H2))
    story.append(bullet(
        "Who added 'roadmap' to the QBR invite title and why? If it's Marcus, "
        "that's a tech conversation. If it's Elena, it's a pricing conversation in disguise."
    ))
    story.append(bullet(
        "Marcus has never been shown our 2026 roadmap slide. The AM (me) put it in "
        "deck without CTO alignment. Risk: he sees something he disagrees with in real time."
    ))

    story.append(Paragraph("Page 3 of 3 — internal prep notes", FOOTER))

    doc.build(story)
    print(f"Wrote: {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
