from django.urls import path, include
from . import views

app_name = 'page'
urlpatterns = [
    path('index/', views.index_view, name='index_view'),
    path('page_list/', views.page_list, name='get_page_list'),
    path('edit/', views.edit_page, name='edit_page'),
    path('add/', views.add_page, name='add_page'),
    path('del/', views.del_page, name='del_page'),
    path('page_tree/', views.page_tree, name='page_tree')
]
