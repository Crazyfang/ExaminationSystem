from django.db import models


# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=50, verbose_name='角色名称', help_text='角色名称')
    button = models.ManyToManyField('button.Membership', through='RolesButton')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        db_table = 'role'

    def __str__(self):
        return self.role_name


class RolesButton(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    button = models.ForeignKey('button.Membership', on_delete=models.CASCADE, verbose_name='页面按钮')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
