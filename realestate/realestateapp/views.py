from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, QueryDict
from .models import (Property, PropertyType, Neighborhood, Ownership, Cart,
Photo, Property_Photo, Amenity, Property_Amenity, Offer, Role, User_Role)
from django.views.decorators.csrf import csrf_exempt
import json, hashlib
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, PropertiesForm
from datetime import datetime
from django.views.decorators.debug import sensitive_post_parameters
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from decimal import Decimal
import datetime
from .scrape import getLivability


# Create your views here.
# @csrf_exempt
# def coupons(request):
#     """Ability to view, delete, or create coupons."""
#     if request.method == 'GET':
#         if not request.user.is_authenticated:
#             return HttpResponse("Not logged in.", status=401)
#         coupons = Coupon.objects.all()
#         couponsList = []
#         for coupon in coupons:
#             couponTemp = {
#                 "couponName":coupon.couponName,
#                 "couponValue":coupon.couponValue,
#                 "couponDescription":coupon.couponDescription,
#                 "couponTypeName":coupon.couponType.couponTypeName,
#                 "couponTypeDescription":coupon.couponType.couponTypeDescription
#             }
#             couponsList.append(couponTemp)
#         return JsonResponse(couponsList, safe=False, status=200)
#     elif request.method == 'POST':
#         if not request.user.is_authenticated:
#             return HttpResponse("Not logged in.", status=401)
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#         except json.JSONDecodeError:
#             return HttpResponse("Error decoding JSON file.", status=400)
#         else:
#             try:
#                 couponT = CouponType()
#                 couponT.couponTypeName = data['couponTypeName']
#                 couponT.couponTypeDescription = data['couponTypeDescription']
#                 couponT.save()
#             #If coupon type has already been made, then retrieve it.
#             except:
#                 couponT = CouponType.objects.get(couponTypeName=data['couponTypeName'])
#             newCoupon = Coupon()
#             newCoupon.couponValue = data['couponValue']
#             newCoupon.couponName = data['couponName']
#             newCoupon.couponDescription = data['couponDescription']
#             newCoupon.couponType = couponT
#             newCoupon.save()
#             couponJSON = {
#                 "couponName":newCoupon.couponName,
#                 "couponValue":newCoupon.couponValue,
#                 "couponDescription":newCoupon.couponDescription,
#                 "couponTypeName":newCoupon.couponType.couponTypeName,
#                 "couponTypeDescription":newCoupon.couponType.couponTypeDescription
#             }
#             return JsonResponse(couponJSON, status=200)
#     elif request.method == 'DELETE':
#         if not request.user.is_authenticated:
#             return HttpResponse("Not logged in.", status=401)
#         coupons = Coupon.objects.all()
#         #Delete all of the coupons.
#         for coupon in coupons:
#             coupon.delete()
#         return HttpResponse("All coupons were deleted.", status=200)

