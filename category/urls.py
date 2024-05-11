from rest_framework import routers
from django.urls import path,include
from .views import CategoryView


router_category = routers.DefaultRouter()
router_category.register(r'all', CategoryView, 'categories')


urlpatterns = [
    path('', include(router_category.urls), name= 'producuts_by_category'),
]
