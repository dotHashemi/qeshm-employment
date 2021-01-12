from django.contrib.auth.models import User
from accounts.models import Verify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.serializers import RegistrationSerializer, VerifySerializer


class Registration(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            content = serializer.create()
            return Response(content, status=201)
        else:
            return Response({
                'errors': serializer.errors
            }, status=400)


class ResetPassword(APIView):
    def post(request):
        thisPhone = request.data['phone']
        thisPassword = request.data['password']
        thisConfirm = request.data['confirm']

        verify = Verify.objects.filter(phone=thisPhone).first()

        if verify and verify.status and thisPassword == thisConfirm:
            user = User.objects.filter(account__phone=thisPhone)
            user.set_password(thisPassword)
            user.save()
            return Response({
                'message': 'password was changed.'
            }, status=200)
        else:
            return Response({
                'errors': 'request is not valid.'
            }, status=400)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(request):
        thisPassword = request.data['password']
        thisConfirm = request.data['confirm']

        if thisPassword == thisConfirm:
            user = request.user
            user.set_password(thisPassword)
            user.save()
            return Response({
                'message': 'password was changed.'
            }, status=200)
        else:
            return Response({
                'errors': 'request is not valid.'
            }, status=400)


class VerifyCode(APIView):
    def post(self, request, type=None):
        request.data['type'] = type
        serializer = VerifySerializer(data=request.data)

        if serializer.is_valid():
            if serializer.check():
                return Response(status=200)
            else:
                return Response({
                    'errors': "inputs are not valid."
                }, status=400)
        else:
            return Response({
                'errors': serializer.errors
            }, status=400)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=200)
