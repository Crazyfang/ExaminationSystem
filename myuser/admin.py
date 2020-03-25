from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_code', 'username', 'gender', 'is_active')
    search_fields = ['user_code']
    list_filter = ['last_login']


admin.site.register(User, UserAdmin)
