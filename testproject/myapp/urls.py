from django.urls import path

from .views import *

app_name = 'myapp'
urlpatterns = [
    # users
    path('download_pdf/', download_pdf, name='download_pdf'),
    path('users/<int:user_id>', get_or_update_or_delete_user, name='get_or_edit_user'),
    path('users/', get_or_create_users, name='get_or_create_users'),
    path('users-by-header/', get_users_by_header, name='get_users_by_header'),

    # products
    path('products/', get_products, name='get_products'),
    path('add-to-cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>', remove_from_cart, name='remove_from_cart'),
    path('cart/', get_cart, name='get_cart'),
]