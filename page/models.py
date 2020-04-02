from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Page(models.Model):
    STATUS_CHOICES = [
        (1, '启用'),
        (2, '未启用'),
    ]
    menu_name = models.CharField(max_length=50, verbose_name='菜单名称', help_text='菜单名称')
    menu_url = models.CharField(max_length=200, verbose_name='链接', help_text='链接')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态', help_text='状态')
    order_no = models.IntegerField(default=1, verbose_name='排序号', help_text='排序号')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True,
                               verbose_name='上级菜单', help_text='上级菜单')

    class Meta:
        db_table = 'page'
        verbose_name_plural = _('部门信息')

    def __str__(self):
        return self.menu_name
