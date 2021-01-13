from core.exceptions import InputDoesNotValid, ModelExist, TimeDoesNotValid
from random import randint
from django.contrib.auth.models import User
from accounts.models import Verify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import RegistrationSerializer, VerifySerializer
from core.helpers import Error, Success


class Registration(APIView):
    def post(self, request):
        request.data['username'] = request.data['phone']
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create()
            content = {
                "id": user.id,
                "phone": user.username
            }
            return Success.responseWithData(content, 201)
        else:
            return Error.throw(serializer.errors, 400)


class ResetPassword(APIView):
    def post(self, request):
        request.data['username'] = request.data['phone']
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.changePassword()
            content = {
                "id": user.id,
                "phone": user.username
            }
            return Success.responseWithData(content, 201)
        else:
            return Error.throw(serializer.errors, 400)


class VerifySendAPIView(APIView):
    def post(self, request, type):
        """ ..................................
            send verify code for phone numbers
            ..................................
        """
        code = randint(10000, 99999)
        request.data['type'] = type
        request.data['code'] = code
        serializer = VerifySerializer(data=request.data)

        try:
            if not serializer.is_valid():
                raise InputDoesNotValid

            if User.objects.filter(username=request.data.get("phone")).exists():
                if request.data.get("type") == "register":
                    raise ModelExist
            elif request.data.get("type") == "resetpass":
                raise User.DoesNotExist
            else:
                raise InputDoesNotValid

            verify = Verify.objects.get(phone=request.data.get("phone"))
            serializer.update(verify, serializer.data)

        except ModelExist:
            return Error.throw({"phone": ["phone exist."]}, 400)

        except InputDoesNotValid:
            return Error.throw(serializer.errors, 400)

        except User.DoesNotExist:
            return Error.throw("user does not exist.", 400)

        except Verify.DoesNotExist:
            serializer.save()

        # TODO: add sms functions
        return Success.responseWithData(serializer.data, 201)


class VerifyCheckAPIView(APIView):
    def post(self, request, type=None):
        """ .............................
            check the code is true or not
            .............................
        """
        request.data['type'] = type
        serializer = VerifySerializer(data=request.data)

        try:
            if not serializer.is_valid():
                raise InputDoesNotValid

            verify = serializer.verified()

            if not verify.isVerified:
                raise TimeDoesNotValid

            return Success.responseWithData({"phone": verify.phone}, status=200)

        except InputDoesNotValid:
            return Error.throw(serializer.errors, 400)

        except TimeDoesNotValid:
            return Error.throw("please do again.", 400)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Success.response("you are logged out.", 200)
