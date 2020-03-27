from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'home'
urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('console/', views.console_view, name='console'),
]