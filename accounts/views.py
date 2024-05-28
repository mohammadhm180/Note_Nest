from django.contrib.auth import logout, login
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

from .forms import SignupForm, SignInForm, ProfileForm
from .models import UserModel
from utils.email_service import send_email


class SignUpView(View):
    def get(self, request: HttpRequest):
        user_form = SignupForm
        return render(request, 'accounts/signup_page.html', {
            'user_form': user_form
        })

    def post(self, request: HttpRequest):
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data.get('email')
            email_exist = UserModel.objects.filter(email__iexact=email).exists()

            if not email_exist:
                name = user_form.cleaned_data.get('name')
                password = user_form.cleaned_data.get('password')
                email_active_code = get_random_string(75)

                user = UserModel(first_name=name, email=email, email_active_code=email_active_code, is_active=False,
                                 username=email)
                user.set_password(password)
                user.save()
                send_email('تایید ایمیل در سایت NoteNest', email, {
                    'email_active_code': email_active_code
                }, 'emails/email_verification.html')
                return redirect(reverse("signin_page"))
            else:
                user_form.add_error('email', 'حسابی با این ایمیل قبلا ثبت نام کرده است.')
        return render(request, 'accounts/signup_page.html', {
            'user_form': user_form
        })


class SignInView(View):
    def get(self, request):
        user_form = SignInForm

        return render(request, template_name='accounts/signin_page.html', context={
            'user_form': user_form
        })

    def post(self, request):
        user_form = SignInForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')

            user: UserModel = UserModel.objects.filter(email__iexact=email).first()
            if user is not None:
                if user.check_password(password):
                    if user.is_active:
                        login(request, user)
                        return redirect(reverse("home_page"))
                    else:
                        user_form.add_error('email', 'حساب کاربری فعال نشده است.')
                else:
                    user_form.add_error('email', 'ایمیل یا رمز اشتباه است.')
            else:
                user_form.add_error('email', 'ایمیل یا رمز اشتباه است.')

            return render(request, template_name='accounts/signin_page.html', context={
                'user_form': user_form
            })


def sign_out(request):
    logout(request)
    return redirect(reverse('home_page'))


def activate_email(request, email_active_code):
    user: UserModel = UserModel.objects.filter(email_active_code__iexact=email_active_code).first()
    if user is not None:
        user.is_active = True
        user.email_active_code = get_random_string(75)
        user.save()
        login(request, user)
        return redirect(reverse('congrats_page'))
    else:
        raise Http404()


def congrats(request):
    if not request.user.is_authenticated or not request.user.is_active:
        return redirect('signin_page')

    return render(request, 'accounts/congrats_page.html')


class ProfileView(View):
    def get(self, request):
        initial_data={
            'name':request.user.first_name,
            'avatar':request.user.avatar
        }
        form=ProfileForm(initial=initial_data)
        return render(request,'accounts/profile_page.html',{
            'user':request.user,
            'form':form
        })

    def post(self, request):
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            avatar = form.cleaned_data['avatar']
            user=request.user
            if avatar:
                user.avatar = avatar
            user.first_name = name
            user.save()
            return redirect(reverse('profile_page'))

        return render(request,'accounts/profile_page.html',{
            'user':request.user,
            'form':form
        })
