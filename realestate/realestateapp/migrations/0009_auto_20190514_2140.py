# Generated by Django 2.2.1 on 2019-05-14 21:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('realestateapp', '0008_auto_20190514_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='user',
        ),
        migrations.AddField(
            model_name='offer',
            name='user_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 5, 14, 21, 40, 29, 513534)),
        ),
    ]
