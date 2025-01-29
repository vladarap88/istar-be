# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO
# from .page import Page
# from typing import List


# def create_book_pdf(filename, pages_content: List[Page]):
#     pdf = SimpleDocTemplate(filename, pagesize=letter)

#     # Define a style for the text
#     styles = getSampleStyleSheet()
#     style = styles["BodyText"]  # You can customize this style

#     # List to hold all content for the PDF
#     content = []
#     # Add each page's text and image
#     for i, page in enumerate(pages_content):
#         # Add text
#         content.append(Paragraph(page.text, style))
#         # Add image if available
#         if page.image:
#             image = Image(BytesIO(page.image))  # Convert binary data to an image
#             image.drawWidth = 400  # Adjust width (in points)
#             image.drawHeight = 300  # Adjust height (in points)
#             content.append(image)

#         # Add a page break if it's not the last page
#         if i < len(pages_content) - 1:
#             content.append(PageBreak())

#     # Build the PDF
#     pdf.build(content)

# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.lib.units import inch
# from io import BytesIO
# from .page import Page
# from typing import List



# def create_book_pdf(filename, pages_content: List[Page]):
#     pdf = SimpleDocTemplate(filename, pagesize=letter)

#     # Define a custom style for the text
#     custom_style = ParagraphStyle(
#         name="CustomStyle",
#         fontName="Courier",  # Prettier font
#         fontSize=20,  # Larger text
#         leading=20,  # Line height
#         alignment=1,  # Center align text
#         spaceAfter=12,  # Space after text
#     )

#     # List to hold all content for the PDF
#     content = []
#     page_height = letter[1]

#     for i, page in enumerate(pages_content):
#         # Add vertical space to position content in the middle upper space (~1/3 down the page)
#         upper_space = page_height / 3
#         content.append(Spacer(1, upper_space))
        
#         # Add text in the middle upper space of the page
#         content.append(Paragraph(page.text, custom_style))
        
#         # Add a gap of 2 lines (~0.5 inch) between text and image if the image exists
#         if page.image:
#             content.append(Spacer(1, 10))  # Gap for image
#             image = Image(BytesIO(page.image))  # Convert binary data to an image
#             image.drawWidth = 3 * inch  # Adjust image width
#             image.drawHeight = 3 * inch  # Adjust image height (maintain square)
#             content.append(image)

#         # Add a page break if it's not the last page
#         if i < len(pages_content) - 1:
#             content.append(PageBreak())

#     # Build the PDF
#     pdf.build(content)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, PageTemplate, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from .page import Page
from typing import List
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Function to draw the light blue background with a sun on odd pages
def draw_background(canvas, doc, page_num):
    page_width, page_height = doc.pagesize
    # Set the fill color to a lighter shade of blue (light cyan)
    canvas.setFillColorRGB(0.678, 0.847, 0.902)  # Lighter blue color
    # Draw a rectangle that covers the entire page
    canvas.rect(0, 0, page_width, page_height, fill=1)

    # Draw the sun only on odd-numbered pages
    if page_num % 2 != 0:
        # Set the fill color to a brighter yellow for the sun
        canvas.setFillColorRGB(1, 1, 0)  # Brighter yellow

        # Draw the sun as a circle at the left-middle-upper part of the page
        sun_radius = 75  # Sun size
        sun_x = page_width * 0.1  # Horizontal position (left-middle)
        sun_y = page_height * 0.75  # Vertical position (upper-middle)

        canvas.circle(sun_x, sun_y, sun_radius, fill=1)  # Draw the bright yellow sun

def create_book_pdf(filename, pages_content: List[Page]):
    pdf = SimpleDocTemplate(filename, pagesize=letter)

    # Define a custom style for the text
    custom_style = ParagraphStyle(
        name="CustomStyle",
        fontName="Courier",  # Prettier font
        fontSize=20,  # Larger text
        leading=20,  # Line height
        alignment=1,  # Center align text
        spaceAfter=12,  # Space after text
    )

    # List to hold all content for the PDF
    content = []
    page_height = letter[1]
    page_width = letter[0]

    # Define the page template with onPage function for custom drawing
    def on_page(canvas, doc):
        page_num = doc.page

        
        # Draw the light blue background with the sun on every page (sun on odd pages)
        draw_background(canvas, doc, page_num)

    # Create a Frame to hold content on the page (this is essential for placing flowables)
    frame = Frame(0.5 * inch, 0.5 * inch, page_width - 1 * inch, page_height - 1 * inch, id='normal')

    # Add the PageTemplate with the custom onPage function and the frame
    page_template = PageTemplate(id='custom', frames=frame, onPage=on_page)
    pdf.addPageTemplates([page_template])

    for i, page in enumerate(pages_content):
        # Add vertical space to position content in the middle upper space (~1/3 down the page)
        upper_space = page_height / 3
        content.append(Spacer(1, upper_space))
        
        # Add text in the middle upper space of the page
        content.append(Paragraph(page.text, custom_style))
        
        # Add a gap of 2 lines (~0.5 inch) between text and image if the image exists
        if page.image:
            content.append(Spacer(1, 10))  # Gap for image
            image = Image(BytesIO(page.image))  # Convert binary data to an image
            image.drawWidth = 3 * inch  # Adjust image width
            image.drawHeight = 3 * inch  # Adjust image height (maintain square)
            content.append(image)

        # Add a page break if it's not the last page
        if i < len(pages_content) - 1:
            content.append(PageBreak())

    # Build the PDF
    pdf.build(content)



