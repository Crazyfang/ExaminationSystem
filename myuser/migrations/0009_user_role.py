# Generated by Django 3.0.3 on 2020-04-09 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0002_role_status'),
        ('myuser', '0008_user_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, help_text='角色', null=True, on_delete=django.db.models.deletion.SET_NULL, to='role.Role', verbose_name='角色'),
        ),
    ]
