from django.urls import path
from .views import loan_application_api_view, emi_payment_api_view, emi_retrieve_api_view
urlpatterns = [
    path('loan-application/', loan_application_api_view,
         name='loan-application-api'),
    path('emi-payment/', emi_payment_api_view, name='emi-payment-api'),
    path('get-statement/<int:loan_id>/', emi_retrieve_api_view, name='emi-api'),
]
