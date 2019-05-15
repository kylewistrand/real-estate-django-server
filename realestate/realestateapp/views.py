from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import (Coupon, CouponType, Property, PropertyType, Neighborhood, Ownership, Cart,
Photo, Property_Photo, Amenity, Property_Amenity, Offer, Role, User_Role)
from django.views.decorators.csrf import csrf_exempt
import json, hashlib
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from .forms import RegistrationForm
from django.views.decorators.debug import sensitive_post_parameters

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

@sensitive_post_parameters('username', 'password')
def signin(request):
    """
    If method is GET:
        Returns sign in page
    If method is POST:
        Validates input, signs user in, and redirects to home.
        If input is invalud, returns 400
        If user doesn't exist, returns 401
    If other method:
        Returns status 405
    """
    if request.method == 'GET':
        from realestateapp.forms import SigninForm
        return render(request, 'auth/signin.html', {"signinForm" : SigninForm})
    elif request.method == 'POST':
        # Get POST parameters, clean them and save them as variables for readability
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        # Validate user input, otherwise return 400
        if len(username) < 1 \
            or len(password) < 1:
            return HttpResponse("Bad login form.", status=400)

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Respond after successful login
            return HttpResponse("Login successful.", status=200)
        else:
            return HttpResponse("Invalid credentials.", status=401)
    else:
        # Unsupported method
        return HttpResponse("Method not allowed on realestateapp/auth/signin.", status=405)

@csrf_exempt
def specificUser(request, user_id):
    """
    If method is GET:
        Returns page with information of user of given ID
        If user of given ID does not exist, returns 404
    If other method:
        Returns status 405
    """
    if not request.user.is_authenticated:
        # User is not authenticated
        return HttpResponseRedirect('auth/signin')
    if request.method == 'GET':
        try:
            userInfo = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponse("User "+str(user_id)+"  Not Found.",status=404)

        # Get email hash for gravitar and append it to the gravitar URL
        emailHash = hashlib.md5(userInfo.email.lower().encode('utf-8')).hexdigest()
        gravatar_url = "https://www.gravatar.com/avatar/" + emailHash

        return render(request, 'main/specificUser.html', {
                'user': userInfo,
                'gravatarURL': gravatar_url,
                'roles': Role.objects.all()
            }
        )
    if request.method == 'POST':
        try:
            isAdmin = User_Role.objects.get(user_id=request.user).role_id.roleName == 'Admin'
        except:
            return HttpResponse("User has no role.",status=403)
        isSelf = user_id == request.user.id
        if isAdmin or isSelf:
            try:
                userRole = User_Role.objects.filter(endDate__isnull=True).get(user_id=user_id)
                newRole = Role.objects.get(roleName=request.POST['role'])
                userRole.endDate = datetime.now()
                userRole.save()
                newOffer = User_Role.objects.create(
                    user_id=User.objects.get(pk=user_id),
                    role_id=newRole
                )
                return HttpResponse("User "+str(user_id)+"  Deleted.",status=202)
            except User.DoesNotExist:
                return HttpResponse("User "+str(user_id)+"  Does Not Exist.",status=404)
        else:
            return HttpResponse("Only admins may delete other users.",status=403)
    if request.method == 'DELETE':
        try:
            isAdmin = User_Role.objects.get(user_id=request.user).role_id.roleName == 'Admin'
        except:
            return HttpResponse("User has no role.",status=403)
        isSelf = user_id == request.user.id
        if isAdmin or isSelf:
            try:
                User.objects.get(pk=user_id).delete()
                return HttpResponse("User "+str(user_id)+"  Deleted.",status=202)
            except User.DoesNotExist:
                return HttpResponse("User "+str(user_id)+"  Does Not Exist.",status=404)
        else:
            return HttpResponse("Only admins may delete other users.",status=403)
    else:
        # Unsupported method
        return HttpResponse("Method not allowed on realestateapp/users/.", status=405)


@csrf_exempt
def offers(request):
    """
    If method is GET:
        Validates that a user is properly authenticated
        Returns a list of all current and past offers
    If method is POST:
        Validates that a user is properly authenticated
        Makes an offer for a property
        If input is invalud, returns 400
    If method is PATCH:
        Validates that a user is properly authenticated
        Edit your own offer or create a counter offer
    If other method:
        Returns status 405
    """
    if not request.user.is_authenticated:
        # User is not authenticated
        return HttpResponseRedirect('auth/signin')
    if request.method == 'GET':
        offers = Offer.objects.all()
        offersList = []
        for offer in offers:
            properties = offer.propertyBuilding.all()
            propertiesList = []
            if (request.user == offer.user_id):
                for propertyBuilding in properties:
                    propertyTemp ={
                        "property_id": propertyBuilding.id,
                        "propertyAddress": propertyBuilding.propertyAddress,
                        "propertyCreatedDate": propertyBuilding.propertyCreatedDate,
                        "propertyMarketPrice": propertyBuilding.propertyMarketPrice,
                        "propertyDescription": propertyBuilding.propertyDescription,
                        "propertySqFt": propertyBuilding.propertySqFt,
                        "propertyBedrooms": propertyBuilding.propertyBedrooms,
                        "propertyBathrooms": propertyBuilding.propertyBathrooms
                    }
                    propertiesList.append(propertyTemp)

                offerTemp = {
                    "offerAmount": offer.offerAmount,
                    "offerDate": offer.offerDate,
                    "offerCounterAmount": offer.offerCounterAmount,
                    "offerCounterDate": offer.offerCounterDate,
                    "properties": propertiesList
                }
                offersList.append(offerTemp)
        return JsonResponse(offersList, safe=False, status=200)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponse("Error decoding JSON file.", status=400)
        else:
            try:
                property_id = data['property_id']
                if isinstance(property_id, int):
                    properties = Property.objects.filter(pk=property_id)
                else:
                    properties = Property.objects.filter(pk__in=property_id)
                    print(len(property_id), len(properties))
                    if len(property_id) != len(properties):
                        raise Exception('Mismatch between number of properties')
            except:
                return HttpResponse("property_id invalid", status=400) 
            newOffer = Offer.objects.create(
                offerAmount=data['offerAmount'],
                offerDate=data['offerDate'],
                user_id=request.user
            )
            newOffer.propertyBuilding.set(properties)
            propertiesList = []
            for propertyBuilding in newOffer.propertyBuilding.all():
                propertyTemp ={
                    "property_id": propertyBuilding.id,
                    "propertyAddress": propertyBuilding.propertyAddress,
                    "propertyCreatedDate": propertyBuilding.propertyCreatedDate,
                    "propertyMarketPrice": propertyBuilding.propertyMarketPrice,
                    "propertyDescription": propertyBuilding.propertyDescription,
                    "propertySqFt": propertyBuilding.propertySqFt,
                    "propertyBedrooms": propertyBuilding.propertyBedrooms,
                    "propertyBathrooms": propertyBuilding.propertyBathrooms
                }
                propertiesList.append(propertyTemp)
            offerJSON = {
                "offerAmount":newOffer.offerAmount,
                "offerDate":newOffer.offerDate,
                "offerCounterAmount": newOffer.offerCounterAmount,
                "offerCounterDate": newOffer.offerCounterDate,
                "propertyBuilding": propertiesList,
                "user_id":newOffer.user_id.id
            }
            return JsonResponse(offerJSON, status=200)

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
            return HttpResponse("Got all coupons")
        if request.method == "POST":
            return HttpResponse("Made a new coupon")
        if request.method == "DELETE":
            return HttpResponse("Deleted a coupon")