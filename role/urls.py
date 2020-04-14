from django.urls import path
from . import views


app_name = 'role'
urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('list/', views.role_list, name='role_list'),
    path('add/', views.add_role, name='add_role'),
    path('edit/', views.edit_role, name='edit_role'),
    path('del/', views.del_role, name='del_role'),
    path('roles_button', views.roles_button, name='roles_button'),
    path('role_page_button', views.role_page_button, name='role_page_button'),
]