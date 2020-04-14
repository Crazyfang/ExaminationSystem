from django.db import models


# Create your models here.
class Button(models.Model):
    TYPE_CHOICES = [
        (1, '表内'),
        (2, '表外')
    ]
    STATUS_CHOICES = [
        (1, '启用'),
        (2, '未启用')
    ]
    button_name = models.CharField(max_length=50, verbose_name='按钮名称', help_text='按钮名称')
    button_type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name='按钮类型', help_text='按钮类型')
    button_code = models.CharField(max_length=50, verbose_name='按钮代码', help_text='按钮代码')
    button_icon = models.CharField(max_length=100, verbose_name='按钮图标', help_text='按钮图标', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态', help_text='状态')
    belong = models.ManyToManyField('page.Page', through='Membership')

    class Meta:
        db_table = 'button'
        verbose_name_plural = '按钮'

    def __str__(self):
        return self.button_name + '——' + str(self.button_type)


class Membership(models.Model):
    page = models.ForeignKey('page.Page', on_delete=models.CASCADE)
    button = models.ForeignKey(Button, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
