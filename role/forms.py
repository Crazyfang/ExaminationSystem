from django.forms import ModelForm
from .models import Role


class RoleAddForm(ModelForm):
    class Meta:
        model = Role
        fields = ['role_name']


class RoleEditForm(ModelForm):
    class Meta:
        model = Role
        fields = ['role_name']
