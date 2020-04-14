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


class UserFormRegister(ModelForm):
    captcha = CaptchaField()
    # gender = forms.ChoiceField()
    # gender = forms.Select(attrs={'id': 'LAY-user-login-gender'}, choices=((1, '男'), (2, '女')))

    class Meta:
        model = User
        fields = ['user_code', 'password', 'username', 'gender']
        widgets = {
            'gender': forms.Select(attrs={'id': 'LAY-user-login-gender'})
        }


class UserFormAdd(ModelForm):
    class Meta:
        model = User
        fields = ['user_code', 'username', 'gender', 'department', 'role']
        error_messages = {
            'user_code': {
                'unique': "存在具有相同柜员号的用户",
            },
        }


class UserFormEdit(ModelForm):
    user_code = forms.CharField(max_length=10, help_text='柜员号')

    class Meta:
        model = User
        fields = ['username', 'gender', 'department', 'role']
