from django.db import models
from django.contrib.auth.models import User
import datetime

class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userPicture = models.ImageField(upload_to = 'user_pics/', blank=True, default = 'user_pics/None/no-img.jpg')
    userDesc = models.TextField(max_length=1000, blank=True , default = 'This user has no description yet.')

class Role(models.Model):
    roleName = models.CharField(max_length=30, blank=False)
    roleDescription = models.CharField(max_length=250, blank=True)

class User_Role(models.Model):
    user_id = models.ForeignKey(User, blank=False)
    role_id = models.ForeignKey(Role, blank=False)
    beginDate = models.DateTimeField(blank=False, default=datetime.now)
    endDate = models.DateTimeField(blank=True, null=True)

class Ownership(models.Model):
    user_id = models.ForeignKey(User, blank=False)
    property_id = models.ForeignKey(Property, blank=False)
    coupon_id = models.ForeignKey(Coupon, blank=False)
    ownershipBeginDate = models.DateTimeField(blank=False, default=datetime.now)
    ownershipEndDate = models.DateTimeField(blank=True, null=True)
    ownershipAskingPrice = models.DecimalField(max_digits=12, decimal_places=2)
    ownershipPaidPrice = models.DecimalField(max_digits=12, decimal_places=2)

class Cart(models.Model):
    user_id = models.ForeignKey(User)
    property_id = models.ForeignKey(Property)
    cartAddedDate = models.DateTimeField(blank=False, default=datetime.now)
    cartRemovedDate = models.DateTimeField(blank=True, null=True)

class Neighborhood(models.Model):
    neighborhood_id = models.AutoField(primary_key=True)
    neighborhood_name = models.CharField(max_length=225)
    neighborhood_desc = models.TextField()

class CouponType(models.Model):
    couponTypeName = models.CharField(max_length=30, default="", unique=True, null=True)
    couponTypeDescription = models.CharField(max_length=250, default="", unique=True, null=True)

class Coupon(models.Model):
    couponType = models.ForeignKey(CouponType, on_delete=models.CASCADE)
    couponValue = models.DecimalField(decimal_places=2, max_digits=3, default=0, unique=True, null=False)
    couponName = models.CharField(max_length=100, default="", unique=True, null=True)
    couponDescription = models.CharField(max_length=250, default="", unique=True, null=True)

class PropertyType(models.Model):
    propertyTypeName = models.CharField(max_length=100, default="", unique=True, null=True)
    propertyTypeDescription = models.CharField(max_length=512, default="", unique=True, null=True)

class Property(models.Model):
    propertyType = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    propertyAddress = models.CharField(max_length=100, default="", unique=True, null=True)
    propertyCreatedDate = models.DateField()
    propertyMarketPrice = models.DecimalField(decimal_places=2, max_digits=9, default=0, unique=True, null=True)
    propertyDescription = models.CharField(max_length=512, default="", unique=True, null=True)
    propertySqFt = models.PositiveSmallIntegerField(default=0, unique=True, null=False)
    propertyBedrooms = models.PositiveSmallIntegerField(default=0, unique=True, null=False)
    propertyBathrooms = models.PositiveSmallIntegerField(default=0, unique=True, null=False)

class Offer(models.Model):
    propertyBuilding = models.ManyToManyField(Property)
    user = models.ManyToManyField(User)
    offerAmount = models.DecimalField(decimal_places=2, max_digits=9, default=0, unique=True, null=False)
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

