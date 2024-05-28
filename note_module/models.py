from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from accounts.models import UserModel


class CategoryModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='ایجاد کننده')
    title = models.CharField(max_length=40, verbose_name='عنوان')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class NoteModel(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE,verbose_name='نویسنده')
    title = models.TextField(verbose_name='عنوان یادداشت')
    text = models.TextField(verbose_name='متن', db_index=True)
    category = models.ForeignKey(CategoryModel, related_name='note_category',on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده/ نشده')
    slug = models.SlugField(db_index=True, verbose_name='عنوان در url', max_length=200, blank=True, unique=True)
    create_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = unidecode(self.title)
            self.slug = slugify(value)
            if NoteModel.objects.filter(slug=self.slug).exists():
                base_slug = self.slug
                counter = 1
                while NoteModel.objects.filter(slug=self.slug).exists():
                    self.slug = f'{base_slug}-{counter}'
                    counter += 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'یادداشت'
        verbose_name_plural = 'یادداشت ها'

    def __str__(self):
        return self.text
