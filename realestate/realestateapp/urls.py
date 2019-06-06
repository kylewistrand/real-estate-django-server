from django.urls import path
from . import views

app_name = 'realestateapp'
urlpatterns = [
        # path('coupons', views.coupons, name='coupons'),
        path('properties', views.properties, name='properties'),
        path('properties/<property_id>', views.specificProperty, name='specificProperty'),
        path('auth/register', views.register, name='account-create'),
        path('auth/signin', views.signin, name='Signin'),
        path('checkout', views.checkout, name="Checkout"),
        path('offers', views.offers, name="Offers"),
        # path('livability', views.getLivability, name="Livability"),
        # path('coupons/<coupon_id>', views.checkout, name="edit-certain-coupon"),
        path('users/<int:user_id>', views.specificUser, name="specificUser"),
]
