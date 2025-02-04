import re

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Animal, PageFormat
from . import settings
from . import pdf
from .s3 import S3
from .page import Page
from .email import send_email


def handle_name(animal_name, animals, page_templates, name_chars_set, image_store: S3):
    pages = []
    for letter in animal_name.lower():
        animal_name, description = animals[letter]
        if letter in name_chars_set:
            pages.append(
                Page(
                    page_templates["repeated_letter"]
                    .replace("<letter>", letter.upper())
                    .replace("<animal_name>", animal_name),
                    image_store.get_image(animal_name),
                )
            )
        else:
            pages.append(Page(description, image_store.get_image(animal_name)))
            name_chars_set.add(letter)

        pages.append(
            Page(
                page_templates["after_animal"]
                .replace("<letter>", letter.upper())
                .replace("<animal_name>", animal_name)
            )
        )
    return pages


def is_valid_email(email):
    """Validates an email address using a regex pattern."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


@api_view(["POST"])  # Allows only POST requests
def create_book(request):
    # Get user input from request
    first_name = request.data.get("first_name", "").strip().lower()
    last_name = request.data.get("last_name", "").strip().lower()
    birth_date = request.data.get("birth_date", "").strip()
    email = request.data.get("email", "")
    personal_note = request.data.get("personal_note", "")

    if not first_name or not last_name or not birth_date:
        return HttpResponseNotFound("One or more required parameters are missing")

    if not first_name.isalpha() or not last_name.isalpha():
        return HttpResponseBadRequest("First/last names contain illegal characters")

    if email and not is_valid_email(email):
        return HttpResponseBadRequest("invalid email address")

    # Fetch all data from the database
    animals = {
        animal.name[0].lower(): (animal.name, animal.description)
        for animal in Animal.objects.all()
    }
    page_templates = {
        page.page_number: page.description for page in PageFormat.objects.all()
    }

    # initialize s3 connection
    image_store = S3()

    pages_list = []
    if personal_note:
        pages_list.append(Page(personal_note[:200]))

    pages_list += [
        Page(page_templates["first_page"]),
        Page(page_templates["second_page"].replace("<date>", birth_date)),
        Page(page_templates["third_page"]),
    ]

    name_chars_set = set()
    pages_list += handle_name(
        first_name, animals, page_templates, name_chars_set, image_store
    )
    pages_list.append(
        Page(page_templates["first_name"].replace("<first_name>", first_name.upper()))
    )
    pages_list += handle_name(
        last_name, animals, page_templates, name_chars_set, image_store
    )

    pages_list.append(
        Page(
            page_templates["last_page"]
            .replace("<last_name>", " ".join([first_name.upper(), last_name.upper()]))
            .replace("<date>", birth_date)
        )
    )

    pdf_file = pdf.create_book_pdf(pages_list)
    file_data = pdf_file.getvalue()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="book.pdf"'

    if email:
        send_email(first_name, email, file_data)

    return response
