from django.urls import path
from .views import AccountRegisterView, AccountRU,MyHistoryJobListCreate, LoginView, MyProfileList
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
)

urlpatterns = [

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),


    path('api/register/', AccountRegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/retrive-update/<int:pk>/', AccountRU.as_view()),
    path('api/myprofile-list/', MyProfileList.as_view()),
    path('api/jobhistory/', MyHistoryJobListCreate.as_view()),

]
