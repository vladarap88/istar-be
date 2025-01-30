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


def create_book_pdf(pages_content: List[Page]):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Define a custom style for the text
    custom_style = ParagraphStyle(
        name="CustomStyle",
        fontName="Courier",
        fontSize=20,
        leading=20,
        alignment=1,
        spaceAfter=12,
    )

    # Define the title style (same font as book)
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontName="Courier",  # Same as book text
        fontSize=40,  # Larger for emphasis
        alignment=1,  # Center align
        spaceAfter=30,
    )

    # List to hold all content for the PDF
    content = []
    page_height = letter[1]
    page_width = letter[0]

    # Create a Frame to hold content on the page
    frame = Frame(
        0.5 * inch,
        0.5 * inch,
        page_width - 1 * inch,
        page_height - 1 * inch,
        id="normal",
    )

    # Add the PageTemplate with the frame only
    page_template = PageTemplate(id="custom", frames=frame)
    pdf.addPageTemplates([page_template])

    # Add Title Page
    content.append(Spacer(1, page_height / 3))  # Move title down to center
    content.append(Paragraph("iStar", title_style))  # Same font as the book
    content.append(PageBreak())  # Move to the next page

    for i, page in enumerate(pages_content):
        content.append(Paragraph(page.text, custom_style))

        # If there is an image, add a larger gap
        if page.image:
            content.append(Spacer(1, 30))  # Increased gap between text and image
            image = Image(BytesIO(page.image))
            image.drawWidth = 3 * inch
            image.drawHeight = 3 * inch
            content.append(image)

        # Add a page break if it's not the last page
        if i < len(pages_content) - 1:
            content.append(PageBreak())

    # Build the PDF
    pdf.build(content)
    buffer.seek(0)
    return buffer
