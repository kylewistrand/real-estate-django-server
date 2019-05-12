from django.contrib import admin
from .models import CouponType, Coupon, PropertyType

# Register your models here.
admin.site.register(CouponType)
admin.site.register(Coupon)
admin.site.register(PropertyType)
