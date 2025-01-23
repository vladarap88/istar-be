from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import Animal, PageFormat


def handle_name(name, animals, page_templates, name_chars_set):
    pages = []
    for letter in name.lower():
        name, description = animals[letter]
        if letter in name_chars_set:
            pages.append(
                page_templates["repeated_letter"]
                .replace("<letter>", letter.upper())
                .replace("<animal_name>", name)
            )
        else:
            pages.append(description)
            name_chars_set.add(letter)

        pages.append(
            page_templates["after_animal"]
            .replace("<letter>", letter.upper())
            .replace("<animal_name>", name)
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

    # book prologue
    book = [
        page_templates["first_page"],
        page_templates["second_page"].replace("<date>", birth_date),
        page_templates["third_page"],
    ]

    name_chars_set = set()
    book += handle_name(first_name, animals, page_templates, name_chars_set)
    book.append(
        page_templates["first_name"].replace("<first_name>", first_name.upper())
    )
    book += handle_name(last_name, animals, page_templates, name_chars_set)

    book.append(
        page_templates["last_page"]
        .replace("<last_name>", " ".join([first_name.upper(), last_name.upper()]))
        .replace("<date>", birth_date)
    )

    return JsonResponse(book, safe=False)
