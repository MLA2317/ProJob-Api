from django.urls import path
from . import views


urlpatterns = [
    path('list-create/', views.ContactListCreateView.as_view()),
    path('email/list-create/', views.SubscribeListCreateView.as_view())
]
