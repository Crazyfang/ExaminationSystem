# Generated by Django 3.0.3 on 2020-02-07 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(1, '男'), (2, '女')], default=1),
        ),
    ]
