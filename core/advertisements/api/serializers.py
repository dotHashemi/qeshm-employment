from rest_framework import serializers

from cities.models import City
from categories.models import Category
from advertisements.models import Advertisement
from categories.api.serializers import CategorySerializer
from cities.api.serializers import CitySerializer


class AdvertisementListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    city = CitySerializer()

    class Meta:
        model = Advertisement

        fields = [
            'id',
            'city',
            'category',
            'title',
            'company',
            'isFullTime',
            'isRemote',
            'isInternship',
            'salary',
        ]

        extra_kwargs = {
            'status': {'write_only': True},
        }


class AdvertisementDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    city = CitySerializer()

    class Meta:
        model = Advertisement

        fields = [
            'id',
            'user',
            'city',
            'category',
            'title',
            'company',
            'description',
            'isFullTime',
            'isRemote',
            'isInternship',
            'salary',
            'status',
        ]

        extra_kwargs = {
            'status': {'write_only': True},
            'user': {'write_only': True},
        }

    def validate(self, attrs):
        city = attrs.get("city", None)
        if city is None or not City.objects.filter(id=city).exists():
            raise serializers.ValidationError("city is not valid.")

        category = attrs.get("category", None)
        if category is None or not Category.objects.filter(id=category).exists():
            raise serializers.ValidationError("category is not valid.")

        return attrs
