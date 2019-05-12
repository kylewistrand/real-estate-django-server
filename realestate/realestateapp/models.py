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
#     propertyMarketPrice = models.DecimalField(decimal_places=2, max_digits=6)
#     propertyDescription = models.CharField(max_length=512)
#     propertySqFt = models.CharField(max_length=10)
#     propertyBedrooms = models.CharField(max_length=10)
#     propertyBathrooms = models.CharField(max_length=10)

# class Offer(models.Model):
#     propertyBuilding = models.ManyToManyField(Property)
#     offerAmount = models.DecimalField(decimal_places=2, max_digits=6)
#     offerDate = models.DateTimeField(datetime.datetime.now())
    #offerCounter
    #offerDate
    #userID
