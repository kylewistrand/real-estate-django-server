# Generated by Django 2.2 on 2019-05-15 00:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0016_auto_20190514_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='offerDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 5, 14, 17, 2, 48, 740092)),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='coupon_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='realestateapp.Coupon'),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyCreatedDate',
            field=models.DateField(default=datetime.datetime(2019, 5, 14, 17, 2, 48, 740092)),
        ),
    ]