@csrf_exempt
def properties(request):
    """Create a property listing, view all of your own properties, or delete all of your properties"""
    if request.method == 'GET':
        form = PropertiesForm()
        properties = Property.objects.exclude(id__in=Ownership.objects.filter(ownershipEndDate__isnull=True).values_list('property_id', flat=True))
        ownerships = Ownership.objects.all()
        return render(request, 'main/properties.html', {'form':form, 'ownerships':ownerships, 'properties':properties})
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse("Not logged in", status=400)
        else:
            form = PropertiesForm(request.POST)
            if form.is_valid():
                address = form.cleaned_data['address']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                # askingPrice = 0.0
                #Zillow reformat
                apiId = 'X1-ZWz1h4b5dpi4nf_1k6qj'
                addressWords = address.split()
                reformatAddress = ""
                for addressWord in addressWords:
                    reformatAddress = reformatAddress + "+" + addressWord
                reformatAddress = reformatAddress[1:]
                cityWords = city.split()
                reformatCity = ""
                for cityWord in cityWords:
                    reformatCity = reformatCity + "+" + cityWord
                reformatCity = reformatCity[1:]
                reformatCityState = reformatCity + "%2C+" + state
                url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=" + apiId +"&address=" + reformatAddress + "&citystatezip=" + reformatCityState
                
                #Zillow fetch
                r = uReq(url)
                # data = r.json()
                # citystatezip = data['SearchResults']['request']
                page_html = r.read()
                r.close()
                page_soup = soup(page_html, features="xml")
                status = int(page_soup.find('code').string)
                if(status != 0):
                    msg = ""
                    try:
                        msg = page_soup.find('text').string
                    except:
                        msg = "Error with request"
                    return HttpResponse(msg, status=status)

                propertyType = page_soup.find('useCode').string
                created = page_soup.find('last-updated').string
                createdDate = datetime.datetime.strptime(created, '%m/%d/%Y')
                priceString = "0"
                try:
                    priceString = page_soup.find('amount').string
                    if priceString == None:
                        try:   
                            priceString = page_soup.find('zindexValue').string
                        except:
                            priceString = "0"
                except: 
                    try:   
                        priceString = page_soup.find('zindexValue').string
                    except:
                        priceString = "0"
                priceIndex = priceString.find(',')
                if(priceIndex != -1):
                    priceString = priceString.replace(",", "")
                marketPrice = Decimal(priceString)
                askingPrice = marketPrice
                try:
                    sqFt = int(page_soup.find('finishedSqFt').string)
                except:
                    sqFt = 0
                bed = int(page_soup.find('bedrooms').string)
                bath = page_soup.find('bathrooms').string
                decimalPoint = bath.find('.')
                bath = bath[:decimalPoint]
                bathVal = int(bath)
                description = page_soup.find('homedetails').string
                neighborhoodName = page_soup.find('region')['name']

                try:
                    propType = PropertyType()
                    propType.propertyTypeName = propertyType
                    propType.save()
                except:
                    propType = PropertyType.objects.get(propertyTypeName=propertyType)
                
                try:
                    neighborhoodModel = Neighborhood()
                    neighborhoodModel.neighborhood_name = neighborhoodName
                    neighborhoodModel.save()
                except:
                    neighborhoodModel = Neighborhood.objects.get(neighborhood_name=neighborhoodName)

                livability = getLivability(city, state)

                prop = Property()
                prop.propertyAddress = page_soup.find('address').string
                prop.propertyType = propType
                prop.neighborhood = neighborhoodModel
                prop.propertyCreatedDate = createdDate
                prop.propertyMarketPrice = marketPrice
                prop.propertyDescription = description
                prop.propertySqFt = sqFt
                prop.propertyBedrooms = bed
                prop.propertyBathrooms = bathVal
                prop.propertyLivability = livability
                prop.save()

                owner = Ownership()
                owner.user_id = request.user
                owner.property_id = prop
                owner.ownershipPaidPrice = marketPrice
                owner.ownershipAskingPrice = askingPrice
                owner.save()

                form = PropertiesForm()
                properties = Property.objects.all()
                ownerships = Ownership.objects.all()
                return render(request, 'main/properties.html', {'form':form, 'ownerships':ownerships, 'properties':properties})
            else:
                return HttpResponse("Form is not valid", status=400)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return HttpResponse("Not logged in.", status=401)
        ownProperties = Ownership.objects.filter(user_id=request.user)
        #Delete only properties that user owns
        for ownership in ownProperties:
            prop = Property.objects.get(id=ownership.property_id.id)
            prop.delete()
        return HttpResponse("All of your properties were deleted.", status=200)


    # if request.method == 'GET':
    #     #Get properties user owns
    #     if not request.user.is_authenticated:
    #         return HttpResponse("Not logged in.", status=401)
    #     ownProperties = Ownership.objects.filter(user_id=request.user)
    #     propertiesList = []
    #     for ownership in ownProperties:
    #         prop = ownership.property_id
    #         propertyTemp = {
    #             "propertyType":prop.propertyType,
    #             "neighborhood":prop.neighborhood,
    #             "propertyAddress":prop.propertyAddress,
    #             "propertyCreatedDate":prop.propertyCreatedDate,
    #             "propertyMarketPrice":prop.propertyMarketPrice,
    #             "propertyDescription":prop.propertyDescription,
    #             "propertySqFt":prop.propertySqFt,
    #             "propertyBedrooms":prop.propertyBedrooms,
    #             "propertyBathrooms":prop.propertyBathrooms
    #         }
    #         propertiesList.append(propertyTemp)
    #     return JsonResponse(propertiesList, safe=False, status=200)
    # elif request.method == 'POST':
    #     if not request.user.is_authenticated:
    #         return HttpResponse("Not logged in.", status=401)
    #     try:
    #         data = json.loads(request.body.decode('utf-8'))
    #     except json.JSONDecodeError:
    #         return HttpResponse("Error decoding JSON file.", status=400)
    #     else:

    #         try:
    #             propertyT = PropertyType()
    #             propertyT.propertyTypeName = data['propertyTypeName']
    #             propertyT.propertyTypeDescription = data['propertyTypeDescription']
    #             propertyT.save()
    #         #If property type already exists, then retrieve it.
    #         except:
    #             propertyT = PropertyType.objects.get(propertyTypeName=data['propertyTypeName'])
    #         try:
    #             neighborhood = Neighborhood()
    #             neighborhood.neighborhood_name = data['neighborhoodName']
    #             neighborhood.neighborhood_desc = data['neighborhoodDescription']
    #             neighborhood.save()
    #         #If neighborhood already exists, then retrieve it.
    #         except:
    #             neighborhood = neighborhood.objects.get(neighborhood_name=data['neighborhoodName'])
    #         propTemp = Property()
    #         propTemp.neighborhood = neighborhood
    #         propTemp.propertyType = propertyT
    #         propTemp.propertyAddress = data['propertyAddress']
    #         propTemp.propertyMarketPrice = data['propertyMarketPrice']
    #         propTemp.propertyDescription = data['propertyDescription']
    #         propTemp.propertySqFt = data['propertySqFt']
    #         propTemp.propertyBedrooms = data['propertyBedrooms']
    #         propTemp.propertyBathrooms = data['propertyBathrooms']
    #         propTemp.save()

    #         amenity = Amenity()
    #         amenity.amenity_name = data['amenityName']
    #         amenity.amenity_desc = data['amenityDescription']
    #         amenity.save()

    #         propAmen = Property_Amenity()
    #         propAmen.property_id = propTemp
    #         propAmen.amenity = amenity
    #         propAmen.save()

    #         photo = Photo()
    #         photo.photo_file = data['photoFile']
    #         photo.save()

    #         propPhoto = Property_Photo()
    #         propPhoto.photo_id = photo
    #         propPhoto.property_id = propTemp
    #         propPhoto.save()

    #         owner = Ownership()
    #         owner.user_id = request.user
    #         owner.property_id = propTemp
    #         owner.ownershipAskingPrice = data['ownershipAskingPrice']
    #         owner.ownershipPaidPrice = data['ownershipPaidPrice']
    #         owner.save()

    #         propertyJSON = {
    #             "owner":owner.user_id.username,
    #             "ownerAskingPrice":owner.ownershipAskingPrice,
    #             "ownerPaidPrice":owner.ownershipPaidPrice,
    #             "propertyTypeName":propTemp.propertyType.propertyTypeName,
    #             "propertyTypeDescription":propTemp.propertyType.propertyTypeDescription,
    #             "neighborhoodName":propTemp.neighborhood.neighborhood_name,
    #             "neighborhoodDescription":propTemp.neighborhood.neighborhood_desc,
    #             "propertyAddress":propTemp.propertyAddress,
    #             "propertyCreatedDate":propTemp.propertyCreatedDate,
    #             "propertyMarketPrice":propTemp.propertyMarketPrice,
    #             "propertyDescription":propTemp.propertyDescription,
    #             "propertySqFt":propTemp.propertySqFt,
    #             "propertyBedrooms":propTemp.propertyBedrooms,
    #             "propertyBathrooms":propTemp.propertyBathrooms,
    #             "amenityName":amenity.amenity_name,
    #             "amenityDescription":amenity.amenity_desc
    #         }
    #         return JsonResponse(propertyJSON, status=200)

