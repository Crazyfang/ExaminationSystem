from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'user'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
]