from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import Animal, PageFormat
from . import settings
from django.http import HttpResponse
from . import pdf
from .s3 import S3
from .page import Page


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


def get_book(request):

    # first_name = "Vlada"
    # last_name = "Rapaport"
    # birth_date = "June 30th, 1988"

    # Get user input from request
    first_name = request.GET.get("first_name", "").strip()
    last_name = request.GET.get("last_name", "").strip()
    birth_date = request.GET.get("birth_date", "").strip()

    if not first_name or not last_name or not birth_date:
        return HttpResponseNotFound("One or more required parameters are missing")

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

    # animal_pic = get_image(s3, "Bear")

    pages_list = [
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
    pdf.create_book_pdf("/tmp/book.pdf", pages_list)

    return JsonResponse("ok", safe=False)
