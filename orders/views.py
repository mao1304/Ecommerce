
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Cart.models import Cart, CartItem
from store.models import Product
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import mercadopago
import json
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@method_decorator(csrf_exempt, name='dispatch')
class ProcessPaymentAPIView(APIView):
    def post(self, request):
        # name = request.data.get('name')        
        # surname = request.data.get('surname')      
        # email = request.data.get('email')
        # phone = request.data.get('phone')
        # address = request.data.get('address')
        
        cart_items = []
        try:
            cart, created = Cart.objects.get_or_create(Cart_id=request.user)
            cart_items = CartItem.objects.filter(Cart=cart, is_active=True)

            sdk = mercadopago.SDK("TEST-8904218361067571-051317-2ec6bea238a4f48da5b9e5054d93af3d-1805958327")

            items = []
            for cart_item in cart_items:
                item = {
                    "id": str(cart_item.Product.id),
                    "title": cart_item.Product.Product_name,
                    "currency_id": "COP",
                    "picture_url": cart_item.Product.images,
                    "description": cart_item.Product.description,
                    "category_id": str(cart_item.Product.SubCategory),
                    "quantity": cart_item.quantity,
                    "unit_price": float(cart_item.Product.price)*10,
                }
                items.append(item)

            preference_data = {
                "items": items,
            #     "payer": {
            #         "name": name,
            #         "surname": surname,
            #         "email": email,
            #         "phone": {
            #             "area_code": "57",
            #             "number": phone
            #         },
            #     "identification": {
            #         "type": "CC",
            #         "number": "123456789"
            #     },
            #     "address": {
            #         "street_name": address
            #     }
            # },
            "back_urls": {
                "success": "https://n3b52h4k-5173.use2.devtunnels.ms/Products",
                "failure": "http://www.failure.com",
                "pending": "http://www.pending.com"
            },
            "auto_return": "approved",
            "notification_url": "https://x762022t-8000.use2.devtunnels.ms/payments/webhook/"
            }
            
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            sandbox_init_point = preference.get("sandbox_init_point")           
            init_point = preference.get("init_point")           
            print("____________________")
            print(preference)
            print("____________________")


            return Response({"INIT":sandbox_init_point,"INIT_POINT":init_point}, status=201)
        except Exception as e:
            error_message = str(e)
            return Response(data={"error": error_message}, status=400)




class webhook(APIView):
    def post(self, request):
        payment = request.query_params
        print(payment)
        data_id = request.query_params.get('data.id')
        type_value = request.query_params.get('type')

        print(f"data.id: {data_id}")
        print(f"type: {type_value}")
        if type_value == "payment":
            data = mercadopago.payment.findById(data_id)
            print("si")
        return HttpResponse(data)