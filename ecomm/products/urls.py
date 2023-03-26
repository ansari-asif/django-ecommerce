from django.urls import path
from products.views import get_products,add_to_cart

urlpatterns = [
    path('<slug>/', get_products , name='get_products'),    
]
