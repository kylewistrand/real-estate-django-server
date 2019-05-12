from django.contrib import admin
from .models import CouponType, Coupon, PropertyType, Property, Neighborhood,
Offer, Photo, Property_Amenity, Property_Photo, Amenity

# Register your models here.
admin.site.register(CouponType)
admin.site.register(Coupon)
admin.site.register(PropertyType)
admin.site.register(Property)
admin.site.register(Neighborhood)
admin.site.register(Offer)
admin.site.register(Photo)
admin.site.register(Property_Photo)
admin.site.register(Amenity)
admin.site.register(Property_Amenity)