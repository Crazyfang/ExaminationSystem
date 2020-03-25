from django.forms import ModelForm
from django import forms
from .models import User
from captcha.fields import CaptchaField


class UserForm(ModelForm):
    captcha = CaptchaField()
    user_code = forms.CharField(max_length=10, help_text='柜员号')

    class Meta:
        model = User
        fields = ['password']
