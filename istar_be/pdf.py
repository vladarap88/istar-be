from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Image,
    Spacer,
    PageBreak,
    PageTemplate,
    Frame,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from .page import Page
from typing import List


def create_book_pdf(pages_content: List[Page], image_store):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    custom_style = ParagraphStyle(
        name="CustomStyle",
        fontName="Courier",
        fontSize=20,
        leading=20,
        alignment=1,
        spaceAfter=12,
    )

    content = []
    page_height = letter[1]
    page_width = letter[0]

    frame = Frame(
        0.5 * inch,
        0.5 * inch,
        page_width - 1 * inch,
        page_height - 1 * inch,
        id="normal",
    )

    page_template = PageTemplate(id="custom", frames=frame)
    pdf.addPageTemplates([page_template])
    content.append(Spacer(1, page_height / 4))
    image = Image(BytesIO(image_store.get_image("1")))
    image.drawWidth = 3 * inch
    image.drawHeight = 3 * inch
    content.append(image)
    content.append(PageBreak())

    for i, page in enumerate(pages_content):
        content.append(Paragraph(page.text, custom_style))

        if page.image:
            content.append(Spacer(1, 30))
            image = Image(BytesIO(page.image))
            image.drawWidth = 3 * inch
            image.drawHeight = 3 * inch
            content.append(image)

        if i < len(pages_content) - 1:
            content.append(PageBreak())

    pdf.build(content)
    buffer.seek(0)
    return buffer
