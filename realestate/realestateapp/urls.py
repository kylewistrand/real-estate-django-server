from django.urls import path
from . import views

app_name = 'realestateapp'
urlpatterns = [
        path('coupons', views.coupons, name='coupons'),
<<<<<<< HEAD
        path('properties', views.properties, name='properties')
=======
        path('auth/register', views.register, name='account-create'),
        path('checkout', views.checkout, name="Checkout"),
        path('coupons/<coupon_id>', views.checkout, name="edit-certain-coupon"),
>>>>>>> master
]
