from django.urls import path
from .views import register_user_api_view

urlpatterns = [
    path('register-user/', register_user_api_view, name='register-user'),
]