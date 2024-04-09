from django.db import models
from django.urls import reverse

from store.models import Product
from accounts.models import Account

class Cart(models.Model):
    Cart_id = models.CharField(max_length=250, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.Cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null= True)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

def subtotal(self):
    return self.Product.price * self.quantity

    def __str__(self):
        return self.Product.Product_name

 

