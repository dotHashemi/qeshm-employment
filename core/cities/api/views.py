from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from cities.api.serializers import CitySerializer
from cities.models import City


class CityListAPIView(APIView):
    def get(self, requests, format=None):
        queryset = City.objects.all()
        
        search = str(requests.GET['search'])
        if search is not None:
            print(search)
            queryset = queryset.filter(title__icontains=search)

        serializer = CitySerializer(queryset, many=True)

        return Response(serializer.data)
