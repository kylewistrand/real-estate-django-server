from django.urls import path
from . import views

app_name = 'realestateapp'
urlpatterns = [
        path('coupons', views.coupons, name='coupons'),
        path('properties', views.properties, name='properties')
]
