from django.urls import path
from . import views


app_name = 'role'
urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('add/', views.add_role, name='add_role'),
    path('edit/', views.edit_role, name='edit_role'),
    path('del/', views.del_role, name='del_role'),
]