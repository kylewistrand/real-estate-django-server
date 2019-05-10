from django.db import models

# Create your models here.


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
