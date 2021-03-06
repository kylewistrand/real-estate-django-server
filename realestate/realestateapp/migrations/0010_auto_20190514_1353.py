# Generated by Django 2.2 on 2019-05-14 20:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0009_auto_20190514_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='amenity_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='couponDescription',
            field=models.CharField(blank=True, default='Generic coupon.', max_length=250),
        ),
        migrations.AlterField(
            model_name='coupontype',
            name='couponTypeDescription',
            field=models.CharField(blank=True, default='Not specified.', max_length=250),
        ),
        migrations.AlterField(
            model_name='neighborhood',
            name='neighborhood_desc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerAmount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerCounter',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerDate',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 14, 13, 53, 45, 968669)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_file',
            field=models.URLField(blank=True, default='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyBathrooms',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyBedrooms',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyCreatedDate',
            field=models.DateField(default=datetime.datetime(2019, 5, 14, 13, 53, 45, 967673)),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyDescription',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyMarketPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertySqFt',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='propertytype',
            name='propertyTypeDescription',
            field=models.CharField(blank=True, default='Not classified property', max_length=512),
        ),
    ]
