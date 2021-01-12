from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import Registration, ResetPassword, Logout, VerifyCode


urlpatterns = [
    path('login/', obtain_auth_token, name='auth.login'),

    path('logout/', Logout.as_view(), name='auth.logout'),

    path('registration/', Registration.as_view(), name="auth.registration"),

    path('password/reset', Registration.post, name="auth.registration"),

    path('verify/<str:type>', VerifyCode.as_view(), name="auth.registration"),
]
