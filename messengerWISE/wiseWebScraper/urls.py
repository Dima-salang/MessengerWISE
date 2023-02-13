from django.urls import path
from .views import WebHook, PrivacyPolicyView, TermsAndService

urlpatterns = [
    path('webhook/', WebHook.as_view(), name="webhook"),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name="privacy-policy"),
    path('terms-of-service/', TermsAndService.as_view(), name='terms-service'),
    
]