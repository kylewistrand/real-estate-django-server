# Generated by Django 2.2 on 2019-05-12 22:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0005_auto_20190512_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='couponDescription',
            field=models.CharField(default='', max_length=250, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='couponName',
            field=models.CharField(default='', max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='couponValue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, unique=True),
        ),
        migrations.AlterField(
            model_name='coupontype',
            name='couponTypeDescription',
            field=models.CharField(default='', max_length=250, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerAmount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, unique=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 5, 12, 15, 20, 20, 358302)),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyAddress',
            field=models.CharField(default='', max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyBathrooms',
            field=models.PositiveSmallIntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyBedrooms',
            field=models.PositiveSmallIntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyDescription',
            field=models.CharField(default='', max_length=512, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyMarketPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertySqFt',
            field=models.PositiveSmallIntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='propertytype',
            name='propertyTypeDescription',
            field=models.CharField(default='', max_length=512, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='propertytype',
            name='propertyTypeName',
            field=models.CharField(default='', max_length=100, null=True, unique=True),
        ),
    ]