@csrf_exempt
def cart(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse("Not logged in.", status=401)
        properties = [cartItem.property_id for cartItem in Cart.objects.filter(cartRemovedDate__isnull=True).filter(user_id=request.user)]
        ownerships = Ownership.objects.all()
        return render(request, 'main/cart.html', {'ownerships':ownerships, 'properties':properties})
    if request.method == 'DELETE':
        propertyId = int(request.body)
        print(propertyId)
        Cart.objects.filter(cartRemovedDate__isnull=True).filter(user_id=request.user).filter(property_id=propertyId).update(cartRemovedDate=datetime.datetime.now())
        return HttpResponse("Item has been deleted from the cart.", status=200)
    if request.method == 'POST':
        currentCart = [cartItem.property_id for cartItem in Cart.objects.filter(cartRemovedDate__isnull=True).filter(user_id=request.user)]
        if len(currentCart) == 0:
            return HttpResponse("Cart is empty.", status=401)
        for prop in currentCart:
            newOwnership = Ownership.objects.create(
                user_id=request.user,
                property_id=prop,
                ownershipAskingPrice=prop.propertyMarketPrice,
                ownershipPaidPrice=prop.propertyMarketPrice,
            )

        Cart.objects.filter(cartRemovedDate__isnull=True).filter(user_id=request.user).update(cartRemovedDate=datetime.datetime.now())
        return HttpResponse("All items bought successfully.", status=200)
    else:
        return HttpResponse("Method not allowed.", status=405)

@csrf_exempt
def specificProperty(request, property_id):
    """Add property to cart, get property information, or delete specified property"""
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse("Not logged in.", status=401)
        propTemp = Property.objects.get(id=property_id)
        propertyJSON = {
            "propertyTypeName":propTemp.propertyType.propertyTypeName,
            "propertyTypeDescription":propTemp.propertyType.propertyTypeDescription,
            "neighborhoodName":propTemp.neighborhood.neighborhood_name,
            "neighborhoodDescription":propTemp.neighborhood.neighborhood_desc,
            "propertyAddress":propTemp.propertyAddress,
            "propertyCreatedDate":propTemp.propertyCreatedDate,
            "propertyMarketPrice":propTemp.propertyMarketPrice,
            "propertyDescription":propTemp.propertyDescription,
            "propertySqFt":propTemp.propertySqFt,
            "propertyBedrooms":propTemp.propertyBedrooms,
            "propertyBathrooms":propTemp.propertyBathrooms
        }
        return JsonResponse(propertyJSON, status=200)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse("Not logged in.", status=401)
        currentCart = [cartItem.property_id.id for cartItem in Cart.objects.filter(cartRemovedDate__isnull=True).filter(user_id=request.user)]

        if int(property_id) in currentCart:
            return HttpResponse('This property is already in your <a href="/cart">cart</a>.', status=401)
        cart = Cart()
        cart.user_id = request.user
        prop = Property.objects.get(id=property_id)
        cart.property_id = prop
        cart.save()
        return HttpResponseRedirect('/cart')
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return HttpResponse("Not logged in.", status=401)
        try:
            prop = Property.objects.get(id=property_id)
        except:
            return HttpResponse("Property doesn't exist", status=400)
        else:
            prop.delete()
            return HttpResponse("Property was successfully deleted", status=200)

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

@csrf_exempt
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
    If method is POST:
        Update user's role
    If method is DELETE:
        Delete user
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
    If method is PUT:
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
            return HttpResponse("Not implemented", status=201)
            # cartItems = Property.objects.all()
            # cartItemList = []
            # for cartItem in cartItems:
            #     cartTemp = {
            #         "property_name":cartItem.couponName,
            #         "proptery_price":cartItem.couponValue,
            #         "property_description":cartItem.couponDescription,
            #         "property_sqfoot":cartItem.couponType.couponTypeName,

            #     }
            #     cartItem.append(cartTemp)
            # return JsonResponse(cartItemList, safe=False, status=200)
    
        if request.method == "POST":
            return HttpResponse("Items Purchesed", status=201)

        if request.method == "DELETE":
            return HttpResponse("Delete cart item")

# def coupon_with_id(request):
#     "Allows admin user to edit, delete a certain coupon"
    
#     if User.is_superuser():
#         if request.method == "GET":
#             return HttpResponse("Got all coupons")
#         if request.method == "POST":
#             return HttpResponse("Made a new coupon")
#         if request.method == "DELETE":
#             return HttpResponse("Deleted a coupon")
