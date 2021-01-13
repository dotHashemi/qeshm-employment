from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import Registration, ResetPassword, LogoutAPIView, VerifySendAPIView, VerifyCheckAPIView


urlpatterns = [
    path('login/', obtain_auth_token),

    path('logout/', LogoutAPIView.as_view()),

    path('registration/', Registration.as_view()),

    path('password/reset/', ResetPassword.as_view()),

    path('verify/check/<str:type>', VerifyCheckAPIView.as_view()),
    path('verify/send/<str:type>', VerifySendAPIView.as_view()),
]
