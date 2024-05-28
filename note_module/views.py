from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import NoteForm, CategoryForm
from .models import NoteModel, CategoryModel


# Create your views here.

def note_detail(request, id):
    note = get_object_or_404(NoteModel, id=id)
    # note = NoteModel.objects.get(id=id)
    if note.user != request.user:
        # return HttpResponseForbidden("You don't have permission to access this note.")
        raise Http404()

    return render(request, 'note_module/note_detail.html', {
        'note': note
    })


class CreateNoteView(View):
    def get(self, request):
        form = NoteForm(user=request.user)
        return render(request, 'note_module/create_note.html', {
            'form': form})

    def post(self, request):
        form = NoteForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            note: NoteModel = NoteModel(user=user, title=form.cleaned_data['title'], text=form.cleaned_data['text'],
                                        category=form.cleaned_data['category'])
            note.save()
            return redirect(reverse('home_page'))


class EditNoteView(View):
    def get(self, request, id):
        note = NoteModel.objects.get(id=id)
        initial_data = {
            'text': note.text,
            'title': note.title,
            'category': note.category
        }
        form = NoteForm(initial=initial_data, user=request.user)

        return render(request, 'note_module/edit_note.html', {
            'form': form,
            'id': note.id
        })

    def post(self, request, id):
        note = NoteModel.objects.get(id=id)
        form = NoteForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            note.title = title = form.cleaned_data['title']
            note.text = form.cleaned_data['text']
            note.category = form.cleaned_data['category']
            note.save()
            return redirect(reverse('home_page'))
        return render(request, 'note_module/edit_note.html', {
            'form': form,
            'id': note.id
        })


def delete_note(request, id):
    note = NoteModel.objects.filter(id=id)
    note.delete()
    return redirect(reverse('home_page'))


class CreateCategoryView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'note_module/create_category.html', {
            'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = CategoryModel(title=form.cleaned_data.get('title'), is_active=True, user=request.user)
            category.save()
            return redirect(reverse('home_page'))
