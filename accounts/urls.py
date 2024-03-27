from django.urls import path, re_path
from . import views
from rest_framework import routers
# router_products = routers.DefaultRouter()
# router_products.register(r'registrer', views.registrer , 'registrer')

urlpatterns = [
    re_path('registrer/',views.registrer, name='registrer'),
    re_path('login/',views.login, name='login'),
    re_path('logout/',views.logout, name='logout'),
    re_path('profile/',views.profile, name='profile'),
    # path('login/',views.Login.as_view(), name='login'),
    # path('logout/',views.logout.as_view(), name='logout'),
]

