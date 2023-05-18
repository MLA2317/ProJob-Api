from django.urls import path
from .views import EmailSendAPI

urlpatterns = [
    path('send-email/', EmailSendAPI.as_view()),
]