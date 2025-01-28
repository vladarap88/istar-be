from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from .page import Page
from typing import List


def create_book_pdf(filename, pages_content: List[Page]):
    pdf = SimpleDocTemplate(filename, pagesize=letter)

    # Define a style for the text
    styles = getSampleStyleSheet()
    style = styles["BodyText"]  # You can customize this style

    # List to hold all content for the PDF
    content = []
    # Add each page's text and image
    for i, page in enumerate(pages_content):
        # Add text
        content.append(Paragraph(page.text, style))
        # Add image if available
        if page.image:
            image = Image(BytesIO(page.image))  # Convert binary data to an image
            image.drawWidth = 400  # Adjust width (in points)
            image.drawHeight = 300  # Adjust height (in points)
            content.append(image)

        # Add a page break if it's not the last page
        if i < len(pages_content) - 1:
            content.append(PageBreak())

    # Build the PDF
    pdf.build(content)
