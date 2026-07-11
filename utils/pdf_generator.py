import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from xml.sax.saxutils import escape


def generate_pdf(
    transcript,
    summary,
    notes,
    keywords,
    quiz,
    flashcards,
    output_path="outputs/lecture_notes.pdf"
):
    os.makedirs("outputs", exist_ok=True)

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading1"],
        fontSize=16,
        spaceBefore=12,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15
    )

    story = []

    story.append(
        Paragraph(
            "Lecture Voice-to-Notes Generator",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI-Generated Study Material",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 20))

    sections = [
        ("Complete Transcript", transcript),
        ("Concise Summary", summary),
        ("Organized Study Notes", notes),
        ("Important Keywords", keywords),
        ("Quiz", quiz),
        ("Flashcards", flashcards)
    ]

    for index, (heading, content) in enumerate(sections):

        story.append(
            Paragraph(
                escape(heading),
                heading_style
            )
        )

        safe_content = escape(
            content or "No content generated."
        )

        safe_content = safe_content.replace(
            "\n",
            "<br/>"
        )

        story.append(
            Paragraph(
                safe_content,
                body_style
            )
        )

        if index < len(sections) - 1:
            story.append(PageBreak())

    document.build(story)

    return output_path