# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)


def send_email(first_name, email, file_data):

    name = first_name[0].upper() + first_name[1:]
    subject = name + "'s iStar book is attached!"
    message = Mail(
        from_email="istarpdf@gmail.com",
        to_emails=email,
        subject=subject,
        html_content="<strong>PDF file attached</strong>",
    )

    decoded_file_data = base64.b64encode(file_data).decode()
    attachment = Attachment(
        FileContent(decoded_file_data),
        FileName(name + "_iStar.pdf"),
        FileType("application/pdf"),
        Disposition("attachment"),
    )

    message.add_attachment(attachment)

    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    sg.send(message)
