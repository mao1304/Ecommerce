from django.urls import path, re_path
from . import views
from rest_framework import routers
# router_products = routers.DefaultRouter()
# router_products.register(r'registrer', views.registrer , 'registrer')

urlpatterns = [
    re_path('registrer/',views.registrer, name='registrer'),
    path('login/',views.Login.as_view(), name='login'),
    path('logout/',views.Logout.as_view(), name='logout'),
    path('profile/',views.profile.as_view(), name='profile'),
    # path('login/',views.Login.as_view(), name='login'),
    # path('logout/',views.logout.as_view(), name='logout'),
]

