from django.db.models import fields
from rest_framework.fields import ReadOnlyField
from categories.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        
        fields = ['id', 'title', 'status', 'created']

        extra_kwargs = {
            'status': {'write_only': True}
        }
