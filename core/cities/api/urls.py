from cities.models import City
from django.urls import path
from cities.api.views import CityListAPIView


urlpatterns = [
    path('', CityListAPIView.as_view()),
]
