from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup_page'),
    path('signin/', views.SignInView.as_view(), name='signin_page'),
    path('sign_out/', views.sign_out, name='sign_out_page'),
    path('activate_email/<email_active_code>/', views.activate_email, name='activate_email'),
    path('congrats/', views.congrats, name='congrats_page'),
    path('profile_page/', views.ProfileView.as_view(), name='profile_page'),

]
