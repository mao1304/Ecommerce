from rest_framework import serializers

from .models import Cart, CartItem

class CartSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Cart
        fields = ('Cart_id')


class CartItemSerializer(serializers.ModelSerializer):
    class  Meta:
        model = CartItem
        fields = ('Product','Cart','quantity')