from django.utils import timezone
from rest_framework.response import Response


class Error():
    def throw(message, status):
        return Response({
            "detail": message
        }, status=status)


class Success():
    def responseWithData(data, status):
        return Response({
            "data": data
        }, status=status)

    def response(message, status):
        return Response({
            "detail": message
        }, status=status)


class Compare():
    def verifyTime(created, minutes=5):
        if (created + timezone.timedelta(minutes=minutes)) >= timezone.now():
            return True
        return False
