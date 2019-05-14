from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Coupon, CouponType
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import RegistrationForm

# Create your views here.
def coupons(request):
    if request.method == 'GET':
        coupons = Coupon.objects.all()
        couponsList = []
        for coupon in coupons:
            couponTemp = {
                "couponName":coupon.couponName,
                "couponValue":coupon.couponValue,
                "couponDescription":coupon.couponDescription,
                "couponTypeName":coupon.couponType.couponTypeName,
                "couponTypeDescription":coupon.couponType.couponTypeDescription
            }
            couponsList.append(couponTemp)
        return JsonResponse(couponsList, safe=False, status=200)
    # elif request.method == 'POST':
    # elif request.method == 'DELETE':



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            passwordConf = form.cleaned_data['passwordConf']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
                
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if password == passwordConf:
                return HttpResponse("User Registered ")
            else:
                return HttpResponse("Passwords do not match", status=400)   
        else:
            return HttpResponse("Invalid registration request.(Bad Request)", status=400)

    else:
        form = RegistrationForm      
        return HttpResponse("Method not allowed on /auth/register.(Method Not Allowed)", status=405)

