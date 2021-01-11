from rest_framework.views import APIView
from rest_framework.response import Response

from advertisements.models import Advertisement
from advertisements.api.serializers import AdvertisementListSerializer


class AdvertisementListAPIView(APIView):
    def get(self, requests, *args, **kwargs):
        queryset = Advertisement.objects.filter(isActive=True, isVerified=True)
        serializer = AdvertisementListSerializer(queryset, many=True)

        return Response(serializer.data)


class AdvertisementDetailAPIView(APIView):
    pass


class AdvertisementCreateAPIView(APIView):
    pass


class AdvertisementUpdateAPIView(APIView):
    pass
