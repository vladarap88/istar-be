# istar-be

Overview

The iStar backend is a Django-based application that generates personalized children's books in PDF format. Users can input their first name, last name, date of birth, and an optional email and personal note. The backend retrieves corresponding animal descriptions and images, formats the content into a book, and delivers the PDF via download or email.


Features

Processes user input to generate a personalized book.
Retrieves animal data from a PostgreSQL database.
Fetches images from AWS S3 storage.
Creates a multi-page PDF using ReportLab.
Sends the generated book via email using SendGrid.


Technologies Used

Django & Django REST Framework: Backend framework and API handling.
PostgreSQL: Database containing animal information and book text. 
AWS S3: Storage for book images.
ReportLab: PDF generation.
SendGrid: Email service for delivering book PDFs.