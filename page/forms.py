from django.forms import ModelForm
from .models import Page
from django import forms


class PageAddForm(ModelForm):
    class Meta:
        model = Page
        fields = ['menu_name', 'menu_url', 'parent', 'status', 'order_no', 'menu_code', 'menu_icon']


class PageEditForm(ModelForm):
    class Meta:
        model = Page
        fields = ['menu_name', 'menu_url', 'parent', 'status', 'order_no', 'menu_code', 'menu_icon']
