from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Cart.models import Cart, CartItem
from store.models import Product

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session_key
    return cart


class add_cart(APIView):
    def post(request, Prodcut_id):
        product = Product.objects.get(id=Prodcut_id)
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
            cart_item = CartItem.create(Product=product, Cart=cart, quantity=1)
            cart_item.save()
        return Response('item add to cart susefully', status=status.HTTP_200_OK)
    
class remove_cart(APIView):
    def post(request, Product_id):
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product, id=Product_id)
        cart_item = CartItem.objects.get(Product=product, Cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        
        return Response('item remove to cart susesfully', status=status.HTTP_200_OK)

class remove_cart_item(APIView):
    def post(request, Product_id):
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product, id=Product_id)
        cart_item = CartItem.objects.get(Product=product, Cart=cart)
        cart_item.delete()

        return Response('item remove to cart susesfully', status=status.HTTP_200_OK)


class cart(APIView):
    def get(request, total=0, quantity=0,cart_item=None):
        cart_item = []

        try:
            cart = Cart.objects.get(Cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(Cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.Product.price * cart_item.quantity)
                quantity += cart_item.quantity
        except ObjectDoesNotExist:
            pass

        context = {
            'total': total,
            'quantity': quantity,
            'cart_item': cart_items,
        }
        return Response (context, status=status.HTTP_200_OK)