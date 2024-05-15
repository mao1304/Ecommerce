from django.urls import path
from . import views



urlpatterns = [
    path("", views.ProcessPaymentAPIView.as_view(), name="ProcessPaymentAPIView"),    
    path("webhook/", views.webhook.as_view(), name="webhook")

]
