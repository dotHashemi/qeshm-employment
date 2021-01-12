from django.urls import path

from advertisements.api.views import AdvertisementCreateAPIView, AdvertisementDetailAPIView, AdvertisementListAPIView


urlpatterns = [
    path('', AdvertisementListAPIView.as_view()),
    path('<int:id>/', AdvertisementDetailAPIView.as_view()),
    path('create/', AdvertisementCreateAPIView.as_view()),
]
