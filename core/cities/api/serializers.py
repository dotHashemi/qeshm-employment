from rest_framework import serializers
from cities.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']

    def validate(self, data):
        title = data.get("title", None)

        if not title or title == "":
            title = "No Title!"

        return data
