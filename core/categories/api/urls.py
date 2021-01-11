from django.urls import path
from categories.api.views import CategoryListAPIView


urlpatterns = [
    path('', CategoryListAPIView.as_view())
]
