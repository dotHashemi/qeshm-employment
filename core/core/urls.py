from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.api.urls')),
    path('api/cities/', include('cities.api.urls')),
    path('api/categories/', include('categories.api.urls')),
    path('api/advertisements/', include('advertisements.api.urls')),
]
