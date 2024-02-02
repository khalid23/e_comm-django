from django.urls import path
from .views import home, collection_detail, category_detail, add_to_cart, get_cart_details, add_to_wishlist

urlpatterns = [
    path('', home, name='home'),
    path('collection/<int:collection_id>/', collection_detail, name='collection_detail'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('get_cart_details/', get_cart_details, name='get_cart_details'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
]
