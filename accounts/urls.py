from django.urls import path, include
from . import views
from rest_framework import routers
# router_products = routers.DefaultRouter()
# router_products.register(r'registrer', views.registrer , 'registrer')

urlpatterns = [
    path('registrer/',views.registrer.as_view(), name='registrer'),
    # path('login/',views.login, name='login'),
    # path('logout/',views.logout, name='logout'),
]

