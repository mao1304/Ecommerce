from uuid import uuid4
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

def _cart_id(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(Cart_id=request.user)
        print(f'{cart} user {request.user.first_name}')
    return cart


# @method_decorator(csrf_exempt, name='dispatch')
# class add_cart(APIView):
#     def post(self, request):  
#         product_id = request.data.get('product_id')
#         product = Product.objects.get(id=product_id)  
#         try:
#             cart = Cart.objects.get(Cart_id=_cart_id(request))
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(Cart_id=_cart_id(request))
#             cart.save()
        
#         try:
#             cart_item = CartItem.objects.get(Product=product, Cart=cart)
#             cart_item.quantity += 1
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             cart_item = CartItem.objects.create(Product=product, Cart=cart, quantity=1)
#             cart_item.save()
#         return Response('item add to cart successfully', status=status.HTTP_200_OK)

# @method_decorator(csrf_exempt, name='dispatch')
# class remove_cart(APIView):
#     def post(self,request):
#         product_id = request.data.get('product_id')
#         cart = Cart.objects.get(Cart_id=_cart_id(request))
#         product = get_object_or_404(Product, id=product_id)
#         cart_item = CartItem.objects.get(Product=product, Cart=cart)

#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
        
#         return Response('item remove to cart susesfully', status=status.HTTP_200_OK)
    
# @method_decorator(csrf_exempt, name='dispatch')  
# class remove_cart_item(APIView):
#     def post(self,request):
#         product_id = request.data.get('product_id')
#         cart = request.data.get('cart_id')
#         # cart = Cart.objects.get(Cart_id = _cart_id(request))
#         cart = Cart.objects.get(Cart_id =cart)
#         product = get_object_or_404(Product, id=product_id)
#         cart_item = CartItem.objects.get(Product=product, Cart=cart)
#         cart_item.delete()

#         return Response('item remove to cart susesfully', status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class add_cart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, quantity=0):
        cart_products = request.data.get('cart', [])

        cart, created = Cart.objects.get_or_create(Cart_id=request.user)


        for products in cart_products:
            product_id = products.get('id')
            quantity = products.get('quantity')

            try:
                product = Product.objects.get(id=product_id)
                print(product)
                cart_item = CartItem.objects.get(Cart=cart, Product=product, is_active=True)
                print(cart_item)
                if quantity <= product.stock:
                    cart_item.quantity += quantity
                    cart_item.save()
                else:
                    cart_item.quantity = product.stock
                    cart_item.save()
            except CartItem.DoesNotExist:
                    print("entro al exept")
                    if quantity <= product.stock:
                        CartItem.objects.create(Cart=cart, Product=product, quantity=quantity)
                    else:
                        CartItem.objects.create(Cart=cart, Product=product, quantity=product.stock)


        return Response("products added", status=status.HTTP_200_OK)
    

@method_decorator(csrf_exempt, name='dispatch')
class checkout(APIView):
    print('entra')
    permission_classes = [IsAuthenticated]
    def get(self, request, total=0, quantity=0, cart_items=None):

        cart_items = []

        try:
            cart, created = Cart.objects.get_or_create(Cart_id=request.user)
            cart_items = CartItem.objects.filter(Cart=cart, is_active=True)

            for cart_item in cart_items:
                total += (cart_item.Product.price * cart_item.quantity)
                quantity += cart_item.quantity
                
        except ObjectDoesNotExist:
            pass

        cart_items_serialized = [model_to_dict(item) for item in cart_items]

        context = {
            'total': total,
            'quantity': quantity,
            'cart_item': cart_items_serialized,

        }
        return Response({'cart': context}, status=status.HTTP_200_OK)


class ProcessPaymentAPIView(APIView):
    def post(self, request):
        try:
            request_values = json.loads(request.body)
            payment_data = {
                "transaction_amount": float(request_values["transaction_amount"]),
                "token": request_values["token"],
                "installments": int(request_values["installments"]),
                "payment_method_id": request_values["payment_method_id"],
                "issuer_id": request_values["issuer_id"],
                "payer": {
                    "email": request_values["payer"]["email"],
                    "identification": {
                        "type": request_values["payer"]["identification"]["type"],
                        "number": request_values["payer"]["identification"]["number"],
                    },
                },
            }

            sdk = mercadopago.SDK(str(settings.YOUR_ACCESS_TOKEN))

            payment_response = sdk.payment().create(payment_data)

            payment = payment_response["response"]
            status = {
                "id": payment["id"],
                "status": payment["status"],
                "status_detail": payment["status_detail"],
            }

            return Response(data={"body": status, "statusCode": payment_response["status"]}, status=201)
        except Exception as e:
            return Response(data={"body": payment_response}, status=400)