# Generated by Django 3.0.3 on 2020-04-04 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('page', '0002_auto_20200403_0058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_name', models.CharField(help_text='按钮名称', max_length=50, verbose_name='按钮名称')),
                ('button_type', models.IntegerField(choices=[(1, '表内'), (2, '表外')], default=1, help_text='按钮类型', verbose_name='按钮类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('status', models.IntegerField(choices=[(1, '启用'), (2, '未启用')], default=1, help_text='状态', verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '按钮',
                'db_table': 'button',
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('button', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='button.Button')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page.Page')),
            ],
        ),
        migrations.AddField(
            model_name='button',
            name='belong',
            field=models.ManyToManyField(through='button.Membership', to='page.Page'),
        ),
    ]
