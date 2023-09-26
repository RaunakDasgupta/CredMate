from django.urls import path
from .views import loan_application_api_view
urlpatterns = [
    path('loan-application/', loan_application_api_view, name='loan-application-api'),
]