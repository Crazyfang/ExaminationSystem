from django.urls import path, include
from . import views


app_name = 'department'
urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('list/', views.department_list, name='department_list'),
    path('add_view/<int:parent_department>/', views.create_view, name='create_view'),
    path('add/', views.create_department, name='create_department'),
]