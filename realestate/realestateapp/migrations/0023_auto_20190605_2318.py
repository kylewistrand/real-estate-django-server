# Generated by Django 2.2 on 2019-06-06 06:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0022_auto_20190605_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ownership',
            name='coupon_id',
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 6, 5, 23, 18, 12, 821900)),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyCreatedDate',
            field=models.DateField(default=datetime.datetime(2019, 6, 5, 23, 18, 12, 820903)),
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
        migrations.DeleteModel(
            name='CouponType',
        ),
    ]