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
            'isMilitary',
            'salary',
        ]


class AdvertisementDetailSerializer(serializers.ModelSerializer):
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
            'description',
            'isFullTime',
            'isRemote',
            'isInternship',
            'isMilitary',
            'salary',
        ]

    # def validate(self, attrs):
    #     city = attrs.get("city", None)
    #     if city is None or not City.objects.filter(id=city).exists():
    #         raise serializers.ValidationError("city is not valid.")

    #     category = attrs.get("category", None)
    #     if category is None or not Category.objects.filter(id=category).exists():
    #         raise serializers.ValidationError("category is not valid.")

    #     return attrs


class AdvertisementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement

        fields = [
            'city',
            'category',
            'title',
            'company',
            'description',
            'isFullTime',
            'isRemote',
            'isInternship',
            'isMilitary',
            'salary',
        ]

    def create(self, user):
        city = self.validated_data.get("city")
        category = self.validated_data.get("category")
        title = self.validated_data.get("title")
        company = self.validated_data.get("company")
        description = self.validated_data.get("description")
        isFullTime = self.validated_data.get("isFullTime")
        isRemote = self.validated_data.get("isRemote")
        isInternship = self.validated_data.get("isInternship")
        isMilitary = self.validated_data.get("isMilitary")
        salary = self.validated_data.get("salary")

        ad = Advertisement.objects.create(
            user=user,
            city=city,
            category=category,
            title=title,
            company=company,
            description=description,
            isFullTime=isFullTime,
            isRemote=isRemote,
            isInternship=isInternship,
            isMilitary=isMilitary,
            salary=salary
        )

        return ad
