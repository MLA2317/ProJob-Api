from django.urls import path
from .views import EmailView

urlpatterns = [
    path('send-email/', EmailView.as_view()),
]