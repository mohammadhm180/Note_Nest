from django.urls import path
from . import views

urlpatterns = [
    path('note_detail/<int:id>/', views.note_detail, name='note_detail'),
    path('create_note/', views.CreateNoteView.as_view(), name='create_note'),
    path('edit_note/<int:id>/', views.EditNoteView.as_view(), name='edit_note'),
    path('delete_note/<int:id>/', views.delete_note, name='delete_note'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
]
