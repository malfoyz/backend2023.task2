from django.urls import path

from .views import *

app_name = 'users'
urlpatterns = [
    path('download_pdf/', download_pdf, name='download_pdf'),
    path('users/<int:user_id>', get_or_update_or_delete_user, name='get_or_edit_user'),
    path('users/', get_or_create_users, name='get_or_create_users'),
    path('users-by-header/', get_users_by_header, name='get_users_by_header')
]