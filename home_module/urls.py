from django.urls import path
from . import views
urlpatterns=[
    path('',views.home_page,name='home_page'),
    path('get_notes/<int:category_id>/', views.get_notes, name='get_notes'),
]