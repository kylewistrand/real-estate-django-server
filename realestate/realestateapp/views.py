from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Coupon, CouponType
from django.views.decorators.csrf import csrf_exempt
import json

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
    pass
    # if request.method == 'GET':

    # elif request.method == 'POST':
    # elif request.method == 'DELETE':
        