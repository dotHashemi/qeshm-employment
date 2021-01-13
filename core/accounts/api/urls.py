from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import Registration, ResetPassword, Logout, VerifySendAPIView, VerifyCheckAPIView


urlpatterns = [
    path('login/', obtain_auth_token, name='auth.login'),

    path('logout/', Logout.as_view(), name='auth.logout'),

    path('registration/', Registration.as_view(), name="auth.registration"),

    path('password/reset/', ResetPassword.as_view()),

    path('verify/check/<str:type>', VerifyCheckAPIView.as_view()),
    path('verify/send/<str:type>', VerifySendAPIView.as_view()),
]
