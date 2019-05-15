# Generated by Django 2.2 on 2019-05-14 23:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0015_auto_20190514_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='couponDescription',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 5, 14, 16, 49, 55, 407223)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_file',
            field=models.URLField(default='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyCreatedDate',
            field=models.DateField(default=datetime.datetime(2019, 5, 14, 16, 49, 55, 407223)),
        ),
        migrations.AlterField(
            model_name='role',
            name='roleDescription',
            field=models.CharField(choices=[('ADMIN', 'Administrative controls'), ('SELLER', 'Sells properties'), ('USER', 'General user')], default='USER', max_length=6),
        ),
        migrations.AlterField(
            model_name='role',
            name='roleName',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('SELLER', 'SELLER'), ('USER', 'USER')], default='USER', max_length=6),
        ),
    ]