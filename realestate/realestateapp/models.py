from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Neighborhood(models.Model):
    neighborhood_id = models.AutoField(primary_key=True)
    neighborhood_name = models.CharField(max_length=225)
    neighborhood_desc = models.TextField()

class CouponType(models.Model):
    couponTypeName = models.CharField(max_length=30)
    couponTypeDescription = models.CharField(max_length=250)

class Coupon(models.Model):
    couponType = models.ForeignKey(CouponType, on_delete=models.CASCADE)
    couponValue = models.DecimalField(decimal_places=2, max_digits=3)
    couponName = models.CharField(max_length=100)
    couponDescription = models.CharField(max_length=250)

class PropertyType(models.Model):
    propertyTypeName = models.CharField(max_length=100)
    propertyTypeDescription = models.CharField(max_length=512)

class Property(models.Model):
    propertyType = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    propertyAddress = models.CharField(max_length=100)
    propertyCreatedDate = models.DateField()
    propertyMarketPrice = models.DecimalField(decimal_places=2, max_digits=9)
    propertyDescription = models.CharField(max_length=512)
    propertySqFt = models.IntegerField()
    propertyBedrooms = models.IntegerField()
    propertyBathrooms = models.IntegerField()

class Offer(models.Model):
    propertyBuilding = models.ManyToManyField(Property)
    user = models.ManyToManyField(User)
    offerAmount = models.DecimalField(decimal_places=2, max_digits=9)
    offerDate = models.DateTimeField(datetime.datetime.now())
    #offerCounter
    #offerCounterDate

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    photo_file = models.URLField()
    photo_added_date = models.DateTimeField()

class Property_Photo(models.Model):
    property_photo_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE)

class Amenity(models.Model):
    amenity_id = models.AutoField(primary_key=True)
    amenity_name = models.CharField(max_length=225)
    amenity_desc = models.TextField()

class Property_Amenity(models.Model):
    property_amenity_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

