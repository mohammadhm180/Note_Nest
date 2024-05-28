from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator

from .models import UserModel


class SignInForm(forms.Form):
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={
        'placeholder': 'ایمیل را وارد کنید.'
    }))
    password = forms.CharField(label='پسوورد', widget=forms.TextInput(attrs={
        'placeholder': 'رمز را وارد کنید.'
    }))


class SignupForm(forms.Form):
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={
        'placeholder': 'ایمیل را وارد کنید.'
    }))

    name = forms.CharField(label='نام', widget=forms.TextInput(attrs={
        'placeholder': 'نام خود را وارد کنید.'
    }))

    password = forms.CharField(label='پسوورد', widget=forms.TextInput(attrs={
        'placeholder': 'رمز را وارد کنید.'
    }), validators=[validators.MinLengthValidator(8)])

    repeated_password = forms.CharField(label='پسوورد', widget=forms.TextInput(attrs={
        'placeholder': 'رمز را دوباره وارد کنید.'
    }),validators=[validators.MinLengthValidator(8)])

    def clean_repeated_password(self):
        password=self.cleaned_data.get('password')
        repeated_password=self.cleaned_data.get('repeated_password')
        if  password== repeated_password:
            return repeated_password
        raise ValidationError('رمزهای وارد شده باهم مطابقت ندارند.')


class ProfileForm(forms.Form):
    name = forms.CharField(label='نام', widget=forms.TextInput(attrs={
        'placeholder': 'نام خود را وارد کنید.'
    }))
    avatar=forms.ImageField(label='تصویر پروفایل',required=False,widget=forms.FileInput())



