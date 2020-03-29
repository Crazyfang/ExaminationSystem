# Generated by Django 3.0.3 on 2020-03-29 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
        ('myuser', '0005_auto_20200325_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.Department'),
        ),
    ]
