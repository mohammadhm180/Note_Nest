from django.http import JsonResponse
from django.shortcuts import render
from note_module.models import NoteModel, CategoryModel


def home_page(request):
    categories = None
    if request.user.is_authenticated:
        categories = CategoryModel.objects.filter(user=request.user)

    return render(request, "home_module/home_page.html", {
        'categories': categories
    })


def get_notes(request, category_id):
    if category_id == 0:
        notes = NoteModel.objects.filter(user=request.user)
    else:
        category = CategoryModel.objects.get(id=category_id)
        notes = NoteModel.objects.filter(category=category, user=request.user)

    data = [{'id': note.id, 'title': note.title, 'text': note.text, "category": note.category.title} for note in notes]
    return JsonResponse(data, safe=False)
