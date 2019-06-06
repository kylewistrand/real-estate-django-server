# Generated by Django 2.2.1 on 2019-06-06 08:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0027_merge_20190606_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='offerDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 6, 6, 8, 27, 55, 952492)),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyCreatedDate',
            field=models.DateField(default=datetime.datetime(2019, 6, 6, 8, 27, 55, 951923)),
        ),
    ]
