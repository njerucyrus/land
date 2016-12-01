from django.conf.urls import url
from payment import views

urlpatterns = [
    url(r'^notifications/$', views.get_transfer_fee_payment_ipn, ),
]
