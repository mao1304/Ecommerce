from django.urls import path

from . import views

urlpatterns = [
    # path("", views.cart.as_view(), name="cart"),
    path('add_cart/',views.add_cart.as_view(), name='add_cart' ),
    path('checkout/',views.checkout.as_view(), name='checkout' ),
    # path('remove_cart_item/',views.remove_cart_item.as_view(), name='remove_cart_item' ),
    
]
