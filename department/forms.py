from django.forms import ModelForm
from django import forms
from .models import Department


class DepartmentCreateForm(ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'department_code']


class DepartmentEditForm(ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'department_code', 'parent_department']
