from django.urls import path
from . import views

app_name = 'realestateapp'
urlpatterns = [
        path('coupons', views.coupons, name='coupons'),
        path('auth/register', views.register, name='account-create'),
        path('checkout', views.checkout, name="Checkout")
]
