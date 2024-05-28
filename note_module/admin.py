from django.contrib import admin
from .models import NoteModel,CategoryModel
# Register your models here.


admin.site.register(NoteModel)
admin.site.register(CategoryModel)
