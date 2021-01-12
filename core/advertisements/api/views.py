from core.helpers import Error, Success
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from advertisements.models import Advertisement
from advertisements.api.serializers import AdvertisementCreateSerializer, AdvertisementDetailSerializer, AdvertisementListSerializer


class AdvertisementListAPIView(APIView):
    def get(self, requests):
        queryset = Advertisement.objects.filter(isActive=True, isVerified=True)
        serializer = AdvertisementListSerializer(queryset, many=True)

        return Success.responseWithData(serializer.data, 200)


class AdvertisementDetailAPIView(APIView):
    def get(self, requests, id):
        ad = Advertisement.objects.filter(
            id=id,
            isActive=True,
            isVerified=True
        ).first()

        if ad is None:
            return Error.throw("ad not found.", 404)

        serializer = AdvertisementDetailSerializer(ad)

        return Success.responseWithData(serializer.data, 200)


class AdvertisementCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, requests):
        serializer = AdvertisementCreateSerializer(data=requests.data)

        if serializer.is_valid():
            ad = serializer.create(requests.user)
            data = {
                'id': ad.id,
                'title': ad.title
            }
            return Success.responseWithData(data, 201)
        else:
            return Error.throw(serializer.errors, 400)


class AdvertisementUpdateAPIView(APIView):
    pass
