from django.urls import path
from .views import productList, productDetails, add_to_cart, remove_from_cart, update_cart_item, cart_detail

urlpatterns = [
    path('', productList, name='home'),
    path('products/<slug:slug>/', productDetails, name='product_details'),

    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
]
