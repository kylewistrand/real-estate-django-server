from django.db import models, IntegrityError
from django.contrib.auth.models import User
import datetime

class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userPicture = models.ImageField(upload_to = 'user_pics/', blank=True, default = 'user_pics/None/no-img.jpg')
    userDesc = models.TextField(max_length=1000, blank=True , default = 'This user has no description yet.')

class Role(models.Model):
    ADMIN = 'ADMIN'
    SELLER = 'SELLER'
    USER = 'USER'
    roleChoices = (
        (ADMIN, 'ADMIN'),
        (SELLER, 'SELLER'),
        (USER, 'USER')
    )
    roleDescription = (
        (ADMIN, 'Administrative controls'),
        (SELLER, 'Sells properties'),
        (USER, 'General user')
    )
    roleName = models.CharField(max_length=6, choices=roleChoices, default='USER')
    roleDescription = models.CharField(max_length=6, choices=roleDescription, default='USER')

class User_Role(models.Model):
    user_id = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, blank=False, on_delete=models.CASCADE)
    beginDate = models.DateTimeField(blank=False, default=datetime.datetime.now)
    endDate = models.DateTimeField(blank=True, null=True)

class Neighborhood(models.Model):
    neighborhood_id = models.AutoField(primary_key=True)
    neighborhood_name = models.CharField(max_length=225, blank=False)
    neighborhood_desc = models.TextField(default="", blank=True, unique=False)

class CouponType(models.Model):
    couponTypeName = models.CharField(max_length=30, default="General", unique=True, blank=False)
    couponTypeDescription = models.CharField(max_length=250, default="Not specified.", unique=False, blank=True)

class Coupon(models.Model):
    couponType = models.ForeignKey(CouponType, on_delete=models.CASCADE)
    couponValue = models.DecimalField(decimal_places=2, max_digits=3, default=0, unique=False, null=False)
    couponName = models.CharField(max_length=30, default="Generic", unique=True, blank=False)
    couponDescription = models.CharField(max_length=250, default="", unique=False, blank=True)

    #Will not save if coupon is not unique
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise IntegrityError

class PropertyType(models.Model):
    propertyTypeName = models.CharField(max_length=50, default="Unclassified", unique=True, blank=False)
    propertyTypeDescription = models.CharField(max_length=512, default="Not classified property", unique=False, blank=True)

class Property(models.Model):
    propertyType = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    propertyAddress = models.CharField(max_length=100, unique=True, null=False, default="Address not given")
    propertyCreatedDate = models.DateField(default=datetime.datetime.now())
    propertyMarketPrice = models.DecimalField(decimal_places=2, max_digits=9, default=0, unique=False, null=False)
    propertyDescription = models.CharField(max_length=512, default="", unique=False, blank=True)
    propertySqFt = models.PositiveSmallIntegerField(default=0, unique=False, null=False)
    propertyBedrooms = models.PositiveSmallIntegerField(default=0, unique=False, null=False)
    propertyBathrooms = models.PositiveSmallIntegerField(default=0, unique=False, null=False)

    #Property is not unique, such as address
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise IntegrityError

class Offer(models.Model):
    propertyBuilding = models.ManyToManyField(Property)
    user_id = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    offerAmount = models.DecimalField(decimal_places=2, max_digits=12, default=0, null=False)
    offerDate = models.DateTimeField(datetime.datetime.now())
    offerCounterAmount = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    offerCounterDate = models.DateTimeField(blank=True, null=True)

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    photo_file = models.URLField(unique=False, null=True, default="https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg")
    photo_added_date = models.DateTimeField(default=datetime.datetime.now)

class Property_Photo(models.Model):
    property_photo_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE)

class Amenity(models.Model):
    amenity_id = models.AutoField(primary_key=True)
    amenity_name = models.CharField(max_length=225, unique=False, blank=False)
    amenity_desc = models.TextField(unique=False, blank=True, default="")

class Property_Amenity(models.Model):
    property_amenity_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    cartAddedDate = models.DateTimeField(blank=False, default=datetime.datetime.now)
    cartRemovedDate = models.DateTimeField(blank=True, null=True)

class Ownership(models.Model):
    user_id = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, blank=False, on_delete=models.CASCADE)
    coupon_id = models.ForeignKey(Coupon, null=True, on_delete=models.CASCADE)
    ownershipBeginDate = models.DateTimeField(blank=False, default=datetime.datetime.now)
    ownershipEndDate = models.DateTimeField(blank=True, null=True)
    ownershipAskingPrice = models.DecimalField(max_digits=12, decimal_places=2)
    ownershipPaidPrice = models.DecimalField(max_digits=12, decimal_places=2)

