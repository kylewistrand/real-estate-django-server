from django.db import models

# Create your models here.


class Neighborhood(models.Model):
    neighborhood_id = models.AutoField(primary_key=True)
    neighborhood_name = models.CharField(max_length=225)
    neighborhood_desc = models.TextField()


class Property_Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    photo_file = models.URLField()
    photo_added_date = models.DateTimeField()

