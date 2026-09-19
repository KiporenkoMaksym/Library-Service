from django.urls import path

from payment.views import (
    PaymentSuccessView,
    PaymentCancelView, PaymentListView, PaymentDetailView
)

urlpatterns = [
    path("success/", PaymentSuccessView.as_view(), name="success"),
    path("cancel/", PaymentCancelView.as_view(), name="cancel"),
    path("", PaymentListView.as_view(), name="list"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="detail")
]

app_name = "payment"
