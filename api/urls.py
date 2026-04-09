from django.urls import path
from .views import (
    AddressListCreateAPIView,
    AddressDetailAPIView,
    set_default_address,
    #process_checkout; is temporarily unavailable, so it's commented out for now. need to implement it later and uncomment this line.  
)

urlpatterns = [
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),
    path('addresses/<int:pk>/set-default/', set_default_address, name='set-default-address'),
    #path('checkout/', process_checkout, name='process-checkout'),
]