from django import forms
from django.forms import ModelForm
from .models import Button


class ButtonAddForm(ModelForm):
    class Meta:
        model = Button
        fields = ['button_name', 'button_type', 'status']


class ButtonEditForm(ModelForm):
    class Meta:
        model = Button
        fields = ['button_name', 'button_type', 'status']
