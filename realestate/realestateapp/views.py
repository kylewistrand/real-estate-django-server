from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Coupon, CouponType, Property, PropertyType, Neighborhood, Ownership
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import RegistrationForm
from .models import Property

# Create your views here.
@csrf_exempt
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
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponse("Error decoding JSON file.", status=400)
        else:
            try:
                couponT = CouponType()
                couponT.couponTypeName = data['couponTypeName']
                couponT.couponTypeDescription = data['couponTypeDescription']
                couponT.save()
            except:
                couponT = CouponType.objects.get(couponTypeName=data['couponTypeName'])
            newCoupon = Coupon()
            newCoupon.couponValue = data['couponValue']
            newCoupon.couponName = data['couponName']
            newCoupon.couponDescription = data['couponDescription']
            newCoupon.couponType = couponT
            newCoupon.save()
            couponJSON = {
                "couponName":newCoupon.couponName,
                "couponValue":newCoupon.couponValue,
                "couponDescription":newCoupon.couponDescription,
                "couponTypeName":newCoupon.couponType.couponTypeName,
                "couponTypeDescription":newCoupon.couponType.couponTypeDescription
            }
            return JsonResponse(couponJSON, status=200)
    elif request.method == 'DELETE':
        coupons = Coupon.objects.all()
        for coupon in coupons:
            coupon.delete()
        return HttpResponse("All coupons were deleted.", status=200)

@csrf_exempt
def properties(request):
    if request.method == 'GET':
        ownProperties = Ownership.objects.filter(user_id=request.user)
        propertiesList = []
        for ownership in ownProperties:
            prop = ownership.property_id
            propertyTemp = {
                "propertyType":prop.propertyType,
                "neighborhood":prop.neighborhood,
                "propertyAddress":prop.propertyAddress,
                "propertyCreatedDate":prop.propertyCreatedDate,
                "propertyMarketPrice":prop.propertyMarketPrice,
                "propertyDescription":prop.propertyDescription,
                "propertySqFt":prop.propertySqFt,
                "propertyBedrooms":prop.propertyBedrooms,
                "propertyBathrooms":prop.propertyBathrooms
            }
            propertiesList.append(propertyTemp)
        return JsonResponse(propertiesList, status=200)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponse("Error decoding JSON file.", status=400)
        else:
            try:
                propertyT = PropertyType()
                propertyT.propertyTypeName = data['propertyTypeName']
                propertyT.propertyTypeDescription = data['propertyTypeDescription']
                propertyT.save()
            except:
                propertyT = PropertyType.objects.get(couponTypeName=data['propertyTypeName'])
            try:
                neighborhood = Neighborhood()
                neighborhood.neighbordhood_name = data['NeighborhoodName']
                neighborhood.neighbordhood_desc = data['NeighborhoodDescription']
                neighborhood.save()
            except:
                neighborhood = neighborhood.objects.get(neighborhood_name=data['NeighborhoodName'])
            propTemp = Property()
            propTemp.neighborhood = neighborhood
            propTemp.propertyType = propertyT
            propTemp.propertyAddress = data['propertyAddress']
            propTemp.propertyMarketPrice = data['propertyMarketPrice']
            propTemp.propertyDescription = data['propertyDescription']
            propTemp.propertySqFt = data['propertySqFt']
            propTemp.propertyBedrooms = data['propertyBedrooms']
            propTemp.propertyBathrooms = data['propertyBathrooms']
            propTemp.save()
            propertyJSON = {
                "propertyType":propTemp.propertyType,
                "neighborhood":propTemp.neighborhood,
                "propertyAddress":propTemp.propertyAddress,
                "propertyCreatedDate":propTemp.propertyCreatedDate,
                "propertyMarketPrice":propTemp.propertyMarketPrice,
                "propertyDescription":propTemp.propertyDescription,
                "propertySqFt":propTemp.propertySqFt,
                "propertyBedrooms":propTemp.propertyBedrooms,
                "propertyBathrooms":propTemp.propertyBathrooms
            }
            return JsonResponse(propertyJSON, status=200)
    elif request.method == 'DELETE':
        ownProperties = Ownership.objects.filter(user_id=request.user)
        for ownership in ownProperties:
            ownership.property_id.delete()
        return HttpResponse("All of your properties were deleted.", status=200)
        
def register(request):
    "Registers a user"

    if request.method == 'GET':
        return render(request, 'auth/register.html', { })

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

def checkout(request):
    "Allows user to checkout items from their cart"

    if User.is_authenticated():
        if request.method == "GET":
            cartItems = Property.objects.all()
            cartItemList = []
            for cartItem in cartItems:
                cartTemp = {
                    "property_name":cartItem.couponName,
                    "proptery_price":cartItem.couponValue,
                    "property_description":cartItem.couponDescription,
                    "property_sqfoot":cartItem.couponType.couponTypeName,

                }
                cartItem.append(cartTemp)
            return JsonResponse(cartItemList, safe=False, status=200)
    
        if request.method == "POST":
            return HttpResponse("Items Purchesed", status=201)

        if request.method == "DELETE":
            return HttpResponse("Delete cart item")

def coupon_with_id(request):
    "Allows admin user to edit, delete a certain coupon"
    
    if User.is_superuser():
        if request.method == "GET":
            return NotImplemented
        if request.method == "POST":
            return NotImplemented
        if request.method == "DELETE":
            return NotImplemented
