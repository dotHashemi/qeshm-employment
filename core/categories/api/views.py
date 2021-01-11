from rest_framework.response import Response
from categories.api.serializers import CategorySerializer
from categories.models import Category
from rest_framework.views import APIView


class CategoryListAPIView(APIView):
    def get(self, requests, *args, **kwargs):
        queryset = Category.objects.filter(status=True)

        search = requests.GET.get('search', None)
        if search is not None:
            queryset = queryset.filter(title__icontains=search)

        serializer = CategorySerializer(queryset, many=True)

        return Response({
            'data': serializer.data
        }, status=200)
