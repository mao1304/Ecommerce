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

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.save() 
        cart = request.session.session_key 
    return cart


@method_decorator(csrf_exempt, name='dispatch')
class add_cart(APIView):
    print('ps 1')
    def post(self, request):  
        print('ps 2')
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)  
        try:
            cart = Cart.objects.get(Cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(Cart_id=_cart_id(request))
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(Product=product, Cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(Product=product, Cart=cart, quantity=1)
            cart_item.save()
        return Response('item add to cart successfully', status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class remove_cart(APIView):
    def post(self,request):
        product_id = request.data.get('product_id')
        cart = Cart.objects.get(Cart_id = _cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(Product=product, Cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        
        return Response('item remove to cart susesfully', status=status.HTTP_200_OK)
    
@method_decorator(csrf_exempt, name='dispatch')  
class remove_cart_item(APIView):
    def post(self,request):
        product_id = request.data.get('product_id')
        cart = Cart.objects.get(Cart_id = _cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(Product=product, Cart=cart)
        cart_item.delete()

        return Response('item remove to cart susesfully', status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class cart(APIView):
    print("1")

    def get(self, request, total=0, quantity=0, cart_items=None):
        print("2")
        cart_items = []
        print(cart_items)
        try:
            print("3")
            cart = Cart.objects.get(Cart_id=_cart_id(request))
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

