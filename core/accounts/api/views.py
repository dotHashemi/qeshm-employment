from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import RegistrationSerializer, VerifySerializer


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
        pass


class ChangePassword(APIView):
    def post(request):
        pass


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
