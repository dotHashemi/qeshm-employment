from core.exceptions import DoesNotValid, Exist, TimeDoesNotValid
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
        # print(request.data)
        # return Success.response("", 200)

        if serializer.is_valid():
            user = serializer.create()
            Verify.objects.filter(phone=user.username).delete()

            content = {
                "id": user.id,
                "phone": user.username
            }

            return Success.responseWithData(content, 201)
        else:
            return Error.throw(serializer.errors, 400)


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
            if User.objects.filter(username=request.data.get("phone")).exists():
                raise Exist

            if not serializer.is_valid():
                raise DoesNotValid

            verify = Verify.objects.get(phone=request.data.get("phone"))
            serializer.update(verify, serializer.data)

        except Exist:
            return Error.throw({"phone": ["phone exist."]}, 400)

        except DoesNotValid:
            return Error.throw(serializer.errors, 400)

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
                raise DoesNotValid

            verify = serializer.verified()

            if not verify.isVerified:
                raise TimeDoesNotValid

            return Success.responseWithData({"phone": verify.phone}, status=200)

        except DoesNotValid:
            return Error.throw(serializer.errors, 400)

        except TimeDoesNotValid:
            return Error.throw("please do again.", 400)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=200)
