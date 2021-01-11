from django.urls import path

from advertisements.api.views import AdvertisementListAPIView


urlpatterns = [
    path('', AdvertisementListAPIView.as_view())
]
