from django.urls import path, include
from . import views

app_name = 'button'
urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('add/', views.add_button, name='add_button'),
    path('edit/', views.edit_button, name='edit_button'),
    path('del/', views.del_button, name='del_button'),
    path('list/', views.button_list, name='button_list'),
    path('button_list/', views.button_distribute, name='button_distribution'),
]
