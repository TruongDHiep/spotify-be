# your_app/urls.py
from django.urls import path
from .views import PaymentView, CSRFTokenView,SavePaymentView

urlpatterns = [
    
    path("momo/", PaymentView.as_view(), name="momo-payment"),
    path("csrf/", CSRFTokenView.as_view(), name="csrf-token"),
    path("save-payment/", SavePaymentView.as_view(), name="save-payment"),
]
  