from django.urls import path
from .views import CompanyListCreate, CountryListCreate, CityListCreate


urlpatterns = [
    path('api/city-list/', CityListCreate.as_view()),
    path('api/country-list/', CountryListCreate.as_view()),
    path('api/company-list/', CompanyListCreate.as_view()),
]