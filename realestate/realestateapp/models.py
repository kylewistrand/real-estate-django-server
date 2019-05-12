from django.db import models
import datetime

# Create your models here.
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

# class Property(models.Model):
#     propertyType = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
#     neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
#     propertyAddress = models.CharField(max_length=100)
#     propertyCreatedDate = models.DateField()
#     propertyMarketPrice = models.DecimalField(decimal_places=2)
#     propertyDescription = models.CharField(max_length=512)
#     propertySqFt = models.IntegerField(min_value=0)
#     propertyBedrooms = models.IntegerField(min_value=0)
#     propertyBathrooms = models.IntegerField(min_value=0)

# class Offer(models.Model):
#     propertyBuilding = models.ManyToManyField(Property)
#     offerAmount = models.DecimalField(decimal_places=2, max_digits=6)
#     offerDate = models.DateTimeField(datetime.datetime.now())
    #offerCounter
    #offerDate
    #userID

class Neighborhood(models.Model):
    neighborhood_id = models.AutoField(primary_key=True)
    neighborhood_name = models.CharField(max_length=225)
    neighborhood_desc = models.TextField()

class Property_Photo(models.Model):
    property_photo_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey()
    photo_id = models.ForeignKey()

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    photo_file = models.URLField()
    photo_added_date = models.DateTimeField()

class Property_Amenity(models.Model):
    property_amenity_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey()
    amenity = models.ForeignKey()

class Amenity(models.Model):
    amenity_id = models.AutoField(primary_key=True)
    amenity_name = models.CharField(max_length=225)
    amenity_desc = models.TextField()

