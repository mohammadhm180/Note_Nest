from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars/', verbose_name='تصویر', blank=True, null=True)
    email_active_code = models.CharField(max_length=80, verbose_name='کد تایید ایمیل')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.first_name
