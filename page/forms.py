from django.forms import ModelForm
from .models import Page
from django import forms


class PageAddForm(ModelForm):
    class Meta:
        model = Page
        fields = ['menu_name', 'menu_url', 'parent', 'status', 'order_no']


class PageEditForm(ModelForm):
    class Meta:
        model = Page
        fields = ['menu_name', 'menu_url', 'parent', 'status', 'order_no']
