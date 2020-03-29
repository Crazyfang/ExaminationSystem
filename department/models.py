from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Department(models.Model):
    department_name = models.CharField(max_length=50, verbose_name=_('部门名称'))
    department_code = models.CharField(max_length=10, verbose_name=_('部门代码'))
    parent_department = models.ForeignKey('self', null=True, blank=True, default=None,
                                          on_delete=models.SET_NULL, verbose_name=_('上级部门'))
    create_time = models.DateTimeField(verbose_name=_('创建时间'), auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=_('修改时间'), auto_now=True)

    class Meta:
        db_table = 'department'
        verbose_name_plural = _('部门信息')
        ordering = ['department_code']

    def __str__(self):
        return '{0}-{1}'.format(self.department_code, self.department_name)
