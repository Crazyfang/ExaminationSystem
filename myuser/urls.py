from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('user_list/', views.user_table, name='user_list'),
    path('add/', views.add_user, name='add_user'),
    path('edit/', views.edit_user, name='edit_user'),
    path('del/', views.del_user, name='del_user'),
]
