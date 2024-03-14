from rest_framework import routers
from django.urls import path,include
from .views import ProductView


router_products = routers.DefaultRouter()
router_products.register(r'', ProductView, 'product_detail')



urlpatterns = [
    path('<slug:category_slug>/', include(router_products.urls), name= 'product'),
]
